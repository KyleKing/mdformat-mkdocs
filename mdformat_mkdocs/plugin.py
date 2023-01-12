import re
from typing import Dict, Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render

_MKDOCS_INDENT_COUNT = 4
"""Use 4-spaces for mkdocs."""


def update_mdit(mdit: MarkdownIt) -> None:
    """No changes to markdown parsing are necessary."""
    ...


_RE_INDENT = re.compile(r"(?P<indent>\s*)(?P<content>.*)")
"""Match `indent` and `content` against line`."""

_RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-\*\d\.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""


def _normalize_list(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """Post-processor to normalize lists."""
    eol = "\n"  # PLANNED: Does this need to support carriage returns?
    indent = " " * _MKDOCS_INDENT_COUNT

    rendered = ""
    last_indent = ""
    indent_counter = 0
    indent_lookup: Dict[str, int] = {}
    for line in text.split(eol):
        match = _RE_INDENT.match(line)
        assert match is not None  # for pylint
        list_match = _RE_LIST_ITEM.match(match["content"])
        new_line = line
        if list_match:
            new_bullet = "-" if list_match["bullet"] in {"-", "*"} else "1."
            new_line = f'{new_bullet} {list_match["item"]}'

        this_indent = match["indent"]
        if this_indent:
            indent_diff = len(this_indent) - len(last_indent)
            if indent_diff == 0:
                ...
            elif indent_diff > 0:
                indent_counter += 1
                indent_lookup[this_indent] = indent_counter
            elif this_indent in indent_lookup:
                indent_counter = indent_lookup[this_indent]
            else:
                raise NotImplementedError(f"Error in indentation of: `{line}`")
        else:
            indent_counter = 0
        last_indent = match["indent"]
        new_indent = indent * indent_counter
        rendered += f"{new_indent}{new_line.strip()}{eol}"
    return rendered.rstrip()


# A mapping from `RenderTreeNode.type` to a `Render` function that can
# render the given `RenderTreeNode` type. These override the default
# `Render` funcs defined in `mdformat.renderer.DEFAULT_RENDERERS`.
RENDERERS: Mapping[str, Render] = {}

# A mapping from `RenderTreeNode.type` to a `Postprocess` that does
# postprocessing for the output of the `Render` function. Unlike
# `Render` funcs, `Postprocess` funcs are collaborative: any number of
# plugins can define a postprocessor for a syntax type and all of them
# will run in series.
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "bullet_list": _normalize_list,
    "ordered_list": _normalize_list,
}

# See: https://github.com/executablebooks/mdformat/blob/5d9b573ce33bae219087984dd148894c774f41d4/src/mdformat/plugins.py
