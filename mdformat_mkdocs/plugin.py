import re
from typing import Dict, Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render

_MKDOCS_INDENT_COUNT = 4
"""Use 4-spaces for mkdocs."""

_ALIGN_SEMANTIC_BREAKS_IN_NUMBERED_LISTS = False
"""use 3-space on subsequent lines in semantic lists."""


def update_mdit(mdit: MarkdownIt) -> None:
    """No changes to markdown parsing are necessary."""
    global _ALIGN_SEMANTIC_BREAKS_IN_NUMBERED_LISTS
    # FIXME: How do I add this configuration option?
    _ALIGN_SEMANTIC_BREAKS_IN_NUMBERED_LISTS = mdit.options.get(
        "align_semantic_breaks_in_numbered_lists", True
    )


_RE_INDENT = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
"""Match `indent` and `content` against line`."""

_RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-\*\d\.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""


def _normalize_list(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """Post-processor to normalize lists."""
    eol = "\n"
    indent = " " * _MKDOCS_INDENT_COUNT

    rendered = ""
    last_indent = ""
    indent_counter = 0
    indent_lookup: Dict[str, int] = {}
    is_numbered = False
    for line in text.split(eol):
        match = _RE_INDENT.match(line)
        assert match is not None  # for pylint
        list_match = _RE_LIST_ITEM.match(match["content"])
        new_line = line
        if list_match:
            is_numbered = list_match["bullet"] not in {"-", "*"}
            new_bullet = "1." if is_numbered else "-"
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
        last_indent = this_indent
        new_indent = indent * indent_counter
        if _ALIGN_SEMANTIC_BREAKS_IN_NUMBERED_LISTS and not list_match and is_numbered:
            new_indent = new_indent[:-1]
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
