"""Ignore reference links without definitions.

Matches:

```md
[package.module.object][]
[Object][package.module.object]
```

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

LINK_PATTERN = re.compile(r"\[([^[|\]\n]+)\]\[([^\]\n]*)\]")
PREFIX = "mkdocstrings_crossreference"


def _mkdocstrings_crossreference(state: StateInline, silent: bool) -> bool:
    match = LINK_PATTERN.match(state.src[state.pos :])
    if not match:
        return False

    if silent:
        return True

    token = state.push(PREFIX, "", 0)
    token.content = match.group()

    state.pos += match.end()

    return True


def mkdocstrings_crossreference_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.push(PREFIX, _mkdocstrings_crossreference)
