from markdown_it.rules_block import StateBlock

from ..admon_helpers import (
    Admonition,
    admon_plugin_wrapper,
    format_admon_markup,
    parse_possible_admon,
)


def admonition_logic(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    result = parse_possible_admon(state, startLine, endLine, silent)
    if isinstance(result, Admonition):
        format_admon_markup(state, startLine, admonition=result)
        return True
    return result


admon_mkdocs_plugin = admon_plugin_wrapper("admonition_mkdocs", admonition_logic)


# from __future__ import annotations

# from typing import TYPE_CHECKING, Any, Callable, Dict, Sequence

# from markdown_it import MarkdownIt
# from markdown_it.rules_block import StateBlock
# from mdit_py_plugins.utils import is_code_block

# from ..admon.index import (
#     MARKER_CHARS,
#     MARKER_LEN,
#     MARKERS,
#     MAX_MARKER_LEN,
#     _get_tag,
#     _validate,
# )

# if TYPE_CHECKING:
#     from markdown_it.renderer import RendererProtocol
#     from markdown_it.token import Token
#     from markdown_it.utils import EnvType, OptionsDict


# def admonition_mkdocs(  # noqa: C901
#     state: StateBlock, startLine: int, endLine: int, silent: bool
# ) -> bool:
#     if is_code_block(state, startLine):
#         return False

#     start = state.bMarks[startLine] + state.tShift[startLine]
#     maximum = state.eMarks[startLine]

#     # Exit quickly on a non-match for first char
#     if state.src[start] not in MARKER_CHARS:
#         return False

#     # Check out the rest of the marker string
#     marker = ""
#     marker_len = MAX_MARKER_LEN
#     while marker_len > 0:
#         marker_pos = start + marker_len
#         markup = state.src[start:marker_pos]
#         if markup in MARKERS:
#             marker = markup
#             break
#         marker_len -= 1
#     else:
#         return False

#     params = state.src[marker_pos:maximum]

#     if not _validate(params):
#         return False

#     # Since start is found, we can report success here in validation mode
#     if silent:
#         return True

#     old_parent = state.parentType
#     old_line_max = state.lineMax
#     old_indent = state.blkIndent

#     blk_start = marker_pos
#     while blk_start < maximum and state.src[blk_start] == " ":
#         blk_start += 1

#     state.parentType = "admonition"
#     # Correct block indentation when extra marker characters are present
#     marker_alignment_correction = MARKER_LEN - len(marker)
#     state.blkIndent += blk_start - start + marker_alignment_correction

#     was_empty = False

#     # Search for the end of the block
#     next_line = startLine
#     while True:
#         next_line += 1
#         if next_line >= endLine:
#             # unclosed block should be autoclosed by end of document.
#             # also block seems to be autoclosed by end of parent
#             break
#         pos = state.bMarks[next_line] + state.tShift[next_line]
#         maximum = state.eMarks[next_line]
#         is_empty = state.sCount[next_line] < state.blkIndent

#         # two consecutive empty lines autoclose the block
#         if is_empty and was_empty:
#             break
#         was_empty = is_empty

#         if pos < maximum and state.sCount[next_line] < state.blkIndent:
#             # non-empty line with negative indent should stop the block:
#             # - !!!
#             #  test
#             break

#     # this will prevent lazy continuations from ever going past our end marker
#     state.lineMax = next_line

#     tags, title = _get_tag(params)
#     tag = tags[0]

#     # HACK: up to here us the same as ../admon/index.py

#     use_details = marker.startswith("???")

#     is_open = None
#     if use_details:
#         is_open = markup.endswith("+")

#     outer_div = "details" if use_details else "div"
#     token = state.push("admonition_mkdocs_open", outer_div, 1)
#     token.markup = markup
#     token.block = True
#     attrs: Dict[str, Any] = {"class": " ".join(tags)}
#     if not use_details:
#         attrs["class"] = f'admonition {attrs["class"]}'
#     if is_open is True:
#         attrs["open"] = "open"
#     token.attrs = attrs
#     token.meta = {"tag": tag}
#     token.content = title
#     token.info = params
#     token.map = [startLine, next_line]

#     if title:
#         title_markup = f"{markup} {tag}"
#         inner_div = "summary" if use_details else "p"
#         token = state.push("admonition_mkdocs_title_open", inner_div, 1)
#         token.markup = title_markup
#         if not use_details:
#             token.attrs = {"class": "admonition-title"}
#         token.map = [startLine, startLine + 1]

#         token = state.push("inline", "", 0)
#         token.content = title
#         token.map = [startLine, startLine + 1]
#         token.children = []

#         token = state.push("admonition_mkdocs_title_close", inner_div, -1)

#     state.md.block.tokenize(state, startLine + 1, next_line)

#     token = state.push("admonition_mkdocs_close", outer_div, -1)
#     token.markup = markup
#     token.block = True

#     state.parentType = old_parent
#     state.lineMax = old_line_max
#     state.blkIndent = old_indent
#     state.line = next_line

#     return True


# def admon_mkdocs_plugin(
#     md: MarkdownIt, render: None | Callable[..., str] = None
# ) -> None:
#     """Plugin to use
#     `python-markdown style admonitions
#     <https://python-markdown.github.io/extensions/admonition>`_.

#     .. code-block:: md

#         !!! note
#             *content*

#     `And mkdocs-style collapsible blocks
#     <https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks>`_.

#     .. code-block:: md

#         ???+ note
#             *content*

#     Note, this is ported from
#     `markdown-it-admon
#     <https://github.com/commenthol/markdown-it-admon>`_.
#     """

#     def renderDefault(
#         self: RendererProtocol,
#         tokens: Sequence[Token],
#         idx: int,
#         _options: OptionsDict,
#         env: EnvType,
#     ) -> str:
#         return self.renderToken(tokens, idx, _options, env)  # type: ignore

#     render = render or renderDefault

#     md.add_render_rule("admonition_mkdocs_open", render)
#     md.add_render_rule("admonition_mkdocs_close", render)
#     md.add_render_rule("admonition_mkdocs_title_open", render)
#     md.add_render_rule("admonition_mkdocs_title_close", render)

#     md.block.ruler.before(
#         "fence",
#         "admonition_mkdocs",
#         admonition_mkdocs,
#         {"alt": ["paragraph", "reference", "blockquote", "list"]},
#     )
