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
    """Decorator to `rstrip` the function return."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return func(*args, **kwargs).rstrip()

    return wrapper


def separate_indent(line: str) -> tuple[str, str]:
    """Separate leading indent from content. Also used by the test suite."""
    re_indent = re.compile(r"(?P<indent>\s*)(?P<content>[^\s]?.*)")
    match = re_indent.match(line)
    assert match is not None  # for pyright # noqa: S101
    return (match["indent"], match["content"])
