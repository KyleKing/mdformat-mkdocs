"""mkdocstrings injection blocks.

Matches:

```md
::: package.module.Class
    options:
        heading_level: 2
```

Docs: https://mkdocstrings.github.io/usage/

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from mdit_py_plugins.utils import is_code_block

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_block import StateBlock

_INJECTION_PATTERN = re.compile(r"^:::\s+\S")
MKDOCSTRINGS_INJECTION_PREFIX = "mkdocstrings_injection"


def _get_line(state: StateBlock, line: int, base_indent: int) -> str:
    return state.src[state.bMarks[line] + base_indent : state.eMarks[line]]


def _mkdocstrings_injection(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    if is_code_block(state, start_line):
        return False

    base_indent = state.blkIndent
    header = _get_line(state, start_line, base_indent)
    if not _INJECTION_PATTERN.match(header):
        return False

    if silent:
        return True

    lines = [header]
    next_line = start_line + 1
    while next_line < end_line:
        if state.tShift[next_line] <= base_indent:
            break
        lines.append(_get_line(state, next_line, base_indent))
        next_line += 1

    token = state.push(MKDOCSTRINGS_INJECTION_PREFIX, "", 0)
    token.content = "\n".join(lines)
    token.block = True
    token.map = [start_line, next_line]

    state.line = next_line
    return True


def mkdocstrings_injection_plugin(md: MarkdownIt) -> None:
    md.block.ruler.before(
        "paragraph",
        MKDOCSTRINGS_INJECTION_PREFIX,
        _mkdocstrings_injection,
        {"alt": ["paragraph"]},
    )
