"""Copied from <https://github.com/hukkin/mdformat-gfm/blob/735781e3fcf95d92cd4537a9712893d00415cd63/src/mdformat_gfm/plugin.py>.

Will be removed when released (Workaround for https://github.com/hukkin/mdformat-gfm/issues/31)

"""

import re

import mdformat.plugins
from markdown_it import MarkdownIt
from mdformat.renderer import DEFAULT_RENDERERS, RenderContext, RenderTreeNode
from mdit_py_plugins.tasklists import tasklists_plugin

# A regex that matches a URL scheme and a following colon, as is valid in CommonMark
RE_COMMONMARK_URL_SCHEME = re.compile("[A-Za-z][A-Za-z0-9+.-]{1,31}:")


def update_mdit(mdit: MarkdownIt) -> None:
    # Enable linkify-it-py (for GFM autolink extension)
    mdit.options["linkify"] = True
    mdit.enable("linkify")

    # Enable mdformat-tables plugin
    tables_plugin = mdformat.plugins.PARSER_EXTENSIONS["tables"]
    if tables_plugin not in mdit.options["parser_extension"]:
        mdit.options["parser_extension"].append(tables_plugin)
        tables_plugin.update_mdit(mdit)

    # Enable strikethrough markdown-it extension
    mdit.enable("strikethrough")

    # Enable tasklist markdown-it extension
    mdit.use(tasklists_plugin)


def _strikethrough_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    content = "".join(child.render(context) for child in node.children)
    return f"~~{content}~~"


def _render_with_default_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    """Render the node using default renderer instead of the one in `context`.

    We don't use `RenderContext.with_default_renderer_for` because that
    changes the default renderer in context, where it's applied
    recursively to render functions of children.
    """
    syntax_type = node.type
    text = DEFAULT_RENDERERS[syntax_type](node, context)
    for postprocessor in context.postprocessors.get(syntax_type, ()):
        text = postprocessor(text, node, context)
    return text


def _is_task_list_item(node: RenderTreeNode) -> bool:
    assert node.type == "list_item"  # noqa: S101
    classes = node.attrs.get("class", "")
    assert isinstance(classes, str)  # noqa: S101
    return "task-list-item" in classes


def _list_item_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    if not _is_task_list_item(node):
        return _render_with_default_renderer(node, context)

    # Tasklists extension makes a bit weird token stream where
    # tasks are annotated by html. We need to remove the HTML.
    paragraph_node = node.children[0]
    inline_node = paragraph_node.children[0]
    assert inline_node.type == "inline"  # noqa: S101
    assert inline_node.children, "inline token must have children"  # noqa: S101
    html_inline_node = inline_node.children[0]
    assert 'class="task-list-item-checkbox"' in html_inline_node.content  # noqa: S101

    # This is naughty, shouldn't mutate and rely on `.remove` here
    inline_node.children.remove(html_inline_node)

    checkmark = "x" if 'checked="checked"' in html_inline_node.content else " "

    text = _render_with_default_renderer(node, context)

    if context.do_wrap:
        wrap_mode = context.options["mdformat"]["wrap"]
        if isinstance(wrap_mode, int):
            text = text[4:]  # Remove the "xxxx" added in `_postprocess_inline`
    # Strip leading space chars (numeric representations)
    text = re.sub(r"^(&#32;)+", "", text)
    text = text.lstrip()
    return f"[{checkmark}] {text}"


def _postprocess_inline(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """Postprocess inline tokens.

    Fix word wrap of the first line in a task list item. It should be
    wrapped narrower than normal because of the "[ ] " prefix that
    indicates a task list item. We fool word wrap by prefixing an
    unwrappable dummy string of the same length. This prefix needs to be
    later removed (in `_list_item_renderer`).
    """
    if not context.do_wrap:
        return text
    wrap_mode = context.options["mdformat"]["wrap"]
    if not isinstance(wrap_mode, int):
        return text
    if (
        node.parent  # noqa: PLR0916
        and node.parent.type == "paragraph"
        and not node.parent.previous_sibling
        and node.parent.parent
        and node.parent.parent.type == "list_item"
        and _is_task_list_item(node.parent.parent)
    ):
        text = text.lstrip("\x00")
        text = f"xxxx{text.lstrip()}"
    return text


def _link_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    """Extend the default link renderer to handle linkify links."""
    if node.markup == "linkify":
        autolink_url = node.attrs["href"]
        assert isinstance(autolink_url, str)  # noqa: S101
        startswith_scheme = RE_COMMONMARK_URL_SCHEME.match(autolink_url)
        if startswith_scheme and not node.children[0].content.startswith(
            startswith_scheme.group(),
        ):
            autolink_url = autolink_url.split(":", maxsplit=1)[1]
            if autolink_url.startswith("//"):
                autolink_url = autolink_url[2:]
        return autolink_url
    return _render_with_default_renderer(node, context)


def _escape_text(
    text: str,
    node: RenderTreeNode,  # noqa: ARG001
    context: RenderContext,  # noqa: ARG001
) -> str:
    # Escape strikethroughs
    return text.replace("~~", "\\~~")


RENDERERS = {
    "s": _strikethrough_renderer,
    "list_item": _list_item_renderer,
    "link": _link_renderer,
}
POSTPROCESSORS = {
    "text": _escape_text,
    "inline": _postprocess_inline,
}
