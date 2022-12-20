import textwrap
from typing import Mapping
from functools import partial
from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render


def update_mdit(mdit: MarkdownIt) -> None:
    ...


def _render_list(node: RenderTreeNode, context: RenderContext, message: str) -> str:
    """Render a `RenderTreeNode` consistent with `mkdocs`."""
    return ""


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "bullet_list": partial(_render_list, message="bullet_list"),
    "ordered_list": partial(_render_list, message="ordered_list"),
    "list_item": partial(_render_list, message="list_item"),
}
