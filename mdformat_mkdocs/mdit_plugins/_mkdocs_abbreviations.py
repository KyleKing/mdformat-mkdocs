"""Ignore abbreviation syntax

Matches:

```md
*[HTML]: Hyper Text Markup Language
```

"""

from __future__ import annotations

import re

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.token import Token
from mdit_py_plugins.utils import is_code_block

ABBREVIATION_PATTERN = re.compile(
    r"\\?\*\\?\[(?P<label>[^\]\\]+)\\?\]: (?P<description>.+)",
)
PREFIX = "mkdocs_abbreviation"
PREFIX_BLOCK = f"{PREFIX}_paragraph"


def _new_match(state: StateBlock, start_line: int) -> re.Match | None:
    """Determine match between start and end lines."""
    start = state.bMarks[start_line] + state.tShift[start_line]
    maximum = state.eMarks[start_line]
    return ABBREVIATION_PATTERN.match(state.src[start:maximum])


ITERS = 0


# PLANNED: replace with more than formatting the plain text
def _mkdocs_abbreviation(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
) -> bool:
    """Identify syntax abbreviation, but the markup is incorrect.

    To fix the generated markup, the abbreviation descriptions would need to
    be stored in the environment, but unlike markdown footnotes, the
    `mdkocs-abbreviations` can be global and may not be possible to support.
    See the below `mdformat-footnote` plugin to reference if implementing
    proper support for HTML:
    https://github.com/executablebooks/mdit-py-plugins/blob/d11bdaf0979e6fae01c35db5a4d1f6a4b4dd8843/mdit_py_plugins/footnote/index.py#L103-L198

    """
    if is_code_block(state, startLine):
        return False

    match = _new_match(state, startLine)
    if not match:
        return False

    if silent:
        return True

    global ITERS
    if ITERS > 3:
        raise ValueError("TOO MANY!")
    ITERS += 1

    matches = [match]
    max_line = startLine
    while match:
        if max_line == endLine:
            break
        if match := _new_match(state, max_line + 1):
            max_line += 1
            matches.append(match)

    open_token = Token(f"{PREFIX_BLOCK}_open", "", 1)
    open_token.meta = {"label": [_m["label"] for _m in matches]}
    open_token.level = state.level
    state.level += 1
    state.tokens.append(open_token)

    old_parent_type = state.parentType

    state.parentType = old_parent_type

    open_token.map = [startLine, max_line]

    token = Token(f"{PREFIX_BLOCK}_close", "", -1)
    state.level -= 1
    token.level = state.level
    state.tokens.append(token)

    token = state.push(PREFIX, "", 0)
    # token.block = True
    token.content = "\n".join(
        [f'*[{match["label"]}]: {match["description"]}' for match in matches],
    )

    state.line = max_line + 1

    return True


def mkdocs_abbreviations_plugin(md: MarkdownIt) -> None:
    global ITERS
    ITERS = 0
    # md.block.ruler.before(
    #     "reference",
    #     PREFIX,
    #     _mkdocs_abbreviation,
    #     {"alt": ["paragraph", "reference"]},
    # )
    md.block.ruler.before(
        "paragraph",
        PREFIX,
        _mkdocs_abbreviation,
        {"alt": ["paragraph"]},
    )
