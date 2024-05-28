"""Ignore abbreviation syntax

Matches:

```md
*[HTML]: Hyper Text Markup Language
```

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.rules_inline import StateInline
from markdown_it.token import Token
from mdit_py_plugins.utils import is_code_block

ABBREVIATION_PATTERN = re.compile(r"\*\\?\[(?P<label>[^\]]+)\\?\]: ")
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

    pos = start  # PLANNED: Maybe?

    open_token = Token(f"{PREFIX}_open", "", 1)
    open_token.meta = {"label": match["label"]}
    open_token.level = state.level
    state.level += 1
    state.tokens.append(open_token)

    oldBMark = state.bMarks[startLine]
    oldTShift = state.tShift[startLine]
    oldSCount = state.sCount[startLine]
    oldParentType = state.parentType

    posAfterColon = pos
    initial = offset = (
        state.sCount[startLine]
        + pos
        - (state.bMarks[startLine] + state.tShift[startLine])
    )

    pos += match.end()

    state.tShift[startLine] = pos - posAfterColon
    state.sCount[startLine] = offset - initial

    state.bMarks[startLine] = posAfterColon
    state.blkIndent += 4
    state.parentType = PREFIX_BLOCK

    if state.sCount[startLine] < state.blkIndent:
        state.sCount[startLine] += state.blkIndent

    state.md.block.tokenize(state, startLine, endLine)

    state.parentType = oldParentType
    state.blkIndent -= 4
    state.tShift[startLine] = oldTShift
    state.sCount[startLine] = oldSCount
    state.bMarks[startLine] = oldBMark

    open_token.map = [startLine, state.line]

    token = Token(f"{PREFIX}_close", "", -1)
    state.level -= 1
    token.level = state.level
    state.tokens.append(token)

    return True


def _mkdocs_abbreviation_block(
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

    open_token = Token(f"{PREFIX}_open", "", 1)
    open_token.meta = {"label": match["label"]}
    open_token.level = state.level
    state.level += 1
    state.tokens.append(open_token)

    old_parent_type = state.parentType
    state.parentType = PREFIX_BLOCK

    state.md.block.tokenize(state, startLine, endLine)
    state.parentType = old_parent_type

    open_token.map = [startLine, state.line]

    token = Token(f"{PREFIX}_close", "", -1)
    state.level -= 1
    token.level = state.level
    state.tokens.append(token)

    return True


def _mkdocs_abbreviation_inline(state: StateInline, silent: bool) -> bool:
    start = state.pos - 1
    maximum = state.posMax
    match = ABBREVIATION_PATTERN.match(state.src[start:maximum])
    if not match:
        return False

    if silent:
        return True

    token = state.push(PREFIX, "", 0)
    token.content = match.group()

    state.pos += match.end()

    return True


def mkdocs_abbreviations_plugin(md: MarkdownIt) -> None:
    md.block.ruler.before(
        "paragraph",
        PREFIX_BLOCK,
        _mkdocs_abbreviation,
        # _mkdocs_abbreviation_block,
        {"alt": ["paragraph"]},
    )
    # md.inline.ruler.push(PREFIX, _mkdocs_abbreviation_inline)
    # md.inline.ruler.after(PREFIX_BLOCK, PREFIX, _mkdocs_abbreviation_inline)
