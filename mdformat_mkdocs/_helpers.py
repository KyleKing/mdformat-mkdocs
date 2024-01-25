"""General Helpers."""

from __future__ import annotations

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
