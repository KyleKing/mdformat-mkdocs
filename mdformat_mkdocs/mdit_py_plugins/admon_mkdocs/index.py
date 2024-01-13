from markdown_it.rules_block import StateBlock

from ..admon_helpers import (
    Admonition,
    admon_plugin_factory,
    format_admon_markup,
    parse_possible_admon_factory,
)


def admonition_logic(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    parse_possible_admon = parse_possible_admon_factory(
        markers=("!!!", "???", "???+"), marker_len=3
    )
    result = parse_possible_admon(state, startLine, endLine, silent)
    if isinstance(result, Admonition):
        format_admon_markup(state, startLine, admonition=result)
        return True
    return result


admon_mkdocs_plugin = admon_plugin_factory("admonition_mkdocs", admonition_logic)
