"""Ignore abbreviation syntax

Matches:

```md
*[HTML]: Hyper Text Markup Language
```

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

ABBREVIATION_PATTERN = re.compile(r"\*\\?\[[^\]]+\\?\]: .*\n?")
PREFIX = "mkdocs_abbreviation"


def _mkdocs_abbreviation(state: StateInline, silent: bool) -> bool:
    start = state.pos - 1
    match = ABBREVIATION_PATTERN.match(state.src[start:])
    if not match:
        return False

    if silent:
        return True

    token = state.push(PREFIX, "", 0)
    token.content = match.group()

    state.pos += match.end()

    return True


def mkdocs_abbreviations_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.push(PREFIX, _mkdocs_abbreviation)
