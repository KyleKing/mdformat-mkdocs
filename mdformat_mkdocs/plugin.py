import argparse
from contextlib import suppress
import re
import textwrap
from typing import Dict, Mapping, Optional

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render

_MKDOCS_INDENT_COUNT = 4
"""Use 4-spaces for mkdocs."""

_ALIGN_SEMANTIC_BREAKS_IN_LISTS = False
"""user-specified flag for toggling semantic breaks.

- 3-spaces on subsequent lines in semantic numbered lists
- and 2-spaces on subsequent bulleted items

"""

_MDFORMAT_WRAP: Optional[int] = None
"""Paragraph word wrap mode (`{keep,no,INTEGER}`, default: `keep`)."""


def add_cli_options(parser: argparse.ArgumentParser) -> None:
    """Add options to the mdformat CLI, to be stored in `mdit.options["mdformat"]`."""
    parser.add_argument(
        "--align-semantic-breaks-in-lists",
        action="store_true",
        help="If specified, align semantic indents in numbered and bulleted lists to the text",
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """No changes to markdown parsing are necessary."""
    global _ALIGN_SEMANTIC_BREAKS_IN_LISTS, _MDFORMAT_WRAP

    _ALIGN_SEMANTIC_BREAKS_IN_LISTS = mdit.options["mdformat"].get(
        "align_semantic_breaks_in_lists", False
    )

    _wrap = mdit.options["mdformat"].get("wrap") or ""
    with suppress(ValueError):
        _MDFORMAT_WRAP = int(_wrap)


_RE_INDENT = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
"""Match `indent` and `content` against line`."""

_RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-\*\d\.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""


def _wrap_text(text: str, *, width: int) -> str:
    """Wrap text.

    Adapted from: https://github.com/executablebooks/mdformat/blob/0cbd2054dedf98ec8366001c8a16eacfa85cebc1/src/mdformat/renderer/_context.py#L320C1-L340C62

    """
    wrapper = textwrap.TextWrapper(
        break_long_words=False,
        break_on_hyphens=False,
        width=width,
        expand_tabs=False,
        replace_whitespace=False,
    )
    return wrapper.fill(text)


def _normalize_list(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """Post-processor to normalize lists."""
    eol = "\n"
    indent = " " * _MKDOCS_INDENT_COUNT

    rendered = ""
    last_indent = ""
    new_indent = ""
    last_wrapped_text = ""
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
            if not indent_diff:
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
        if _ALIGN_SEMANTIC_BREAKS_IN_LISTS and not list_match:
            removed_indents = -1 if is_numbered else -2
            new_indent = new_indent[:removed_indents]

        new_text = f"{new_indent}{new_line.strip()}"
        if _MDFORMAT_WRAP and len(new_text) > _MDFORMAT_WRAP:
            wrapped_text = _wrap_text(text=new_text, width=_MDFORMAT_WRAP)
            new_text, *extra = wrapped_text.split("\n")
            last_wrapped_text = "".join(extra)
        rendered += f"{new_text}{eol}"
        if last_wrapped_text:
            rendered += f"{new_indent}{last_wrapped_text}{eol}"
            last_wrapped_text = ""
    if last_wrapped_text:
        rendered += f"{new_indent}{last_wrapped_text}{eol}"
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
