"""`mdformat` Plugin."""

from __future__ import annotations

import argparse
from functools import partial
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
    mdit.use(mkdocs_admon_plugin)
    mdit.use(content_tabs_plugin)

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
    return node.content


def _render_link(node: RenderTreeNode, context: RenderContext) -> str:
    if _IGNORE_MISSING_REFERENCES:
        return _render_node_content(node, context)
    link = DEFAULT_RENDERERS.get("link", _render_node_content)
    return link(node, context)


# A mapping from `RenderTreeNode.type` to a `Render` function that can
# render the given `RenderTreeNode` type. These override the default
# `Render` funcs defined in `mdformat.renderer.DEFAULT_RENDERERS`.
RENDERERS: Mapping[str, Render] = {
    "admonition_mkdocs": ADMON_RENDERS["admonition"],
    "admonition_mkdocs_title": ADMON_RENDERS["admonition_title"],
    "content_tab_mkdocs": ADMON_RENDERS["admonition"],
    "content_tab_mkdocs_title": ADMON_RENDERS["admonition_title"],
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX: _render_link,
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
