from markdown_it.rules_block import StateBlock
from mdformat_admon.factories import (
    AdmonitionData,
    admon_plugin_factory,
    new_token,
    parse_possible_whitespace_admon_factory,
)


def format_content_tab_markup(
    state: StateBlock,
    start_line: int,
    admonition: AdmonitionData,
) -> None:
    title = admonition.meta_text.strip().strip("'\"")

    with new_token(state, "content-tab", "div") as token:
        token.markup = admonition.markup
        token.block = True
        token.attrs = {"class": "content-tab"}
        token.info = admonition.meta_text
        token.map = [start_line, admonition.next_line]

        with new_token(state, "content-tab-title", "p") as tkn_inner:
            tkn_inner.attrs = {"class": "content-tab-title"}
            tkn_inner.map = [start_line, start_line + 1]

            tkn_inline = state.push("inline", "", 0)
            tkn_inline.content = title
            tkn_inline.map = [start_line, start_line + 1]
            tkn_inline.children = []

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    state.parentType = admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.blkIndent = admonition.old_state.blkIndent
    state.line = admonition.next_line


def content_tab_logic(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
) -> bool:
    # Because content-tabs look like admonitions syntactically, we can
    #   reuse admonition parsing logic
    # TODO: recursively call the parser to identify all sequential content tabs
    parse_possible_whitespace_admon = parse_possible_whitespace_admon_factory(
        markers={"==="},
    )
    result = parse_possible_whitespace_admon(state, startLine, endLine, silent)
    if isinstance(result, AdmonitionData):
        format_content_tab_markup(state, startLine, admonition=result)
        return True
    return result


content_tabs_plugin = admon_plugin_factory("content_tabs", content_tab_logic)
