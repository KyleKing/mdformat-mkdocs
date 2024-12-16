"""Python-Markdown Snippets.

WARNING: matches only the "scissors" portion, leaving the rest unparsed

```md
--8<-- ...
```

Docs: <https://facelessuser.github.io/pymd-extensions/extensions/snippets>

"""

from __future__ import annotations

import re

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdit_py_plugins.utils import is_code_block

from mdformat_mkdocs._synced.admon_factories import new_token

# _SNIPPET_MARKER = "--8<--"
_ABBREVIATION_PATTERN = re.compile(
    r"--8<-- (?P<label>.+)",
)
PYMD_SNIPPET_PREFIX = "pymd_snippet"


def _new_match(state: StateBlock, start_line: int) -> re.Match[str] | None:
    """Determine match between start and end lines."""
    start = state.bMarks[start_line] + state.tShift[start_line]
    maximum = state.eMarks[start_line]
    return _ABBREVIATION_PATTERN.match(state.src[start:maximum])


def _pymd_snippet(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    if is_code_block(state, start_line):
        return False

    match = _new_match(state, start_line)
    if match is None:
        return False

    if silent:
        return True

    max_line = start_line

    with new_token(state, PYMD_SNIPPET_PREFIX, "p"):
        tkn_inline = state.push("inline", "", 0)
        tkn_inline.content = match["label"]
        tkn_inline.map = [start_line, max_line]
        tkn_inline.children = []

    state.line = max_line

    return True


def pymd_snippet_plugin(md: MarkdownIt) -> None:
    md.block.ruler.before(
        "reference",
        PYMD_SNIPPET_PREFIX,
        _pymd_snippet,
        {"alt": ["paragraph"]},
    )
