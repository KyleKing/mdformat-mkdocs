"""Material Definition Lists.

Based on
[mdformat-deflist](https://github.com/executablebooks/mdformat-deflist/blob/bbcf9ed4f80847db58b6f932ed95e2c7a6c49ae5/mdformat_deflist/plugin.py),
but modified for mkdocs-material conventions.

Example:
```md
`Lorem ipsum dolor sit amet`

:   Sed sagittis eleifend rutrum. Donec vitae suscipit est. Nullam tempus
    tellus non sem sollicitudin, quis rutrum leo facilisis.

`Cras arcu libero`

:   Aliquam metus eros, pretium sed nulla venenatis, faucibus auctor ex. Proin
    ut eros sed sapien ullamcorper consequat. Nunc ligula ante.

    Duis mollis est eget nibh volutpat, fermentum aliquet dui mollis.
    Vulputate tincidunt fringilla.
    Nullam dignissim ultrices urna non auctor.
```

Docs:
<https://squidfunk.github.io/mkdocs-material/reference/lists/#using-definition-lists>

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt
from mdit_py_plugins.deflist import deflist_plugin

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from mdformat.renderer import RenderContext, RenderTreeNode
    from mdformat.renderer.typing import Render


def material_deflist_plugin(md: MarkdownIt) -> None:
    """Add mkdocs-material definition list support to markdown-it parser."""
    md.use(deflist_plugin)


def make_render_children(separator: str) -> Render:
    """Create a renderer that joins child nodes with a separator."""

    def render_children(
        node: RenderTreeNode,
        context: RenderContext,
    ) -> str:
        return separator.join(child.render(context) for child in node.children)

    return render_children


def render_material_definition_list(
    node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Render Material Definition List."""
    return make_render_children("\n")(node, context)


def render_material_definition_term(
    node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Render Material Definition Term."""
    return make_render_children("\n")(node, context)


def render_material_definition_body(
    node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Render the definition body."""
    tight_list = all(
        child.type != "paragraph" or child.hidden for child in node.children
    )
    marker = ":   "  # FYI: increased for material
    indent_width = len(marker)
    context.env["indent_width"] += indent_width
    try:
        text = make_render_children("\n\n")(node, context)
        lines = text.splitlines()
        if not lines:
            return ":"
        indented_lines = [f"{marker}{lines[0]}"] + [
            f"{' ' * indent_width}{line}" if line else "" for line in lines[1:]
        ]
        joined_lines = ("" if tight_list else "\n") + "\n".join(indented_lines)
        next_sibling = node.next_sibling
        return joined_lines + (
            "\n" if (next_sibling and next_sibling.type == "dt") else ""
        )
    finally:
        context.env["indent_width"] -= indent_width


def escape_deflist(
    text: str,
    node: RenderTreeNode,  # noqa: ARG001
    context: RenderContext,  # noqa: ARG001
) -> str:
    """Escape line starting ":" which would otherwise be parsed as a definition list."""
    pattern = re.compile(r"^[:~] ")
    return "\n".join(
        "\\" + line if pattern.match(line) else line for line in text.split("\n")
    )
