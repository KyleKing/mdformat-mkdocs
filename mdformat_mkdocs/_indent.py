from __future__ import annotations

import functools
import re
from contextlib import suppress
from enum import Enum
from functools import partial, reduce
from typing import Callable, NamedTuple

from mdformat.renderer import RenderContext, RenderTreeNode
from more_itertools import zip_equal

from .mdit_plugins import CONTENT_TAB_MARKERS, MKDOCS_ADMON_MARKERS


def rstrip_result(func: Callable[..., str]) -> Callable[..., str]:
    """Decorator to `rstrip` the function return."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return func(*args, **kwargs).rstrip()

    return wrapper


MARKERS = CONTENT_TAB_MARKERS.union(MKDOCS_ADMON_MARKERS)
"""All block type markers."""

RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-*\d.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""

EOL = "\n"
"""Line delimiter."""

# > FILLER_CHAR = "𝕏"  # noqa: RUF003
# """A spacer that is inserted and then removed to ensure proper word wrap."""

MKDOCS_INDENT_COUNT = 4
"""Use 4-spaces for mkdocs."""

DEFAULT_INDENT = " " * MKDOCS_INDENT_COUNT
"""Default indent."""


class Syntax(Enum):
    """Non-standard line types."""

    LIST = "LIST"
    START_MARKED = "START_MARKED"
    EDGE_CODE = "EDGE_CODE"

    @classmethod
    def from_content(cls, content: str) -> Syntax | None:
        if RE_LIST_ITEM.fullmatch(content):
            return cls.LIST
        if any(content.startswith(f"{marker} ") for marker in MARKERS):
            return cls.START_MARKED
        if content.startswith("```"):
            return cls.EDGE_CODE
        return None


class ParsedLine(NamedTuple):
    """Parsed Line of text."""

    line_num: int
    indent: str
    content: str
    syntax: Syntax | None


class LineResult(NamedTuple):
    """Parsed Line of text."""

    parsed: ParsedLine
    parents: list[ParsedLine]
    prev_list_peers: list[ParsedLine]  # Only applicable for lists


def separate_indent(line: str) -> tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite."""
    re_indent = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
    match = re_indent.match(line)
    assert match is not None  # for pylint # noqa: S101
    return (match["indent"], match["content"])


def is_parent_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    return bool(prev_line.parsed.content) and len(parsed.indent) > len(
        prev_line.parsed.indent,
    )


def is_peer_list_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    return (
        len(parsed.indent) == len(prev_line.parsed.indent)
        and prev_line.parsed.syntax == Syntax.LIST
    )


def acc_parsed_lines(acc: list[ParsedLine], arg: tuple[int, str]) -> list[ParsedLine]:
    line_num, content = arg
    indent, content = separate_indent(content)
    syntax = Syntax.from_content(content)
    result = ParsedLine(
        line_num=line_num,
        indent=indent,
        content=content,
        syntax=syntax,
    )
    return [*acc, result]


def acc_line_results(acc: list[LineResult], parsed: ParsedLine) -> list[LineResult]:
    parent_idx = 0
    parents = []
    with suppress(StopIteration):
        parent_idx, parent = next(
            (len(acc) - idx, line)
            for idx, line in enumerate(acc[::-1])
            if is_parent_line(line, parsed)
        )
        parents = [*parent.parents, parent.parsed]

    prev_list_peers = (
        [
            line.parsed
            for line in acc[parent_idx:][::-1]
            if is_peer_list_line(line, parsed)
        ]
        if parsed.syntax == Syntax.LIST
        else []
    )

    result = LineResult(parsed=parsed, parents=parents, prev_list_peers=prev_list_peers)
    return [*acc, result]


def get_inner_indent(block_indent: BlockIndent, line_indent: str) -> str:
    """Return white space to the right of the outer indent block."""
    outer_indent_len = len(block_indent.raw_indent)
    if outer_indent_len > len(line_indent):
        return block_indent.raw_indent
    return "".join(line_indent[outer_indent_len:])


class BlockIndent(NamedTuple):
    """Track the parsed code block indentation."""

    raw_indent: str
    indent_depth: int


def acc_code_block_indents(
    acc: list[BlockIndent | None],
    line: LineResult,
) -> list[BlockIndent | None]:
    last = (acc or [None])[-1]
    result = last
    if line.parsed.syntax == Syntax.EDGE_CODE:
        # On first edge, start tracking a code block
        #   on the second edge, stop tracking
        new_block = BlockIndent(
            raw_indent=line.parsed.indent,
            indent_depth=len(line.parents),
        )
        result = None if last else new_block

    return [*acc, result]


def acc_new_indents(
    acc: list[str],
    arg: tuple[LineResult, BlockIndent | None],
) -> list[str]:
    line, block_indent = arg

    result = ""
    if line.parsed.content:
        if block_indent:
            depth = block_indent.indent_depth
            extra_indent = get_inner_indent(
                block_indent=block_indent,
                line_indent=line.parsed.indent,
            )
            result = DEFAULT_INDENT * depth + extra_indent
        else:
            result = DEFAULT_INDENT * len(line.parents)

    return [*acc, result]


class ParsedText(NamedTuple):
    """Intermediary result of parsing the text."""

    new_lines: list[tuple[str, str]]
    # Used only for debugging purposes
    lines: list[LineResult]
    block_indents: list[BlockIndent | None]


def acc_new_contents(acc: list[str], line: LineResult, inc_numbers: bool) -> list[str]:
    new_content = line.parsed.content
    if list_match := RE_LIST_ITEM.fullmatch(line.parsed.content):
        new_bullet = "-"
        if list_match["bullet"] not in {"-", "*"}:
            new_bullet = f"{len(line.prev_list_peers) + 1 if inc_numbers else 1}."
        new_content = f'{new_bullet} {list_match["item"]}'

    return [*acc, new_content]


def parse_text(text: str, inc_numbers: bool) -> ParsedText:
    """Post-processor to normalize lists."""
    parsed_lines = reduce(acc_parsed_lines, enumerate(text.rstrip().split(EOL)), [])
    lines = reduce(acc_line_results, parsed_lines, [])

    code_block_indents = reduce(acc_code_block_indents, lines, [])
    new_indents = reduce(acc_new_indents, zip_equal(lines, code_block_indents), [])

    new_contents = reduce(
        partial(acc_new_contents, inc_numbers=inc_numbers),
        lines,
        [],
    )
    return ParsedText(
        new_lines=[*zip_equal(new_indents, new_contents)],
        lines=lines,
        block_indents=code_block_indents,
    )


def merge_parsed_text(parsed_text: ParsedText, use_sem_break: bool) -> str:
    if use_sem_break:
        raise NotImplementedError("Pending text wrap implementation")

    # PLANNED: Need a flat_map (`collapse` in more-itertools) to handle semantic indents
    return "".join(
        f"{new_indent}{new_content}{EOL}"
        for new_indent, new_content in parsed_text.new_lines
    )


@rstrip_result
def normalize_list(
    text: str,
    node: RenderTreeNode,
    context: RenderContext,
    check_if_align_semantic_breaks_in_lists: Callable[[], bool],  # Attach with partial
) -> str:
    # FIXME: should only skip if root of this node is a list!
    if node.level > 1:
        # Note: this function is called recursively,
        #   so only process the top-level item
        return text

    # Retrieve user-options
    inc_numbers = bool(context.options["mdformat"].get("number"))

    parsed_text = parse_text(text=text, inc_numbers=inc_numbers)

    return merge_parsed_text(
        parsed_text=parsed_text,
        use_sem_break=check_if_align_semantic_breaks_in_lists(),
    )
