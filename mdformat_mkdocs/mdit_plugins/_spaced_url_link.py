"""Inline rule: parse ``[text](url with spaces)`` as a link.

CommonMark requires angle brackets for link destinations containing spaces.
Python-Markdown/MkDocs users write these without angle brackets. Without
this rule, markdown-it treats the whole construct as plain text, and
mdformat's HTML stability check fires.

This rule fires BEFORE markdown-it's built-in link rule. When it detects a
URL with at least one literal space (and no angle brackets), it emits proper
link tokens with the space percent-encoded in the href, matching the HTML
that mdformat outputs for the corrected form ``[text](<url with spaces>)``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from markdown_it import MarkdownIt

if TYPE_CHECKING:
    from markdown_it.rules_inline import StateInline

SPACED_URL_LINK_PREFIX = "spaced_url_link"


def _spaced_url_link(state: StateInline, silent: bool) -> bool:
    src = state.src
    pos = state.pos

    if src[pos] != "[":
        return False

    bracket_end = src.find("]", pos + 1)
    if bracket_end == -1 or bracket_end + 1 >= len(src) or src[bracket_end + 1] != "(":
        return False

    paren_start = bracket_end + 2
    paren_end = src.find(")", paren_start)
    if paren_end == -1:
        return False

    url = src[paren_start:paren_end]
    if " " not in url or url.startswith("<"):
        return False

    first_space = url.index(" ")
    char_after_space = url[first_space + 1] if first_space + 1 < len(url) else ""
    if char_after_space in {'"', "'", "("}:
        return False

    if not silent:
        old_pos_max = state.posMax

        token = state.push("link_open", "a", 1)
        token.attrs = {"href": url.replace(" ", "%20")}
        token.markup = ""
        token.info = ""

        state.pos = pos + 1
        state.posMax = bracket_end
        state.linkLevel += 1
        state.md.inline.tokenize(state)
        state.linkLevel -= 1
        state.posMax = old_pos_max

        state.push("link_close", "a", -1)

    state.pos = paren_end + 1
    return True


def spaced_url_link_plugin(md: MarkdownIt) -> None:
    """Register the spaced-URL inline rule before the built-in link rule."""
    md.inline.ruler.before(
        "link",
        SPACED_URL_LINK_PREFIX,
        _spaced_url_link,
    )
