"""`mdformat` Plugin."""

from __future__ import annotations

import argparse
from functools import lru_cache, partial
from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import DEFAULT_RENDERERS, RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render
from mdformat_admon import RENDERERS as ADMON_RENDERS

from ._normalize_list import normalize_list as unbounded_normalize_list
from ._postprocess_inline import postprocess_inline
from .mdit_plugins import (
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
    content_tabs_plugin,
    mkdocs_admon_plugin,
    mkdocstrings_crossreference_plugin,
)

_IGNORE_MISSING_REFERENCES = None
"""user-specified flag to turn off bracket escaping when no link reference found.

Addresses: https://github.com/KyleKing/mdformat-mkdocs/issues/19

"""

_ALIGN_SEMANTIC_BREAKS_IN_LISTS = None
"""user-specified flag for toggling semantic breaks.

- 3-spaces on subsequent lines in semantic numbered lists
- and 2-spaces on subsequent bulleted items

"""


def add_cli_options(parser: argparse.ArgumentParser) -> None:
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
    mdit.use(content_tabs_plugin)
    mdit.use(mkdocs_admon_plugin)

    global _ALIGN_SEMANTIC_BREAKS_IN_LISTS  # noqa: PLW0603
    _ALIGN_SEMANTIC_BREAKS_IN_LISTS = mdit.options["mdformat"].get(
        "align_semantic_breaks_in_lists",
        False,
    )
    global _IGNORE_MISSING_REFERENCES  # noqa: PLW0603
    _IGNORE_MISSING_REFERENCES = mdit.options["mdformat"].get(
        "ignore_missing_references",
        False,
    )
    if _IGNORE_MISSING_REFERENCES:
        mdit.use(mkdocstrings_crossreference_plugin)


def _render_node_content(node: RenderTreeNode, context: RenderContext) -> str:  # noqa: ARG001
    """Return node content without additional processing."""
    return node.content


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


@lru_cache(maxsize=1)
def _match_plugin_renderer(syntax_type: str) -> Render | None:
    from mdformat.plugins import PARSER_EXTENSIONS  # noqa: PLC0415

    for name, plugin in PARSER_EXTENSIONS.items():
        # Ignore this plugin (mkdocs) to avoid recursion. Name is set in pyproject.toml
        if name != "mkdocs" and plugin.RENDERERS.get(syntax_type):
            return plugin.RENDERERS[syntax_type]
    return None


def _render_cross_reference(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a MKDocs crossreference link."""
    if _IGNORE_MISSING_REFERENCES:
        return _render_node_content(node, context)
    # Default to treating the matched content as a link
    return _render_with_default_renderer(node, context, "link")


def _render_links_and_mkdocs_anchors(
    node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Intercepts rendering of [MKDocs AutoRefs 'markdown anchors'](https://mkdocs.github.io/autorefs/#markdown-anchors).

    Replaces `[...](<>)` with `[...]()` to produce output like:

    ```md
    [](){#some-anchor-name}
    ```

    If no match, defers to other plugins or the default

    """
    syntax_type = node.type

    rendered = _render_with_default_renderer(node, context, syntax_type)
    if rendered.endswith("](<>)"):
        return rendered[:-3] + ")"

    # Run other plugin renders if they exist
    if plugin_render := _match_plugin_renderer(syntax_type):
        return plugin_render(node, context)
    return rendered


# A mapping from `RenderTreeNode.type` to a `Render` function that can
# render the given `RenderTreeNode` type. These override the default
# `Render` funcs defined in `mdformat.renderer.DEFAULT_RENDERERS`.
RENDERERS: Mapping[str, Render] = {
    "admonition_mkdocs": ADMON_RENDERS["admonition"],
    "admonition_mkdocs_title": ADMON_RENDERS["admonition_title"],
    "content_tab_mkdocs": ADMON_RENDERS["admonition"],
    "content_tab_mkdocs_title": ADMON_RENDERS["admonition_title"],
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX: _render_cross_reference,
    "link": _render_links_and_mkdocs_anchors,
}


def check_if_align_semantic_breaks_in_lists() -> bool:
    """Returns value of global variable."""
    return _ALIGN_SEMANTIC_BREAKS_IN_LISTS or False


normalize_list = partial(
    unbounded_normalize_list,
    check_if_align_semantic_breaks_in_lists=check_if_align_semantic_breaks_in_lists,
)

# A mapping from `RenderTreeNode.type` to a `Postprocess` that does
# postprocessing for the output of the `Render` function. Unlike
# `Render` funcs, `Postprocess` funcs are collaborative: any number of
# plugins can define a postprocessor for a syntax type and all of them
# will run in series.
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "bullet_list": normalize_list,
    "inline": postprocess_inline,
    "ordered_list": normalize_list,
}
