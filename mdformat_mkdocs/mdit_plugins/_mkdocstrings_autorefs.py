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

LINK_PATTERN = re.compile(r"\[\]\(<?>?\){#(?P<anchor>[^ }]+)}")
MKDOCSTRINGS_AUTOREFS_PREFIX = "mkdocstrings_autorefs"


def _mkdocstrings_autorefs_plugin(state: StateInline, silent: bool) -> bool:
    match = LINK_PATTERN.match(state.src[state.pos : state.posMax])
    if not match:
        return False

    if silent:
        return True

    anchor = match["anchor"]
    o_token = state.push(f"{MKDOCSTRINGS_AUTOREFS_PREFIX}_open", "a", 1)
    o_token.attrs = {"id": anchor, "href": ""}
    o_token.meta = {"content": f"[](){{#{anchor}}}"}
    state.push(f"{MKDOCSTRINGS_AUTOREFS_PREFIX}_close", "a", -1)

    state.pos += match.end()

    return True


def mkdocstrings_autorefs_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.before(
        "link",
        MKDOCSTRINGS_AUTOREFS_PREFIX,
        _mkdocstrings_autorefs_plugin,
        {"alt": ["link"]},
    )
