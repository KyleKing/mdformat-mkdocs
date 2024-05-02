"""MKDocs AutoRefs 'markdown anchors'.

Docs: https://mkdocs.github.io/autorefs/#markdown-anchors

Matches:

```md
[](){#some-anchor-name}
```

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

_LINK_PATTERN = re.compile(r"\[\]\(\){[^}]+}")
LINK_PATTERN = re.compile(r"{")
PREFIX = "mkdocs_anchors"


def _mkdocs_anchors(state: StateInline, silent: bool) -> bool:
    # match = LINK_PATTERN.match(state.src[state.pos :])
    match = _LINK_PATTERN.match(state.src)
    if not match:
        return False
    # else:
    #     breakpoint()
    #     return False

    if silent:
        return True

    token = state.push(PREFIX, "", 0)
    token.content = match.group()

    state.pos += match.end()

    return True


def mkdocs_anchors_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.push(PREFIX, _mkdocs_anchors)
