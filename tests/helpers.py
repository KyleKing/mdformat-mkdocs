"""Test Helpers."""

from __future__ import annotations

import re

_SHOW_TEXT = True  # PLANNED: Make configurable based on pytest CLI


def separate_indent(line: str) -> tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite."""
    re_indent = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
    match = re_indent.match(line)
    assert match is not None  # for pyright
    return (match["indent"], match["content"])


def _print(content: str, show_whitespace: bool) -> None:
    for line in content.split("\n"):
        indent, content = separate_indent(line)
        visible_indents = indent.replace(" ", "→").replace("\t", "➤")
        print((visible_indents if show_whitespace else indent) + content)


def print_text(output: str, expected: str, show_whitespace: bool = False) -> None:
    """Conditionall print text for debugging."""
    if _SHOW_TEXT:
        print("--  Output  --")
        _print(output, show_whitespace)
        print("-- Expected --")
        _print(expected, show_whitespace)
        print("--  <End>   --")
