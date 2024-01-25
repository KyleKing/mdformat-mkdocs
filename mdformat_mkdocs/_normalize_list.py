"""Normalize list indentation."""

from __future__ import annotations

import re
from contextlib import suppress
from enum import Enum
from functools import partial, reduce
from typing import Callable, Literal, NamedTuple

from mdformat.renderer import RenderContext, RenderTreeNode
from more_itertools import unzip, zip_equal

from ._helpers import (
    EOL,
    FILLER_CHAR,
    MKDOCS_INDENT_COUNT,
    rstrip_result,
    separate_indent,
)
from .mdit_plugins import CONTENT_TAB_MARKERS, MKDOCS_ADMON_MARKERS

# ======================================================================================
# Parsing Operations

MARKERS = CONTENT_TAB_MARKERS.union(MKDOCS_ADMON_MARKERS)
"""All block type markers."""

RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-*\d.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""


class Syntax(Enum):
    """Non-standard line types."""

    LIST_BULLETED = "LIST_BULLETED"
    LIST_NUMBERED = "LIST_NUMBERED"
    START_MARKED = "START_MARKED"
    EDGE_CODE = "EDGE_CODE"
    HTML = "HTML"

    @classmethod
    def from_content(cls, content: str) -> Syntax | None:
        if match := RE_LIST_ITEM.fullmatch(content):
            return (
                cls.LIST_NUMBERED
                if match["bullet"] not in {"-", "*"}
                else cls.LIST_BULLETED
            )
        if any(content.startswith(f"{marker} ") for marker in MARKERS):
            return cls.START_MARKED
        if content.startswith("```"):
            return cls.EDGE_CODE
        if content.startswith("<"):
            return cls.HTML
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


def is_parent_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    return bool(prev_line.parsed.content) and len(parsed.indent) > len(
        prev_line.parsed.indent,
    )


def is_peer_list_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    list_types = {Syntax.LIST_BULLETED, Syntax.LIST_NUMBERED}
    return (
        parsed.syntax in list_types
        and prev_line.parsed.syntax in list_types
        and len(parsed.indent) == len(prev_line.parsed.indent)
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

    prev_list_peers = [
        line.parsed
        for line in acc[parent_idx:][::-1]
        if is_peer_list_line(line, parsed)
    ]

    result = LineResult(parsed=parsed, parents=parents, prev_list_peers=prev_list_peers)
    return [*acc, result]


# ======================================================================================
# Block Parsing Operations


def get_inner_indent(block_indent: BlockIndent, line_indent: str) -> str:
    """Return white space to the right of the outer indent block."""
    if block_indent.kind == "HTML":
        return ""

    outer_indent_len = len(block_indent.raw_indent)
    if outer_indent_len > len(line_indent):
        return block_indent.raw_indent
    return line_indent[outer_indent_len:]


class BlockIndent(NamedTuple):
    """Track the parsed code block indentation."""

    raw_indent: str
    indent_depth: int
    kind: Literal["code", "HTML"]


def acc_code_block_indents(
    acc: list[BlockIndent | None],
    line: LineResult,
) -> list[BlockIndent | None]:
    last = (acc or [None])[-1]
    result = last
    if line.parsed.syntax == Syntax.EDGE_CODE:
        # On first edge, start tracking a code block
        #   on the second edge, stop tracking
        result = (
            None
            if last
            else BlockIndent(
                raw_indent=line.parsed.indent,
                indent_depth=len(line.parents),
                kind="code",
            )
        )
    return [*acc, result]


def acc_html_blocks(
    acc: list[BlockIndent | None],
    line: LineResult,
) -> list[BlockIndent | None]:
    last = (acc or [None])[-1]
    result = last
    if line.parsed.syntax == Syntax.HTML:
        # Start tracking an HTML block if not already
        result = last or BlockIndent(
            raw_indent=line.parsed.indent,
            indent_depth=len(line.parents),
            kind="HTML",
        )
    elif last and not line.parsed.content:
        # Stop tracking an HTML block on a line break
        result = None
    return [*acc, result]


# ======================================================================================
# High-Level Accumulators

DEFAULT_INDENT = " " * MKDOCS_INDENT_COUNT
"""Default indent."""


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

    lines: list[LineResult]
    new_lines: list[tuple[str, str]]
    # Used only for debugging purposes
    debug_block_indents: list[BlockIndent | None]


def acc_new_contents(acc: list[str], line: LineResult, inc_numbers: bool) -> list[str]:
    new_content = line.parsed.content
    if line.parsed.syntax in {Syntax.LIST_BULLETED, Syntax.LIST_NUMBERED}:
        list_match = RE_LIST_ITEM.fullmatch(line.parsed.content)
        assert list_match is not None  # for pyright # noqa: S101
        new_bullet = "-"
        if line.parsed.syntax == Syntax.LIST_NUMBERED:
            counter = len(line.prev_list_peers) + 1 if inc_numbers else 1
            new_bullet = f"{counter}."
        new_content = f'{new_bullet} {list_match["item"]}'

    return [*acc, new_content]


def parse_text(text: str, inc_numbers: bool) -> ParsedText:
    """Post-processor to normalize lists."""
    parsed_lines = reduce(acc_parsed_lines, enumerate(text.rstrip().split(EOL)), [])
    lines = reduce(acc_line_results, parsed_lines, [])

    # `code_block_indents` take precedence to ignore contents of an HTML code block
    code_indents = reduce(acc_code_block_indents, lines, [])
    html_indents = reduce(acc_html_blocks, lines, [])
    block_indents = [_c or _h for _c, _h in zip_equal(code_indents, html_indents)]
    new_indents = reduce(acc_new_indents, zip_equal(lines, block_indents), [])

    new_contents = reduce(
        partial(acc_new_contents, inc_numbers=inc_numbers),
        lines,
        [],
    )
    return ParsedText(
        lines=lines,
        new_lines=[*zip_equal(new_indents, new_contents)],
        debug_block_indents=block_indents,
    )


# ======================================================================================
# Join Operations


class SemanticIndent(Enum):
    NONE = ""
    ONE_LESS_ON_NEXT = "⤓(←)"
    ONE_LESS_SPACE = "←"
    TWO_LESS_ON_NEXT = "⤓(←←)"  # Bulleted
    TWO_LESS_SPACE = "←←"


def acc_semantic_indents(
    acc: list[SemanticIndent],
    line: LineResult,
) -> list[SemanticIndent]:
    last = (acc or [SemanticIndent.NONE])[-1]

    if not line.parsed.content:
        result = SemanticIndent.NONE

    elif line.parsed.syntax == Syntax.LIST_BULLETED:
        result = SemanticIndent.TWO_LESS_ON_NEXT
    elif line.parsed.syntax == Syntax.LIST_NUMBERED:
        result = SemanticIndent.ONE_LESS_ON_NEXT

    elif last == SemanticIndent.TWO_LESS_ON_NEXT:
        result = SemanticIndent.TWO_LESS_SPACE
    elif last == SemanticIndent.ONE_LESS_ON_NEXT:
        result = SemanticIndent.ONE_LESS_SPACE
    else:
        result = last

    return [*acc, result]


def trim_semantic_indent(indent: str, s_i: SemanticIndent) -> str:
    if s_i == SemanticIndent.ONE_LESS_SPACE:
        return indent[:-1]
    if s_i == SemanticIndent.TWO_LESS_SPACE:
        return indent[:-2]
    return indent


def merge_parsed_text(parsed_text: ParsedText, use_sem_break: bool) -> str:
    new_indents, new_contents = unzip(parsed_text.new_lines)

    if use_sem_break:
        new_indents = [
            trim_semantic_indent(indent, s_i)
            for s_i, indent in zip_equal(
                reduce(acc_semantic_indents, parsed_text.lines, []),
                new_indents,
            )
        ]

    # Remove filler characters added by inline formatting for 'wrap'
    new_contents = [
        content.replace(f"{FILLER_CHAR} ", "").replace(FILLER_CHAR, "")
        for content in new_contents
    ]

    return "".join(
        f"{new_indent}{new_content}{EOL}"
        for new_indent, new_content in zip_equal(new_indents, new_contents)
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
