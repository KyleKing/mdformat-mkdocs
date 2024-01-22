from __future__ import annotations

import re
from contextlib import suppress
from enum import Enum
from functools import partial, reduce
from typing import Callable, NamedTuple

from mdformat.renderer import RenderContext, RenderTreeNode
from more_itertools import zip_equal

from .mdit_plugins import CONTENT_TAB_MARKERS, MKDOCS_ADMON_MARKERS

MARKERS = CONTENT_TAB_MARKERS.union(MKDOCS_ADMON_MARKERS)
"""All block type markers."""

RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-*\d.]+)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""

FILLER_CHAR = "𝕏"  # noqa: RUF001
"""A spacer that is inserted and then removed to ensure proper word wrap."""

MKDOCS_INDENT_COUNT = 4
"""Use 4-spaces for mkdocs."""

DEFAULT_INDENT = " " * MKDOCS_INDENT_COUNT
"""Default indent."""


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
    prev_peers: list[ParsedLine]


def separate_indent(line: str) -> tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite."""
    re_indent = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
    match = re_indent.match(line)
    assert match is not None  # for pylint # noqa: S101
    return (match["indent"], match["content"])


def is_parent_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    return len(parsed.indent) > len(prev_line.parsed.indent)


def is_peer_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    return len(parsed.indent) == len(prev_line.parsed.indent)


def acc_parsed_lines(acc: list[LineResult], content: str) -> list[LineResult]:
    indent, content = separate_indent(content)
    syntax = Syntax.from_content(content)
    parsed = ParsedLine(indent=indent, content=content, syntax=syntax)

    parent_idx = 0
    parents = []
    with suppress(StopIteration):
        parent_idx, parent = next(
            (idx, line)
            for idx, line in enumerate(acc[::-1])
            if is_parent_line(line, parsed)
        )
        parents = [*parent.parents, parent.parsed]
    prev_peers = [line for line in acc[parent_idx:][::-1] if is_peer_line(line, parsed)]

    result = LineResult(parsed=parsed, parents=parents, prev_peers=prev_peers)
    return [*acc, result]


def acc_code_block_indents(acc: list[str | None], line: LineResult) -> list[str | None]:
    last = (acc or [None])[-1]
    result = last
    if line.parsed.syntax == Syntax.EDGE_CODE:
        result = None if last else line.parsed.indent
    return [*acc, result]


def acc_new_indents(
    acc: list[str],
    arg: tuple[LineResult, str | None],
    use_sem_break: bool,  # Attach with partial
) -> list[str]:
    if use_sem_break:
        raise NotImplementedError("Pending implementation!")

    line, code_block_indent = arg

    raw_indent = line.parsed.indent
    indent_depth = len(line.parents)
    extra_indent = (
        "".join(raw_indent[len(code_block_indent) :]) if code_block_indent else ""
    )

    result = DEFAULT_INDENT * indent_depth + extra_indent if line.parsed.content else ""

    return [*acc, result]


class ParsedText(NamedTuple):
    """Intermediary result of parsing the text."""

    new_indents: list[str]
    new_contents: list[str]
    # Used only for debugging purposes
    lines: list[dict]
    code_block_indents: list[str | None]


def acc_new_contents(acc: list[str], line: LineResult, inc_numbers: bool) -> list[str]:
    new_content = line.parsed.content
    if list_match := RE_LIST_ITEM.fullmatch(line.parsed.content):
        new_bullet = "-"
        if list_match["bullet"] not in {"-", "*"}:
            new_bullet = f"{len(line.prev_peers) + 1 if inc_numbers else 1}."
        new_content = f'{new_bullet} {list_match["item"]}'

    return [*acc, new_content]


def process_text(
    text: str,
    eol: str,
    inc_numbers: bool,
    use_sem_break: bool,
) -> ParsedText:
    """Post-processor to normalize lists."""
    lines = reduce(acc_parsed_lines, text.rstrip().split(eol), [])

    code_block_indents = reduce(acc_code_block_indents, lines, [])
    new_indents = reduce(
        partial(acc_new_indents, use_sem_break=use_sem_break),
        zip_equal(lines, code_block_indents),
        [],
    )

    new_contents = reduce(partial(acc_new_contents, inc_numbers=inc_numbers), lines, [])
    return ParsedText(
        new_indents=new_indents,
        new_contents=new_contents,
        lines=[line._asdict() for line in lines],
        code_block_indents=code_block_indents,
    )


def normalize_list(
    text: str,
    node: RenderTreeNode,  # noqa: ARG001
    context: RenderContext,
    check_if_align_semantic_breaks_in_lists: Callable[[], bool],  # Attach with partial
) -> str:
    # Retrieve user-options
    inc_numbers = bool(context.options["mdformat"].get("number"))

    eol = "\n"
    parsed_text = process_text(
        text=text,
        eol="\n",
        inc_numbers=inc_numbers,
        use_sem_break=check_if_align_semantic_breaks_in_lists(),
    )

    return "".join(
        f"{new_indent}{new_content}{eol}"
        for new_indent, new_content in zip_equal(
            parsed_text.new_indents,
            parsed_text.new_contents,
        )
    )
