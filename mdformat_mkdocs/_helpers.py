"""General Helpers."""

from __future__ import annotations

import re
from functools import wraps
from typing import Callable

EOL = "\n"
"""Line delimiter."""

MKDOCS_INDENT_COUNT = 4
"""Use 4-spaces for mkdocs."""

FILLER_CHAR = "𝕏"  # noqa: RUF001
"""A spacer that is inserted and then removed to ensure proper word wrap."""


def rstrip_result(func: Callable[..., str]) -> Callable[..., str]:
    """Right-strip the decorated function's result.

    Returns:
        Callable[..., str]: decorator

    """

    @wraps(func)
    def _wrapper(*args, **kwargs) -> str:
        return func(*args, **kwargs).rstrip()

    return _wrapper


def separate_indent(line: str) -> tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite.

    Returns:
        tuple[str, str]: separate indent and content

    """
    re_indent = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
    match = re_indent.match(line)
    assert match  # for pyright
    return (match["indent"], match["content"])
