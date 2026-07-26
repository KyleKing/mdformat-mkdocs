"""Test Helpers."""

from __future__ import annotations

import re

_SHOW_TEXT = True


def separate_indent(line: str) -> tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite.

    Returns:
        tuple[str, str]: pair of indent and content

    """
    re_indent = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
    match = re_indent.match(line)
    assert match is not None  # for pyright
    return (match["indent"], match["content"])


def _print(content: str, show_whitespace: bool) -> None:
    for line in content.split("\n"):
        indent, content = separate_indent(line)
        visible_indents = indent.replace(" ", "→").replace("\t", "➤")
        print((visible_indents if show_whitespace else indent) + content)  # ruff:ignore[print]


def print_text(output: str, expected: str, show_whitespace: bool = False) -> None:  # ruff:ignore[boolean-default-value-positional-argument]
    """Conditional print text for debugging."""
    if _SHOW_TEXT:
        print("--  Output  --")  # ruff:ignore[print]
        _print(output, show_whitespace)
        print("-- Expected --")  # ruff:ignore[print]
        _print(expected, show_whitespace)
        print("--  <End>   --")  # ruff:ignore[print]
