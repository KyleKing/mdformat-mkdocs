"""Match markdown anchors from the mkdocs-autorefs plugin.

Matches:

```md
[](){#some-anchor-name}
```

Docs: https://mkdocstrings.github.io/autorefs

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

LINK_PATTERN = re.compile(r"\[\]\(<?>?\){#(?P<anchor>[^}]+)}")
MKDOCS_ANCHORS_PREFIX = "mkdocs_anchor"


def _mkdocs_anchors_plugin(state: StateInline, silent: bool) -> bool:
    match = LINK_PATTERN.match(state.src[state.pos : state.posMax])
    if not match:
        return False

    if silent:
        return True

    state.push(MKDOCS_ANCHORS_PREFIX, "", 0)

    anchor = match["anchor"]
    state.push(
        f"{MKDOCS_ANCHORS_PREFIX}_open",
        "a",
        1,
        attrs={"id": anchor, "href": "???"},
        content="",
        meta={"content": f"[](){{#{anchor}}}"},
    )
    state.push(f"{MKDOCS_ANCHORS_PREFIX}_close", "a", -1)

    state.posMax = match.end()
    state.pos = match.end() + 1

    return True


def mkdocs_anchors_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.before(
        "link",
        MKDOCS_ANCHORS_PREFIX,
        _mkdocs_anchors_plugin,
        {"alt": ["link"]},
    )
