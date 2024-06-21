"""Python-Markdown Abbreviations.

Matches:

```md
*[HTML]: Hyper Text Markup Language
```

Docs:
https://github.com/Python-Markdown/markdown/blob/ec8c305fb14eb081bb874c917d8b91d3c5122334/docs/extensions/abbreviations.md


"""

from __future__ import annotations

import re

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdit_py_plugins.utils import is_code_block

_ABBREVIATION_PATTERN = re.compile(
    r"\\?\*\\?\[(?P<label>[^\]\\]+)\\?\]: (?P<description>.+)",
)
PYMD_ABBREVIATIONS_PREFIX = "mkdocs_abbreviation"


def _new_match(state: StateBlock, start_line: int) -> re.Match | None:
    """Determine match between start and end lines."""
    start = state.bMarks[start_line] + state.tShift[start_line]
    maximum = state.eMarks[start_line]
    return _ABBREVIATION_PATTERN.match(state.src[start:maximum])


def _pymd_abbreviations(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
) -> bool:
    """Identifies syntax abbreviation syntax, but generates incorrect markup.

    To properly generate markup, the abbreviation descriptions would need to
    be stored in the state.env, but unlike markdown footnotes, the
    `mdkocs-abbreviations` aren't limited to the same file, so a full
    implementation in mdformat may not be possible, although someone more
    familiar with the library could probably find a way.

    If revisiting, the `mdformat-footnote` plugin is a great reference for how
    Material Abbreviations could be implemented in full:
    https://github.com/executablebooks/mdit-py-plugins/blob/d11bdaf0979e6fae01c35db5a4d1f6a4b4dd8843/mdit_py_plugins/footnote/index.py#L103-L198

    Additionally, reviewing the `python-markdown` implementation would likely
    be helpful:
    https://github.com/Python-Markdown/markdown/blob/ec8c305fb14eb081bb874c917d8b91d3c5122334/markdown/extensions/abbr.py

    """
    if is_code_block(state, startLine):
        return False

    match = _new_match(state, startLine)
    if not match:
        return False

    if silent:
        return True

    matches = [match]
    max_line = startLine
    while match:
        if max_line == endLine:
            break
        if match := _new_match(state, max_line + 1):
            max_line += 1
            matches.append(match)

    token = state.push(PYMD_ABBREVIATIONS_PREFIX, "", 0)
    token.block = True
    token.content = "\n".join(
        [f'*[{match["label"]}]: {match["description"]}' for match in matches],
    )

    state.line = max_line + 1

    return True


def pymd_abbreviations_plugin(md: MarkdownIt) -> None:
    md.block.ruler.before(
        "reference",
        PYMD_ABBREVIATIONS_PREFIX,
        _pymd_abbreviations,
        {"alt": ["paragraph", "reference"]},
    )
