r"""Python-Markdown: Attribute List.

WARNING: does not properly render HTML with the attributes and does not
respect escaping '\\{ '

Docs: <https://python-markdown.github.io/extensions/attr_list>

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt

from mdformat_mkdocs._synced.admon_factories import new_token

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_inline import StateInline

_ATTR_LIST_PATTERN = re.compile(r"{:? (?P<attrs>[^}]+) }")

PYTHON_MARKDOWN_ATTR_LIST_PREFIX = "python_markdown_attr_list"


def _python_markdown_attr_list(state: StateInline, silent: bool) -> bool:
    match = _ATTR_LIST_PATTERN.match(state.src[state.pos : state.posMax])
    if not match:
        return False

    if state.pos > 0 and state.src[state.pos - 1] == "\\":
        return False

    # Check if we're potentially inside a link by looking for an unclosed '['
    # before us and a '](' after the match
    if state.linkLevel > 0:
        return False

    # Look backwards for unclosed '['
    search_start = max(0, state.pos - 100)  # Limit backwards search
    text_before = state.src[search_start:state.pos]
    open_brackets = text_before.count("[") - text_before.count("]")
    if open_brackets > 0:
        # We might be inside a link, check if there's '](' after our match
        match_end_pos = state.pos + match.end()
        if match_end_pos < len(state.src):
            lookahead = state.src[match_end_pos:min(match_end_pos + 100, len(state.src))]
            if "](" in lookahead:
                # Very likely inside link text, don't match
                return False

    if silent:
        return True

    original_pos = state.pos
    original_pos_max = state.posMax
    state.pos += 1
    state.posMax = state.pos + (match.end() - len(" }"))
    with new_token(state, PYTHON_MARKDOWN_ATTR_LIST_PREFIX, "span") as token:
        token.attrs = {"attributes": match["attrs"].split(" ")}  # type: ignore[dict-item]
        token.meta = {"content": match.group()}

        state.md.inline.tokenize(state)

    state.pos = original_pos
    state.posMax = original_pos_max
    state.pos += match.end()

    return True


def python_markdown_attr_list_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.push(
        PYTHON_MARKDOWN_ATTR_LIST_PREFIX,
        _python_markdown_attr_list,
    )
