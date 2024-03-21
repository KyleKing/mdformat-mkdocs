"""Adapted from `mdformat-wikilink`.

https://github.com/tmr232/mdformat-wikilink/blob/d095be227a3cefc18d6fd823d9eb6fdfeaa5c895/src/mdformat_wikilink/mdit_wikilink_plugin.py

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

LINK_PATTERN = re.compile(r"\[\[([^[|\]\n]+)(\|[^]\n]+)?\]\]")


def _wikilink_inline(state: StateInline, silent: bool) -> bool:
    if state.src[state.pos] != "[":  # Exit quickly
        return False

    match = LINK_PATTERN.match(state.src[state.pos :])
    if not match:
        return False

    if silent:
        return True

    token = state.push("wikilink", "", 0)
    token.content = match.group()

    state.pos += match.end()

    return True


def wikilink_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.push("wikilink", _wikilink_inline)
