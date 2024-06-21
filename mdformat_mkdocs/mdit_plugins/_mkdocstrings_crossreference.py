"""Matches `mkdocstrings` cross-references.

Matches:

```md
[package.module.object][]
[Object][package.module.object]
```

Docs: <https://mkdocstrings.github.io/usage/#cross-references>

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

LINK_PATTERN = re.compile(r"\[([^[|\]\n]+)\]\[([^\]\n]*)\]")
MKDOCSTRINGS_CROSSREFERENCE_PREFIX = "mkdocstrings_crossreference"


def _mkdocstrings_crossreference(state: StateInline, silent: bool) -> bool:
    match = LINK_PATTERN.match(state.src[state.pos :])
    if not match:
        return False

    if silent:
        return True

    token = state.push(MKDOCSTRINGS_CROSSREFERENCE_PREFIX, "", 0)
    token.content = match.group()

    state.pos += match.end()

    return True


def mkdocstrings_crossreference_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.push(
        MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
        _mkdocstrings_crossreference,
    )
