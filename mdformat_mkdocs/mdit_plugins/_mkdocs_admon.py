"""MKDocs Admonition Plugin."""

from __future__ import annotations

from typing import Any

from markdown_it.rules_block import StateBlock
from mdformat_admon.factories import (
    AdmonitionData,
    admon_plugin_factory,
    new_token,
    parse_possible_whitespace_admon_factory,
    parse_tag_and_title,
)
from mdformat_admon.mdit_plugins import format_python_markdown_admon_markup

PREFIX = "admonition_mkdocs"
"""Prefix used to differentiate the parsed output."""

MKDOCS_ADMON_MARKERS = {"!!!", "???", "???+"}
"""All supported MKDocs Admonition markers."""


def format_admon_markup(
    state: StateBlock,
    start_line: int,
    admonition: AdmonitionData,
) -> None:
    """Format markup."""
    if admonition.marker == "!!!":
        format_python_markdown_admon_markup(state, start_line, admonition)
        return

    tags, title = parse_tag_and_title(admonition.meta_text)
    tag = tags[0]

    with new_token(state, PREFIX, "details") as token:
        token.markup = admonition.markup
        token.block = True
        attrs: dict[str, Any] = {"class": " ".join(tags)}
        if admonition.markup.endswith("+"):
            attrs["open"] = "open"
        token.attrs = attrs
        token.meta = {"tag": tag}
        token.info = admonition.meta_text
        token.map = [start_line, admonition.next_line]

        if title:
            title_markup = f"{admonition.markup} {tag}"
            with new_token(state, f"{PREFIX}_title", "summary") as tkn_title:
                tkn_title.markup = title_markup
                tkn_title.map = [start_line, start_line + 1]

                tkn_inline = state.push("inline", "", 0)
                tkn_inline.content = title
                tkn_inline.map = [start_line, start_line + 1]
                tkn_inline.children = []

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    state.parentType = admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.blkIndent = admonition.old_state.blkIndent
    state.line = admonition.next_line


def admonition_logic(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
) -> bool:
    """Parse MKDocs-style Admonitions.

    `Such as collapsible blocks
    <https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks>`.

    .. code-block:: md

        ???+ note
            *content*

    """
    parse_possible_whitespace_admon = parse_possible_whitespace_admon_factory(
        markers=MKDOCS_ADMON_MARKERS,
    )
    result = parse_possible_whitespace_admon(state, startLine, endLine, silent)
    if isinstance(result, AdmonitionData):
        format_admon_markup(state, startLine, admonition=result)
        return True
    return result


mkdocs_admon_plugin = admon_plugin_factory(PREFIX, admonition_logic)
