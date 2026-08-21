"""Python-Markdown Extensions Generic Blocks.

Matches:

```md
/// details-example
    open: True

Content
///
```

Docs:
https://facelessuser.github.io/pymdown-extensions/extensions/blocks/

Block-specific options must directly follow the opening fence (no blank line) and be
indented at least four spaces; that indentation is preserved verbatim so it survives
formatting. `///caption`/`figure-caption`/`table-caption` blocks are excluded here and
handled by `pymd_captions_plugin` instead.

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from mdit_py_plugins.utils import is_code_block

from mdformat_mkdocs._synced.admon_factories._whitespace_admon_factories import (
    new_token,
)

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_block import StateBlock

_BLOCK_START_PATTERN = re.compile(r"^(?P<markup>/{3,})\s+(?P<rest>\S.*?)\s*$")
_BLOCK_END_PATTERN = re.compile(r"^(?P<markup>/{3,})\s*$")
_CAPTION_NAME_PATTERN = re.compile(r"^(figure-|table-)?caption\b")
PYMD_BLOCKS_PREFIX = "pymd_blocks"


def _src_in_line(state: StateBlock, line: int) -> str:
    """Get the source in a given line number, with leading indentation stripped."""
    start_pos = state.bMarks[line] + state.tShift[line]
    end_pos = state.eMarks[line]
    return state.src[start_pos:end_pos]


def _raw_line(state: StateBlock, line: int) -> str:
    """Get the source in a given line number, indentation intact."""
    return state.src[state.bMarks[line] : state.eMarks[line]]


def _find_end_line(
    state: StateBlock,
    start_line: int,
    end_line: int,
    fence_len: int,
) -> int | None:
    """Find the line closing the block, tracking any more-deeply-nested blocks."""
    stack = [fence_len]
    line = start_line + 1
    while line < end_line:
        text = _src_in_line(state, line)
        end_match = _BLOCK_END_PATTERN.match(text)
        if end_match and len(end_match.group("markup")) == stack[-1]:
            stack.pop()
            if not stack:
                return line
            line += 1
            continue
        start_match = _BLOCK_START_PATTERN.match(text)
        if start_match and len(start_match.group("markup")) > stack[-1]:
            stack.append(len(start_match.group("markup")))
        line += 1
    return None


def _parse_options(
    state: StateBlock,
    start_line: int,
    end_line: int,
) -> tuple[str, int]:
    """Collect indented option lines directly after the header, verbatim."""
    lines = []
    line = start_line + 1
    while line < end_line:
        text = _raw_line(state, line)
        if not text.strip() or not text[:1].isspace():
            break
        lines.append(text)
        line += 1
    return "\n".join(lines), line


def _pymd_blocks(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    """Detect pymdownx.blocks generic blocks and wrap them in a token."""
    if is_code_block(state, start_line):
        return False

    start_match = _BLOCK_START_PATTERN.match(_src_in_line(state, start_line))
    if start_match is None:
        return False
    name = start_match.group("rest").split("|", 1)[0].strip()
    if _CAPTION_NAME_PATTERN.match(name):
        return False

    fence_len = len(start_match.group("markup"))
    close_line = _find_end_line(state, start_line, end_line, fence_len)
    if close_line is None:
        return False

    if silent:
        return True

    options, content_start = _parse_options(state, start_line, close_line)

    old_parent_type = state.parentType
    old_line_max = state.lineMax
    state.parentType = PYMD_BLOCKS_PREFIX
    # Prevent lazy continuation from letting content, e.g. a paragraph, absorb
    # lines past the closing fence.
    state.lineMax = close_line

    with new_token(state, PYMD_BLOCKS_PREFIX, "div") as token:
        token.markup = start_match.group("markup")
        token.info = start_match.group("rest")
        token.meta = {"options": options}
        token.map = [start_line, close_line]

        state.md.block.tokenize(state, content_start, close_line)

    state.parentType = old_parent_type
    state.lineMax = old_line_max
    state.line = close_line + 1

    return True


def pymd_blocks_plugin(md: MarkdownIt) -> None:
    md.block.ruler.before(
        "fence",
        PYMD_BLOCKS_PREFIX,
        _pymd_blocks,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )
