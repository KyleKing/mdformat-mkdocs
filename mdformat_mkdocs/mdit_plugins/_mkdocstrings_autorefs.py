"""Match 'markdown anchors' from the `mkdocs-autorefs` plugin.

Matches:

```md
[](){#some-anchor-name}
```

Docs: https://mkdocstrings.github.io/autorefs

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline
from mdformat_admon.factories import new_token

_AUTOREFS_PATTERN = re.compile(r"\[\]\(<?>?\){#(?P<anchor>[^ }]+)}")
MKDOCSTRINGS_AUTOREFS_PREFIX = "mkdocstrings_autorefs"


def _mkdocstrings_autorefs_plugin(state: StateInline, silent: bool) -> bool:
    match = _AUTOREFS_PATTERN.match(state.src[state.pos : state.posMax])
    if not match:
        return False

    if silent:
        return True

    anchor = match["anchor"]
    with new_token(state, MKDOCSTRINGS_AUTOREFS_PREFIX, "a") as token:
        token.attrs = {"id": anchor, "href": ""}
        token.meta = {"content": f"[](){{#{anchor}}}"}

    state.pos += match.end()

    return True


def mkdocstrings_autorefs_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.before(
        "link",
        MKDOCSTRINGS_AUTOREFS_PREFIX,
        _mkdocstrings_autorefs_plugin,
        {"alt": ["link"]},
    )
