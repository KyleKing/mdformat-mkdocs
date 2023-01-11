import re
from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render


def update_mdit(mdit: MarkdownIt) -> None:
    """No changes to markdown parsing are necessary."""
    ...


_RE_INDENT = re.compile(r"(?P<indent>\s*)(?P<content>.*)")
"""Match `indent` and `content` against line`."""

_RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-\*\d\.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""


def _normalize_list(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """No changes to markdown parsing are necessary."""
    eol = "\n"  # PLANNED: What about carriage returns?
    indent = " " * 4

    rendered = ""
    last_indent = ""
    indent_depth = 0
    for line in text.split(eol):
        match = _RE_INDENT.match(line)
        assert match is not None  # for pylint
        list_match = _RE_LIST_ITEM.match(match["content"])
        new_line = line
        if list_match:
            new_bullet = "-" if list_match["bullet"] in {"-", "*"} else "1."
            new_line = f'{new_bullet} {list_match["item"]}'

        indent_diff = len(match["indent"]) - len(last_indent)
        last_indent = match["indent"]
        if indent_diff > 0:
            indent_depth += 1
        elif indent_diff < 0:
            indent_depth -= 1
        new_indent = indent * indent_depth
        rendered += f"{new_indent}{new_line.strip()}{eol}"
    return rendered.rstrip()


# # A mapping from syntax tree node type to a function that renders it.
# # This can be used to overwrite renderer functions of existing syntax
# # or add support for new syntax.
RENDERERS: Mapping[str, Render] = {}
POSTPROCESSORS = {
    "bullet_list": _normalize_list,
    "ordered_list": _normalize_list,
}
