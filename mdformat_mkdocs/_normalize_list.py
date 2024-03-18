"""Normalize list indentation."""

from __future__ import annotations

import re
from contextlib import suppress
from enum import Enum
from itertools import starmap
from typing import Callable, Literal, NamedTuple, TypeVar

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
# FP Helpers

Tin = TypeVar("Tin")
Tout = TypeVar("Tout")


def map_lookback(
    func: Callable[[Tout, Tin], Tout],
    items: list[Tin],
    initial: Tout,
) -> list[Tout]:
    """Modify each item based on the result of the modification to the prior item."""
    results = [initial]
    if len(items) > 1:
        for item in items[1:]:
            result = func(results[-1], item)
            results.append(result)
    return results


# ======================================================================================
# Parsing Operations

MARKERS = CONTENT_TAB_MARKERS.union(MKDOCS_ADMON_MARKERS)
"""All block type markers."""

RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-*]|\d+\.)\s+(?P<item>.+)")
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


def parse_line(line_num: int, content: str) -> ParsedLine:
    indent, content = separate_indent(content)
    syntax = Syntax.from_content(content)
    return ParsedLine(
        line_num=line_num,
        indent=indent,
        content=content,
        syntax=syntax,
    )


def acc_line_results(parsed_lines: list[ParsedLine]) -> list[LineResult]:
    results: list[LineResult] = []
    for parsed in parsed_lines:
        parent_idx = 0
        parents = []
        with suppress(StopIteration):
            parent_idx, parent = next(
                (len(results) - idx, line)
                for idx, line in enumerate(results[::-1])
                if is_parent_line(line, parsed)
            )
            parents = [*parent.parents, parent.parsed]

        prev_list_peers = [
            line.parsed
            for line in results[parent_idx:][::-1]
            if is_peer_list_line(line, parsed)
        ]

        result = LineResult(
            parsed=parsed,
            parents=parents,
            prev_list_peers=prev_list_peers,
        )
        results.append(result)
    return results


# ======================================================================================
# Block Parsing Operations


def get_inner_indent(block_indent: BlockIndent, line_indent: str) -> str:
    """Return white space to the right of the outer indent block."""
    if block_indent.kind == "HTML":
        # PLANNED: Consider restoring some pretty indentation for HTML
        #   But the problem is that a single space is added to each line
        #       from somewhere else in mdformat that needs to be undone or
        #       accounted for
        #   This feature may require knowing when the HTML block ends
        return ""

    if (outer_indent_len := len(block_indent.raw_indent)) <= len(line_indent):
        return line_indent[outer_indent_len:]
    return block_indent.raw_indent


class BlockIndent(NamedTuple):
    """Track the parsed code block indentation."""

    raw_indent: str
    indent_depth: int
    kind: Literal["code", "HTML"]


def parse_code_block(last: BlockIndent | None, line: LineResult) -> BlockIndent | None:
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
    return result


def parse_html_line(last: BlockIndent | None, line: LineResult) -> BlockIndent | None:
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
    return result


# ======================================================================================
# High-Level Accumulators

DEFAULT_INDENT = " " * MKDOCS_INDENT_COUNT
"""Default indent."""


def format_new_indent(line: LineResult, block_indent: BlockIndent | None) -> str:
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
    return result


class ParsedText(NamedTuple):
    """Intermediary result of parsing the text."""

    lines: list[LineResult]
    new_lines: list[tuple[str, str]]
    # Used only for debugging purposes
    debug_block_indents: list[BlockIndent | None]


def format_new_content(line: LineResult, inc_numbers: bool) -> str:
    new_content = line.parsed.content
    if line.parsed.syntax in {Syntax.LIST_BULLETED, Syntax.LIST_NUMBERED}:
        list_match = RE_LIST_ITEM.fullmatch(line.parsed.content)
        assert list_match is not None  # for pyright # noqa: S101
        new_bullet = "-"
        if line.parsed.syntax == Syntax.LIST_NUMBERED:
            counter = len(line.prev_list_peers) + 1 if inc_numbers else 1
            new_bullet = f"{counter}."
        new_content = f'{new_bullet} {list_match["item"]}'

    return new_content


def parse_text(text: str, inc_numbers: bool) -> ParsedText:
    """Post-processor to normalize lists."""
    parsed_lines = list(starmap(parse_line, enumerate(text.rstrip().split(EOL))))
    lines = acc_line_results(parsed_lines)

    # `code_block_indents` take precedence to ignore contents of an HTML code block
    code_indents = map_lookback(parse_code_block, lines, None)
    html_indents = map_lookback(parse_html_line, lines, None)
    block_indents = [_c or _h for _c, _h in zip_equal(code_indents, html_indents)]
    new_indents = list(starmap(format_new_indent, zip_equal(lines, block_indents)))

    new_contents = [format_new_content(line, inc_numbers) for line in lines]
    return ParsedText(
        lines=lines,
        new_lines=[*zip_equal(new_indents, new_contents)],
        debug_block_indents=block_indents,
    )


# ======================================================================================
# Join Operations


class SemanticIndent(Enum):
    INITIAL = "Hack for MyPy and map_lookack, which returns initial..."
    EMPTY = ""
    ONE_LESS_ON_NEXT = "⤓(←)"
    ONE_LESS_SPACE = "←"
    TWO_LESS_ON_NEXT = "⤓(←←)"  # Bulleted
    TWO_LESS_SPACE = "←←"


def parse_semantic_indent(last: SemanticIndent, line: LineResult) -> SemanticIndent:
    # TODO: This works, but is very confusing
    if not line.parsed.content:
        result = SemanticIndent.EMPTY

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

    return result


def trim_semantic_indent(indent: str, s_i: SemanticIndent) -> str:
    if s_i == SemanticIndent.ONE_LESS_SPACE:
        return indent[:-1]
    if s_i == SemanticIndent.TWO_LESS_SPACE:
        return indent[:-2]
    return indent


def merge_parsed_text(parsed_text: ParsedText, use_sem_break: bool) -> str:
    new_indents, new_contents = unzip(parsed_text.new_lines)

    new_indents_iter = new_indents
    if use_sem_break:
        semantic_indents = map_lookback(
            parse_semantic_indent,
            parsed_text.lines,
            parse_semantic_indent(SemanticIndent.INITIAL, parsed_text.lines[0]),
        )
        new_indents_iter = starmap(
            trim_semantic_indent,
            zip_equal(new_indents, semantic_indents),
        )

    # Remove filler characters added by inline formatting for 'wrap'
    new_contents_iter = (
        content.replace(f"{FILLER_CHAR} ", "").replace(FILLER_CHAR, "")
        for content in new_contents
    )

    return "".join(
        f"{new_indent}{new_content}{EOL}"
        for new_indent, new_content in zip_equal(new_indents_iter, new_contents_iter)
    )


@rstrip_result
def normalize_list(
    text: str,
    node: RenderTreeNode,
    context: RenderContext,
    check_if_align_semantic_breaks_in_lists: Callable[[], bool],  # Attach with partial
) -> str:
    # FIXME: Is this filter working correctly?
    #   If it is, the test for "Formats non-root lists" should be failing
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
