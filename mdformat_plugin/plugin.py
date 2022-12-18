from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    pass


def _render_table(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode` of type "table".

    Change "table" to the name of the syntax you want to render.
    """
    return ""


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {"table": _render_table}
