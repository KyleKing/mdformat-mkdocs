"""Match 'markdown anchors' from the `mkdocs-autorefs` plugin.

Matches:

```md
[](){#some-anchor-name}
```

Docs: https://mkdocstrings.github.io/autorefs

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.rules_inline import StateInline
from mdformat_admon.factories import new_token

_AUTOREFS_PATTERN = re.compile(r"\[\]\(<?>?\){#(?P<anchor>[^ }]+)}")
MKDOCSTRINGS_AUTOREFS_PREFIX = "mkdocstrings_autorefs"
MKDOCSTRINGS_HEADER_AUTOREFS_PREFIX = f"{MKDOCSTRINGS_AUTOREFS_PREFIX}_header"


def _mkdocstrings_autorefs_plugin(state: StateInline, silent: bool) -> bool:
    match = _AUTOREFS_PATTERN.match(state.src[state.pos : state.posMax])
    if not match:
        return False

    if silent:
        return True

    anchor = match["anchor"]
    with new_token(state, MKDOCSTRINGS_AUTOREFS_PREFIX, "a") as token:  # type: ignore[arg-type]
        token.attrs = {"id": anchor, "href": ""}
        token.meta = {"content": f"[](){{#{anchor}}}"}

    state.pos += match.end()

    return True


def _mkdocstrings_header_anchor_plugin(
    state: StateBlock,
    start_line: int,
    end_line: int,  # noqa: ARG001
    silent: bool,
) -> bool:
    """Identify when an autoref anchor is directly before a header.

    Simplified header parsing adapted from:
    https://github.com/executablebooks/markdown-it-py/blob/c10312e2e475a22edb92abede15d3dcabd0cac0c/markdown_it/rules_block/heading.py

    """
    if start_line == 0 or state.is_code_block(start_line):
        return False

    start = state.bMarks[start_line] + state.tShift[start_line]
    if state.src[start] != "#":
        return False

    prev_line = start_line - 1
    prev = state.bMarks[prev_line] + state.tShift[prev_line]
    maximum = state.eMarks[1]
    try:
        [prev_text, header] = state.src[prev:maximum].split("\n")
    except ValueError:
        return False
    if not _AUTOREFS_PATTERN.match(prev_text):
        return False

    if silent:
        return True

    [header_prefix, *header_text_parts] = header.split(" ")
    level = len(header_prefix)
    state.line = start_line + 1
    with new_token(state, MKDOCSTRINGS_HEADER_AUTOREFS_PREFIX, f"h{level}") as token:
        token.markup = "#" * level
        token.map = [start_line, state.line]

        inline = state.push("inline", "", 0)
        inline.content = " ".join(header_text_parts)
        inline.map = [start_line, state.line]
        inline.children = []

    return True


def mkdocstrings_autorefs_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.before(
        "link",
        MKDOCSTRINGS_AUTOREFS_PREFIX,
        _mkdocstrings_autorefs_plugin,
        {"alt": ["link"]},
    )
    md.block.ruler.before(
        "heading",
        MKDOCSTRINGS_HEADER_AUTOREFS_PREFIX,
        _mkdocstrings_header_anchor_plugin,
        {"alt": ["heading"]},
    )
