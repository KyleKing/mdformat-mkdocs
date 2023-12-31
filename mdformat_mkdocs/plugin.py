import argparse
import re
from typing import Dict, Mapping, Tuple

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

FILLER_CHAR = "𝕏"
"""A spacer that is inserted and then removed to ensure proper word wrap."""

FILLER = FILLER_CHAR * (_MKDOCS_INDENT_COUNT - 2)  # `mdformat` default is two spaces
"""A spacer that is inserted and then removed to ensure proper word wrap."""


def add_cli_options(parser: argparse.ArgumentParser) -> None:
    """Add options to the mdformat CLI, to be stored in `mdit.options["mdformat"]`."""
    parser.add_argument(
        "--align-semantic-breaks-in-lists",
        action="store_true",
        help="If specified, align semantic indents in numbered and bulleted lists to the text",
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """No changes to markdown parsing are necessary."""
    global _ALIGN_SEMANTIC_BREAKS_IN_LISTS
    _ALIGN_SEMANTIC_BREAKS_IN_LISTS = mdit.options["mdformat"].get(
        "align_semantic_breaks_in_lists", False
    )


_RE_INDENT = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
"""Match `indent` and `content` against line`."""

_RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-*\d.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""

_DEFAULT_INDENT = " " * _MKDOCS_INDENT_COUNT
"""Default indent."""


def _separate_indent(line: str) -> Tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite."""
    match = _RE_INDENT.match(line)
    assert match is not None  # for pylint
    return (match["indent"], match["content"])


class _MarkdownList:
    """Markdown list."""

    is_numbered = False
    is_semantic_indent = False
    is_list_match = False

    _numbered = None
    _this_indent_depth = 0

    def __init__(self, increment_number_mode: bool) -> None:
        """Store relevant 'mdformat' context."""
        self.increment_number_mode = increment_number_mode

    def _number(self) -> int:
        """Return the number."""
        if self.increment_number_mode:
            idx = self._this_indent_depth
            pad = [0] * (idx + 1)
            # FYI: on de-dent, clip previously saved _numbered
            self._numbered = [*(self._numbered or []), *pad][: (idx + 1)]
            self._numbered[idx] += 1
            return self._numbered[idx]
        return 1

    def add_bullet(self, line: str) -> str:
        """Add bullet to the line."""
        indent, content = _separate_indent(line)
        self._this_indent_depth = len(indent)
        list_match = _RE_LIST_ITEM.fullmatch(content)
        self.is_list_match = bool(list_match)
        new_line = line
        if list_match:
            self.is_numbered = list_match["bullet"] not in {"-", "*"}
            new_bullet = f"{self._number()}." if self.is_numbered else "-"
            new_line = f'{new_bullet} {list_match["item"]}'
            self.is_semantic_indent = True
        elif not new_line:
            self.is_semantic_indent = False  # on line break, use non-semantic indents
        return new_line


class _MarkdownIndent:
    """Track Markdown Indent."""

    _last_indent = ""
    _counter = 0
    _lookup: Dict[str, int] = {}
    _code_block_indent: str = ""

    def __init__(self) -> None:
        self._lookup = {}

    def _get_code_indent(self, indent: str, content: str) -> str:
        if content.startswith("```"):
            # Remove tracked indent on end of code block
            self._code_block_indent = "" if self._code_block_indent else indent
        return self._code_block_indent

    def calculate(self, line: str) -> str:
        """Calculate the new indent."""
        raw_indent, content = _separate_indent(line)
        code_indent = self._get_code_indent(raw_indent, content)
        working_indent = code_indent or raw_indent
        extra_indent = ""

        if working_indent:
            diff = len(working_indent) - len(self._last_indent)
            if not diff:
                ...
            elif diff > 0:
                self._counter += 1
                self._lookup[working_indent] = self._counter
            elif working_indent in self._lookup:
                self._counter = self._lookup[working_indent]
            else:
                raise ValueError(f"Error in list indentation at '{line}'")

            if code_indent:
                extra_indent = "".join(raw_indent[len(code_indent) :])
        else:
            self._counter = 0
        self._last_indent = working_indent

        return _DEFAULT_INDENT * self._counter + extra_indent if content else ""


def _normalize_list(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """Post-processor to normalize lists."""
    eol = "\n"

    rendered = ""
    number_mode = bool(context.options["mdformat"].get("number"))
    md_list = _MarkdownList(increment_number_mode=number_mode)
    md_indent = _MarkdownIndent()
    for line in text.split(eol):
        new_indent = md_indent.calculate(line=line)

        new_line = md_list.add_bullet(line)
        if (
            _ALIGN_SEMANTIC_BREAKS_IN_LISTS
            and not md_list.is_list_match
            and md_list.is_semantic_indent
        ):
            removed_indents = -1 if md_list.is_numbered else -2
            new_indent = new_indent[:removed_indents]

        new_line = new_line.replace(f"{FILLER_CHAR} ", "").replace(FILLER_CHAR, "")
        rendered += f"{new_indent}{new_line.strip()}{eol}"
    return rendered.rstrip()


def _postprocess_inline(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """Postprocess inline tokens.

    Fix word wrap for lists to account for the change in indentation.
    We fool word wrap by prefixing an unwrappable dummy string of the same length.
    This prefix needs to be later removed (in `_list_item_renderer`).

    Adapted from: https://github.com/hukkin/mdformat-gfm/blob/cf316a121b6cf35cbff7b0ad6e171f287803f8cb/src/mdformat_gfm/plugin.py#L86-L111

    """
    if not context.do_wrap:
        return text
    wrap_mode = context.options["mdformat"]["wrap"]
    if (
        not isinstance(wrap_mode, int)
        or FILLER_CHAR in text  # noqa: W503
        or (node.parent and node.parent.type != "paragraph")  # noqa: W503
        or (node.parent.parent and node.parent.parent.type != "list_item")  # noqa: W503
    ):
        return text

    _counter = -1
    parent = node.parent
    while parent and parent.type == "paragraph":
        parent = parent.parent
        _counter += 1
    indent_count = max(_counter, 0)

    soft_break = "\x00"
    text = text.lstrip(soft_break).lstrip()
    filler = (FILLER * indent_count)[:-1] if indent_count else ""
    newline_filler = filler + FILLER if indent_count else FILLER[:-1]
    if len(text) > wrap_mode:
        indent_length = _MKDOCS_INDENT_COUNT * indent_count
        wrapped_length = -123
        words = []
        for word in text.split(soft_break):
            next_length = wrapped_length + len(word)
            if not words:
                words = [filler, word]
                wrapped_length = indent_length + len(word)
            elif next_length > wrap_mode:
                words += [word, newline_filler]
                wrapped_length = indent_length + len(word)
            else:
                words.append(word)
                wrapped_length = next_length + 1
        return soft_break.join(_w for _w in words if _w)
    return f"{filler}{soft_break}{text}" if filler else text


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
    "inline": _postprocess_inline,
}

# See: https://github.com/executablebooks/mdformat/blob/5d9b573ce33bae219087984dd148894c774f41d4/src/mdformat/plugins.py
