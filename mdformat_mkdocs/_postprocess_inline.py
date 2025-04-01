"""Postprocess inline."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ._helpers import FILLER_CHAR, MKDOCS_INDENT_COUNT, get_conf, rstrip_result

if TYPE_CHECKING:
    from mdformat.renderer import RenderContext, RenderTreeNode

FILLER = FILLER_CHAR * (MKDOCS_INDENT_COUNT - 2)  # `mdformat` default is two spaces
"""A spacer that is inserted and then removed to ensure proper word wrap."""

# Pattern to match HTML entities like &nbsp;
_HTML_ENTITY_PATTERN = re.compile(r"&[a-zA-Z]+;")


def _preserve_html_entities(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Replace HTML entities with placeholders and return a list of replacements."""
    replacements = []
    counter = 0

    def replace_entity(match: re.Match) -> str:
        nonlocal counter
        placeholder = f"__HTML_ENTITY_{counter}__"
        counter += 1
        replacements.append((placeholder, match.group(0)))
        return placeholder

    text = _HTML_ENTITY_PATTERN.sub(replace_entity, text)
    return text, replacements


def _restore_html_entities(text: str, replacements: list[tuple[str, str]]) -> str:
    """Restore HTML entities from their placeholders."""
    for placeholder, entity in replacements:
        text = text.replace(placeholder, entity)
    return text


@rstrip_result
def postprocess_list_wrap(
    text: str,
    node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Postprocess inline tokens.

    Fix word wrap for lists to account for the change in indentation.
    We fool word wrap by prefixing an unwrappable dummy string of the same length.
    This prefix needs to be later removed (in `merge_parsed_text`).

    Adapted from:
    https://github.com/hukkin/mdformat-gfm/blob/cf316a121b6cf35cbff7b0ad6e171f287803f8cb/src/mdformat_gfm/plugin.py#L86-L111

    """
    if not context.do_wrap:
        return text
    wrap_mode = get_conf(context.options, "wrap")
    if (
        not isinstance(wrap_mode, int)  # noqa: PLR0916
        or FILLER_CHAR in text
        or (node.parent and node.parent.type != "paragraph")
        or (
            node.parent
            and node.parent.parent
            and node.parent.parent.type != "list_item"
        )
    ):
        return text

    # Preserve HTML entities before wrapping
    text_with_placeholders, replacements = _preserve_html_entities(text)

    counter_ = -1
    parent = node.parent
    while parent and parent.type == "paragraph":
        parent = parent.parent
        counter_ += 1
    indent_count = max(counter_, 0)

    soft_break = "\x00"
    text_with_placeholders = text_with_placeholders.lstrip(soft_break).lstrip()
    filler = (FILLER * indent_count)[:-1] if indent_count else ""
    newline_filler = filler + FILLER if indent_count else FILLER[:-1]
    if len(text_with_placeholders) > wrap_mode:
        indent_length = MKDOCS_INDENT_COUNT * indent_count
        wrapped_length = -123
        words: list[str] = []
        for word in text_with_placeholders.split(soft_break):
            next_length = wrapped_length + len(word)
            if not words:
                words = [filler, word]
                wrapped_length = indent_length + len(word)
            elif next_length > wrap_mode:
                words += [word, newline_filler]
                wrapped_length = indent_length + len(word)
            else:
                words.append(word)
                wrapped_length = next_length + 1
        text_with_placeholders = soft_break.join(_w for _w in words if _w)
    else:
        text_with_placeholders = f"{filler}{soft_break}{text_with_placeholders}" if filler else text_with_placeholders

    # Restore HTML entities after wrapping
    return _restore_html_entities(text_with_placeholders, replacements)
