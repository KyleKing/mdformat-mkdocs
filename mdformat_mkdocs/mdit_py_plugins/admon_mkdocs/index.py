from typing import Any, Dict

from markdown_it.rules_block import StateBlock

from ..admon_helpers import (
    Admonition,
    admon_plugin_factory,
    format_python_markdown_admon_markup,
    new_token,
    parse_possible_admon_factory,
    parse_tag_and_title,
)


def format_admon_markup(
    state: StateBlock,
    start_line: int,
    admonition: Admonition,
) -> None:
    if admonition.marker == "!!!":
        return format_python_markdown_admon_markup(state, start_line, admonition)

    tags, title = parse_tag_and_title(admonition.meta_text)
    tag = tags[0]

    with new_token(state, "admonition", "details") as token:
        token.markup = admonition.markup
        token.block = True
        attrs: Dict[str, Any] = {"class": " ".join(tags)}
        if admonition.markup.endswith("+"):
            attrs["open"] = "open"
        token.attrs = attrs
        token.meta = {"tag": tag}
        token.info = admonition.meta_text
        token.map = [start_line, admonition.next_line]

        if title:
            title_markup = f"{admonition.markup} {tag}"
            with new_token(state, "admonition_title", "summary") as token:
                token.markup = title_markup
                token.map = [start_line, start_line + 1]

                token = state.push("inline", "", 0)
                token.content = title
                token.map = [start_line, start_line + 1]
                token.children = []

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    state.parentType = admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.blkIndent = admonition.old_state.blkIndent
    state.line = admonition.next_line


def admonition_logic(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    parse_possible_admon = parse_possible_admon_factory(markers={"!!!", "???", "???+"})
    result = parse_possible_admon(state, startLine, endLine, silent)
    if isinstance(result, Admonition):
        format_admon_markup(state, startLine, admonition=result)
        return True
    return result


admon_mkdocs_plugin = admon_plugin_factory("admonition_mkdocs", admonition_logic)
