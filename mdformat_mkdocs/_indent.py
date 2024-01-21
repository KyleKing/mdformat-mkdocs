from __future__ import annotations

import re
from contextlib import suppress
from enum import Enum
from functools import partial, reduce
from typing import Callable, NamedTuple

from mdformat.renderer import RenderContext, RenderTreeNode

from .mdit_plugins import CONTENT_TAB_MARKERS, MKDOCS_ADMON_MARKERS

MARKERS = CONTENT_TAB_MARKERS.union(MKDOCS_ADMON_MARKERS)
"""All block type markers."""

RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-*\d.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""

FILLER_CHAR = "𝕏"  # noqa: RUF001
"""A spacer that is inserted and then removed to ensure proper word wrap."""


class Syntax(Enum):
    """Non-standard line types."""

    LIST = "LIST"
    START_MARKED = "START_MARKED"
    EDGE_CODE = "EDGE_CODE"
    HTML = "HTML"

    @classmethod
    def from_content(cls, content: str) -> Syntax | None:
        if RE_LIST_ITEM.fullmatch(content):
            return cls.LIST
        if any(content.startswith(f"{marker} ") for marker in MARKERS):
            return cls.START_MARKED
        if content.startswith("```"):
            return cls.EDGE_CODE
        if content.startswith("<"):
            # TODO: Figure out how to handle "markdown in HTML" (like figcaption)
            return cls.HTML
        return None


class ParsedLine(NamedTuple):
    """Parsed Line of text."""

    indent: str
    content: str
    syntax: Syntax | None


class LineResult(NamedTuple):
    """Parsed Line of text."""

    parsed: ParsedLine
    parents: list[ParsedLine]


def separate_indent(line: str) -> tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite."""
    re_indent = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
    match = re_indent.match(line)
    assert match is not None  # for pylint # noqa: S101
    return (match["indent"], match["content"])


def is_parent(line: LineResult, parsed: ParsedLine) -> bool:
    return len(parsed.indent) < len(line.parsed.indent)


def acc_parsed_lines(acc: list[LineResult], content: str) -> list[LineResult]:
    indent, content = separate_indent(content)
    syntax = Syntax.from_content(content)
    parsed = ParsedLine(indent=indent, content=content, syntax=syntax)

    parents = []
    with suppress(StopIteration):
        parent = next(line for line in acc if is_parent(line, parsed))
        parents = [*parent.parents, parent.parsed]
    result = LineResult(parsed=parsed, parents=parents)
    return [*acc, result]


def acc_code_blocks(
    acc: list[LineResult | None],
    line: LineResult,
) -> list[LineResult | None]:
    last = (acc or [None])[-1]
    result = last
    if line.parsed.syntax == Syntax.EDGE_CODE:
        result = None if last else line
    return [*acc, result]


def acc_new_indents(
    acc: list[str],
    arg: tuple[LineResult, LineResult | None, LineResult | None],
    use_sem_break: bool,  # Attach with partial
) -> list[str]:
    line, prev_line, code_block = arg
    result = line.parsed.indent
    # FIXME: Calculate indents using additional arguments!
    # TODO: Adjust white space when within a code block based on parent EDGE block
    # ??
    #   indent = indent.replace(f"{FILLER_CHAR} ", "").replace(FILLER_CHAR, "")
    return [*acc, result]


def acc_new_contents(
    acc: list[str],
    arg: tuple[LineResult, str | None],
) -> list[str]:
    line, bullet = arg
    result = line.parsed.content
    # FIXME: MOdify 'content' if 'bullet' is not None!
    return [*acc, result]


def normalize_list(
    text: str,
    node: RenderTreeNode,  # noqa: ARG001
    context: RenderContext,
    check_if_align_semantic_breaks_in_lists: Callable[[], bool],  # Attach with partial
) -> str:
    """Post-processor to normalize lists."""
    # Retrieve user-options
    number_mode = bool(context.options["mdformat"].get("number"))

    eol = "\n"
    lines = reduce(acc_parsed_lines, text.split(eol), [])

    # md_list = _MarkdownList(increment_number_mode=number_mode)
    # md_indent = _MarkdownIndent()
    # for line in lines:
    #     new_indent = md_indent.calculate(line=line)

    #     new_line = md_list.add_bullet(line)
    #     if (
    #         _ALIGN_SEMANTIC_BREAKS_IN_LISTS
    #         and not md_list.is_list_match
    #         and md_list.is_semantic_indent
    #     ):
    #         removed_indents = -1 if md_list.is_numbered else -2
    #         new_indent = new_indent[:removed_indents]

    prev_lines = [None, *lines][: len(lines)]
    code_blocks = reduce(acc_code_blocks, lines, [])
    new_indents = reduce(
        partial(
            acc_new_indents,
            use_sem_break=check_if_align_semantic_breaks_in_lists(),
        ),
        zip(lines, prev_lines, code_blocks),
        [],
    )

    # TODO: Assign bullet of `1. #. or -` based on sequence in LIST and settings
    bullets: list[str | None] = ["" for _l in lines]
    new_contents = reduce(acc_new_contents, zip(lines, bullets), [])

    return "".join(
        f"{new_indent}{new_content}{eol}"
        for new_indent, new_content in zip(new_indents, new_contents)
    )
