"""Public Extension."""

from __future__ import annotations

import textwrap
from argparse import ArgumentParser
from collections.abc import Mapping
from functools import partial
from typing import Any

from markdown_it import MarkdownIt
from mdformat.renderer import DEFAULT_RENDERERS, RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render

from ._normalize_list import normalize_list as unbounded_normalize_list
from ._postprocess_inline import postprocess_list_wrap
from .mdit_plugins import (
    MKDOCSTRINGS_AUTOREFS_PREFIX,
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
    MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX,
    PYMD_ABBREVIATIONS_PREFIX,
    PYMD_SNIPPET_PREFIX,
    material_admon_plugin,
    material_content_tabs_plugin,
    mkdocstrings_autorefs_plugin,
    mkdocstrings_crossreference_plugin,
    pymd_abbreviations_plugin,
    pymd_admon_plugin,
    pymd_snippet_plugin,
)

ContextOptions = Mapping[str, Any]


def cli_is_ignore_missing_references(options: ContextOptions) -> bool:
    """user-specified flag to turn off bracket escaping when no link reference found.

    Addresses: https://github.com/KyleKing/mdformat-mkdocs/issues/19

    """
    return options["mdformat"].get("ignore_missing_references", False)


def cli_is_align_semantic_breaks_in_lists(options: ContextOptions) -> bool:
    """user-specified flag for toggling semantic breaks.

    - 3-spaces on subsequent lines in semantic numbered lists
    - and 2-spaces on subsequent bulleted items

    """
    return options["mdformat"].get("align_semantic_breaks_in_lists", False)


def add_cli_options(parser: ArgumentParser) -> None:
    """Add options to the mdformat CLI, to be stored in `mdit.options["mdformat"]`."""
    parser.add_argument(
        "--align-semantic-breaks-in-lists",
        action="store_true",
        help="If specified, align semantic indents in numbered and bulleted lists to the text",  # noqa: E501
    )
    parser.add_argument(
        "--ignore-missing-references",
        action="store_true",
        help="If set, do not escape link references when no definition is found. This is required when references are dynamic, such as with python mkdocstrings",  # noqa: E501
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """No changes to markdown parsing are necessary."""
    mdit.use(material_admon_plugin)
    mdit.use(material_content_tabs_plugin)
    mdit.use(mkdocstrings_autorefs_plugin)
    mdit.use(pymd_abbreviations_plugin)
    mdit.use(pymd_snippet_plugin)
    mdit.use(pymd_admon_plugin)

    if cli_is_ignore_missing_references(mdit.options):
        mdit.use(mkdocstrings_crossreference_plugin)


def _render_node_content(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Return node content without additional processing."""
    return node.content


def _render_meta_content(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Return node content without additional processing."""
    return node.meta.get("content", "")


def _render_inline_content(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Render the node's inline content."""
    [inline] = node.children
    return inline.content


def _render_heading_autoref(node: RenderTreeNode, context: RenderContext) -> str:
    """Render autorefs directly above a heading."""
    [*autorefs, heading] = node.children
    lines = [_render_meta_content(_n, context) for _n in autorefs]
    lines.append(f"{heading.markup} {_render_inline_content(heading, context)}")
    return "\n".join(lines)


def _render_with_default_renderer(
    node: RenderTreeNode,
    context: RenderContext,
    syntax_type: str,
) -> str:
    """Attempt to render using the mdformat DEFAULT.

    Adapted from:
    https://github.com/hukkin/mdformat-gfm/blob/bd3c3392830fc4805d51582adcd1ae0d0630aed4/src/mdformat_gfm/plugin.py#L35-L46

    """
    text = DEFAULT_RENDERERS.get(syntax_type, _render_node_content)(node, context)
    for postprocessor in context.postprocessors.get(syntax_type, ()):
        text = postprocessor(text, node, context)
    return text


def _render_cross_reference(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a MkDocs crossreference link."""
    if cli_is_ignore_missing_references(context.options):
        return _render_meta_content(node, context)
    # Default to treating the matched content as a link
    return _render_with_default_renderer(node, context, "link")


# Start: copied from mdformat-admon


def render_admon(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode` of type `admonition`."""
    prefix = node.markup.split(" ")[0]
    title = node.info.strip()
    title_line = f"{prefix} {title}"

    elements = [render for child in node.children if (render := child.render(context))]
    separator = "\n\n"

    # Then indent to either 3 or 4 based on the length of the prefix
    #   For reStructuredText, '..' should be indented 3-spaces
    #       While '!!!', , '...', '???', '???+', etc. are indented 4-spaces
    indent = " " * (min(len(prefix), 3) + 1)
    content = textwrap.indent(separator.join(elements), indent)

    return title_line + "\n" + content if content else title_line


def render_admon_title(
    node: RenderTreeNode,  # noqa: ARG001
    context: RenderContext,  # noqa: ARG001
) -> str:
    """Skip rendering the title when called from the `node.children`."""
    return ""


# End: copied from mdformat-admon


def add_extra_admon_newline(node: RenderTreeNode, context: RenderContext) -> str:
    """Return admonition with additional newline after the title for mkdocs."""
    result = render_admon(node, context)
    if "\n" not in result:
        return result
    title, *content = result.split("\n", maxsplit=1)
    return f"{title}\n\n{''.join(content)}"


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "admonition": add_extra_admon_newline,
    "admonition_title": render_admon_title,
    "admonition_mkdocs": add_extra_admon_newline,
    "admonition_mkdocs_title": render_admon_title,
    "content_tab_mkdocs": add_extra_admon_newline,
    "content_tab_mkdocs_title": render_admon_title,
    MKDOCSTRINGS_AUTOREFS_PREFIX: _render_meta_content,
    MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX: _render_heading_autoref,
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX: _render_cross_reference,
    PYMD_ABBREVIATIONS_PREFIX: _render_inline_content,
    PYMD_SNIPPET_PREFIX: _render_inline_content,
}


normalize_list = partial(
    unbounded_normalize_list,
    check_if_align_semantic_breaks_in_lists=cli_is_align_semantic_breaks_in_lists,
)

# A mapping from `RenderTreeNode.type` to a `Postprocess` that does
# postprocessing for the output of the `Render` function. Unlike
# `Render` funcs, `Postprocess` funcs are collaborative: any number of
# plugins can define a postprocessor for a syntax type and all of them
# will run in series.
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "bullet_list": normalize_list,
    "inline": postprocess_list_wrap,
    "ordered_list": normalize_list,
}
