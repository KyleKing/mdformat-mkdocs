"""Ignore abbreviation syntax

Matches:

```md
*[HTML]: Hyper Text Markup Language
```

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.token import Token
from mdit_py_plugins.utils import is_code_block

ABBREVIATION_PATTERN = re.compile(r"\*\\?\[(?P<label>[^\]]+)\\?\]: .*")
PREFIX = "mkdocs_abbreviation"
PREFIX_BLOCK = f"{PREFIX}_paragraph"


def _mkdocs_abbreviation(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
) -> bool:
    """Identify an abbreviation.

    Adapted from:
    https://github.com/executablebooks/mdit-py-plugins/blob/d11bdaf0979e6fae01c35db5a4d1f6a4b4dd8843/mdit_py_plugins/footnote/index.py#L103-L198

    """
    if is_code_block(state, startLine):
        return False

    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    match = ABBREVIATION_PATTERN.match(state.src[start:maximum])
    if not match:
        return False

    if silent:
        return True

    open_token = Token(f"{PREFIX_BLOCK}_open", "", 1)
    open_token.meta = {"label": match["label"]}
    open_token.level = state.level
    state.level += 1
    state.tokens.append(open_token)

    oldParentType = state.parentType

    state.md.block.tokenize(state, startLine, endLine)

    state.parentType = oldParentType

    open_token.map = [startLine, state.line]

    token = Token(f"{PREFIX_BLOCK}_close", "", -1)
    state.level -= 1
    token.level = state.level
    state.tokens.append(token)

    token = state.push(PREFIX, "", 0)
    # FIXME: Keep iterating until the last Abbreviation to prevent breaks
    # token.content = match.group()
    token.content = state.src[start:]

    return True


def mkdocs_abbreviations_plugin(md: MarkdownIt) -> None:
    # md.inline.ruler.push(PREFIX, _mkdocs_abbreviation)
    md.block.ruler.before(
        "paragraph",
        PREFIX_BLOCK,
        _mkdocs_abbreviation,
        {"alt": ["paragraph"]},
    )
