"""Public Extension."""

from __future__ import annotations

import textwrap
from functools import partial
from typing import TYPE_CHECKING

from mdformat.renderer import DEFAULT_RENDERERS, RenderContext, RenderTreeNode

from ._helpers import ContextOptions, get_conf
from ._normalize_list import normalize_list as unbounded_normalize_list
from ._postprocess_inline import postprocess_list_wrap
from .mdit_plugins import (
    AMSMATH_BLOCK,
    DOLLARMATH_BLOCK,
    DOLLARMATH_BLOCK_LABEL,
    DOLLARMATH_INLINE,
    MKDOCSTRINGS_AUTOREFS_PREFIX,
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
    MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX,
    PYMD_ABBREVIATIONS_PREFIX,
    PYMD_CAPTIONS_PREFIX,
    PYMD_SNIPPET_PREFIX,
    PYTHON_MARKDOWN_ATTR_LIST_PREFIX,
    TEXMATH_BLOCK_EQNO,
    escape_deflist,
    material_admon_plugin,
    material_content_tabs_plugin,
    material_deflist_plugin,
    mkdocstrings_autorefs_plugin,
    mkdocstrings_crossreference_plugin,
    pymd_abbreviations_plugin,
    pymd_admon_plugin,
    pymd_arithmatex_plugin,
    pymd_captions_plugin,
    pymd_snippet_plugin,
    python_markdown_attr_list_plugin,
    render_material_definition_body,
    render_material_definition_list,
    render_material_definition_term,
)

if TYPE_CHECKING:
    import argparse
    from collections.abc import Mapping

    from markdown_it import MarkdownIt
    from mdformat.renderer.typing import Postprocess, Render


def cli_is_ignore_missing_references(options: ContextOptions) -> bool:
    """user-specified flag to turn off bracket escaping when no link reference found.

    Addresses: https://github.com/KyleKing/mdformat-mkdocs/issues/19

    """
    return bool(get_conf(options, "ignore_missing_references")) or False


def cli_is_align_semantic_breaks_in_lists(options: ContextOptions) -> bool:
    """user-specified flag for toggling semantic breaks.

    - 3-spaces on subsequent lines in semantic numbered lists
    - and 2-spaces on subsequent bulleted items

    """
    return bool(get_conf(options, "align_semantic_breaks_in_lists")) or False


def cli_is_no_mkdocs_math(options: ContextOptions) -> bool:
    """user-specified flag to disable math/LaTeX rendering."""
    return bool(get_conf(options, "no_mkdocs_math")) or False


def add_cli_argument_group(group: argparse._ArgumentGroup) -> None:
    """Add options to the mdformat CLI.

    Stored in `mdit.options["mdformat"]["plugin"]["mkdocs"]`

    """
    group.add_argument(
        "--align-semantic-breaks-in-lists",
        action="store_const",
        const=True,
        help="If specified, align semantic indents in numbered and bulleted lists to the text",
    )
    group.add_argument(
        "--ignore-missing-references",
        action="store_const",
        const=True,
        help="If set, do not escape link references when no definition is found. This is required when references are dynamic, such as with python mkdocstrings",
    )
    group.add_argument(
        "--no-mkdocs-math",
        action="store_const",
        const=True,
        help="If set, disable math/LaTeX rendering (Arithmatex). By default, math is enabled.",
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser."""
    mdit.use(material_admon_plugin)
    if not cli_is_no_mkdocs_math(mdit.options):
        mdit.use(pymd_arithmatex_plugin)
    mdit.use(pymd_captions_plugin)
    mdit.use(material_content_tabs_plugin)
    mdit.use(material_deflist_plugin)
    mdit.use(mkdocstrings_autorefs_plugin)
    mdit.use(pymd_abbreviations_plugin)
    mdit.use(pymd_admon_plugin)
    mdit.use(pymd_snippet_plugin)
    mdit.use(python_markdown_attr_list_plugin)

    if cli_is_ignore_missing_references(mdit.options):
        mdit.use(mkdocstrings_crossreference_plugin)


def _render_node_content(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Return node content without additional processing."""
    return node.content


def _render_math_inline(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Render inline math with original delimiters."""
    markup = node.markup
    content = node.content
    if markup == "$":
        return f"${content}$"
    if markup == "\\(":
        return f"\\({content}\\)"
    # Fallback
    return f"${content}$"


def _render_math_block(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Render block math with original delimiters."""
    markup = node.markup
    content = node.content
    if markup == "$$":
        return f"$$\n{content.strip()}\n$$"
    if markup == "\\[":
        return f"\\[\n{content.strip()}\n\\]"
    # Fallback
    return f"$$\n{content.strip()}\n$$"


def _render_math_block_eqno(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Render block math with equation label."""
    markup = node.markup
    content = node.content
    label = node.info  # Label is stored in info field
    if markup == "$$":
        return f"$$\n{content.strip()}\n$$ ({label})"
    if markup == "\\[":
        return f"\\[\n{content.strip()}\n\\] ({label})"
    # Fallback
    return f"$$\n{content.strip()}\n$$ ({label})"


def _render_amsmath(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Render amsmath environment."""
    # Content already includes \begin{} and \end{}
    return node.content


def _render_meta_content(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Return node content without additional processing."""
    return node.meta.get("content", "")


def _render_inline_content(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Render the node's inline content."""
    [inline] = node.children
    return inline.content


def _render_code_inline(node: RenderTreeNode, context: RenderContext) -> str:
    r"""Render inline code, cleaning up whitespace from newline normalization.

    `markdown-it` normalizes newlines in inline code to spaces. This can result in
    unintended trailing spaces from original newlines before closing backticks.
    Per mdformat's own logic, trailing spaces are only intentional if there are
    also leading spaces. So we strip trailing spaces when there's no leading space.

    Example: `code\n` (newline) → `code ` (parsed) → `code` (rendered)

    This could break at any time, so this is a best effort to resolve issues like:
    https://github.com/KyleKing/mdformat-mkdocs/issues/34#issuecomment-3589835341

    """
    default_renderer = DEFAULT_RENDERERS.get("code_inline")
    if default_renderer is None:
        return node.content

    result = default_renderer(node, context)

    # Only process single-backtick code (not double-backtick code with embedded backticks)
    if not (result.startswith("`") and result.endswith("`") and "``" not in result):
        return result

    content = result[1:-1]  # Strip opening and closing backticks
    has_leading_space = content.startswith(" ")
    has_trailing_space = content.endswith(" ")

    # Strip trailing space only if there's no leading space and content is not all whitespace
    # This preserves the mdformat rule: spaces are only intentional when both are present
    if has_trailing_space and not has_leading_space and content.strip():
        return f"`{content.rstrip(' ')}`"

    return result


def _render_heading_autoref(node: RenderTreeNode, context: RenderContext) -> str:
    """Render autorefs directly above a heading."""
    [*autorefs, heading] = node.children
    lines = [_render_meta_content(n_, context) for n_ in autorefs]
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


def render_pymd_caption(node: RenderTreeNode, context: RenderContext) -> str:
    """Render caption with normalized format."""
    caption_type = node.info or "caption"
    attrs = node.meta.get("attrs")
    number = node.meta.get("number")
    rendered_content = "".join(
        child.render(context) for child in node.children[0].children
    )
    caption_number = f" | {number}" if number else ""
    caption_attrs = f"\n    {attrs}" if attrs else ""
    return f"/// {caption_type}{caption_number}{caption_attrs}\n{rendered_content}\n///"


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "admonition": add_extra_admon_newline,
    "admonition_title": render_admon_title,
    "admonition_mkdocs": add_extra_admon_newline,
    "admonition_mkdocs_title": render_admon_title,
    "code_inline": _render_code_inline,
    "content_tab_mkdocs": add_extra_admon_newline,
    "content_tab_mkdocs_title": render_admon_title,
    "dl": render_material_definition_list,
    "dt": render_material_definition_term,
    "dd": render_material_definition_body,
    # Math support (from mdit-py-plugins)
    DOLLARMATH_INLINE: _render_math_inline,
    DOLLARMATH_BLOCK: _render_math_block,
    DOLLARMATH_BLOCK_LABEL: _render_math_block_eqno,
    TEXMATH_BLOCK_EQNO: _render_math_block_eqno,
    AMSMATH_BLOCK: _render_amsmath,
    # Other plugins
    PYMD_CAPTIONS_PREFIX: render_pymd_caption,
    MKDOCSTRINGS_AUTOREFS_PREFIX: _render_meta_content,
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX: _render_cross_reference,
    MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX: _render_heading_autoref,
    PYMD_ABBREVIATIONS_PREFIX: _render_inline_content,
    PYMD_SNIPPET_PREFIX: _render_inline_content,
    PYTHON_MARKDOWN_ATTR_LIST_PREFIX: _render_meta_content,
}


normalize_list = partial(
    unbounded_normalize_list,  # type: ignore[has-type]
    check_if_align_semantic_breaks_in_lists=cli_is_align_semantic_breaks_in_lists,
)

# A mapping from `RenderTreeNode.type` to a `Postprocess` that does
# postprocessing for the output of the `Render` function. Unlike
# `Render` funcs, `Postprocess` funcs are collaborative: any number of
# plugins can define a postprocessor for a syntax type and all of them
# will run in series.
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "bullet_list": normalize_list,
    "inline": postprocess_list_wrap,  # type: ignore[has-type]
    "ordered_list": normalize_list,
    "paragraph": escape_deflist,
}
