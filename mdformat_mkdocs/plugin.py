import textwrap
from typing import Mapping
from functools import partial

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render


def update_mdit(mdit: MarkdownIt) -> None:
    """No changes to markdown parsing are necessary."""
    ...


def _render_list(node: RenderTreeNode, context: RenderContext, bullet: str) -> str:
    """Render a `RenderTreeNode` consistent with `mkdocs`."""
    indent = " " * 4  # MkDocs requires four spaces
    rendered = ""
    with context.indented(len(indent)):  # Modifies context.env['indent_width']
        inner_indent = indent * (context.env["indent_width"] // len(indent) - 1)
        for child in node.children:
            content = child.render(context)
            # inner_items = content.split("\n")
            rendered += f"{inner_indent}{bullet} {content}\n"
            # # Process nested code blocks
            # if len(inner_items) > 1:
            #     nested_conent = textwrap.indent(
            #         "\n".join(inner_items[1:]),
            #         inner_indent + indent,
            #     )
            #     rendered += f"\n{nested_conent}\n"
    return rendered


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "bullet_list": partial(_render_list, bullet="-"),
    "ordered_list": partial(_render_list, bullet="1."),
}
