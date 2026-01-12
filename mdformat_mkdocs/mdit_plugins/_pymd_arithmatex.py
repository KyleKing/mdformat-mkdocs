r"""Python-Markdown Extensions: Arithmatex (Math Support).

Uses existing mdit-py-plugins for LaTeX/MathJax mathematical expressions.

Inline math delimiters:
- $...$ (with smart_dollar rules: no whitespace adjacent to $)
- \\(...\\)

Block math delimiters:
- $$...$$
- \\[...\\]
- \\begin{env}...\\end{env}

Docs: <https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex>

"""

from __future__ import annotations

import re
from textwrap import dedent
from typing import TYPE_CHECKING

from mdit_py_plugins.amsmath import amsmath_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.texmath import texmath_plugin

if TYPE_CHECKING:
    from collections.abc import Callable

    from markdown_it import MarkdownIt
    from markdown_it.rules_block import StateBlock

# Token types from the plugins
# Note: dollarmath and texmath share the same token types for inline/block math:
# - "math_inline" is used for both $...$ and \(...\)
# - "math_block" is used for both $$...$$ and \[...\]
DOLLARMATH_INLINE = "math_inline"
DOLLARMATH_BLOCK = "math_block"
DOLLARMATH_BLOCK_LABEL = "math_block_label"  # For $$...$$ (label) syntax
TEXMATH_BLOCK_EQNO = "math_block_eqno"  # For \[...\] (label) syntax
AMSMATH_BLOCK = "amsmath"

_ESCAPED_BRACKET_RE = re.compile(r"^\\\[([^\n\r]*?)\\\](\S)")
r"""Pattern to detect single-line \[...\] with content after closing bracket.

This identifies escaped brackets like \[test\]: value (not math)"""

_BACKTICK_IN_BRACKETS_RE = re.compile(r"^\\\[([^\n\r]*?`[^\n\r]*?)\\\]")
r"""Pattern to detect single-line \[...\] with backticks in content.

This identifies escaped brackets like \[`code`\] (not math), since backticks are not valid LaTeX."""

_EXPECTED_WRAPPED_RULES = 2


def _is_escaped_bracket(state: StateBlock, start_line: int) -> bool:
    r"""Check if \[...\] on this line is escaped brackets, not math.

    Returns True if line starts with \[ and:
    - \] are on same line with non-whitespace after \], OR
    - Content between \[ and \] contains backticks (inline code)

    Only checks lines starting with \[ to avoid interfering with dollar math.
    """
    pos = state.bMarks[start_line] + state.tShift[start_line]
    if pos + 2 > len(state.src):
        return False
    line_start = state.src[pos : pos + 2]
    if line_start != r"\[":
        return False
    line_content = state.src[pos:]
    return bool(
        _ESCAPED_BRACKET_RE.match(line_content)
        or _BACKTICK_IN_BRACKETS_RE.match(line_content)
    )


def pymd_arithmatex_plugin(md: MarkdownIt) -> None:
    r"""Register Arithmatex support using existing mdit-py-plugins.

    This is a convenience wrapper that configures three existing plugins:
    - dollarmath_plugin: for $...$ and $$...$$
    - texmath_plugin: for \\(...\\) and \\[...\\] (with fix for issue #72)
    - amsmath_plugin: for \\begin{env}...\\end{env}

    Raises:
        RuntimeError: If texmath rules cannot be found and wrapped.
    """
    # Dollar syntax: $...$ and $$...$$
    # Defaults provide smart dollar mode (no digits/space adjacent to $)
    md.use(dollarmath_plugin)

    # Bracket syntax: \(...\) and \[...\]
    md.use(texmath_plugin, delimiters="brackets")

    # Fix for issue #72: Wrap texmath block rules to reject \[test\]: value
    # Find the texmath rules (inserted after dollarmath's math_block)
    def make_wrapper(
        original_fn: Callable[[StateBlock, int, int, bool], bool],
    ) -> Callable[[StateBlock, int, int, bool], bool]:
        def wrapped(state: StateBlock, start: int, end: int, silent: bool) -> bool:
            if _is_escaped_bracket(state, start):
                return False
            return original_fn(state, start, end, silent)

        return wrapped

    # Wrap math_block_eqno and the second math_block (both from texmath)
    # Find them by name, skipping the first math_block (from dollarmath)
    found_first_math_block = False
    wrapped_count = 0
    for idx, rule in enumerate(md.block.ruler.__rules__):
        if rule.name == "math_block":
            if found_first_math_block:
                # This is the second math_block (from texmath)
                md.block.ruler.__rules__[idx].fn = make_wrapper(rule.fn)
                wrapped_count += 1
            else:
                found_first_math_block = True
        elif rule.name == "math_block_eqno":
            # This is from texmath
            md.block.ruler.__rules__[idx].fn = make_wrapper(rule.fn)
            wrapped_count += 1

    if wrapped_count != _EXPECTED_WRAPPED_RULES:
        msg = dedent(f"""\
            Expected to wrap {_EXPECTED_WRAPPED_RULES} texmath rules (math_block and math_block_eqno), but wrapped {wrapped_count}.
            Plugin configuration may have changed.""")
        raise RuntimeError(msg)

    # LaTeX environments: \begin{env}...\end{env}
    md.use(amsmath_plugin)
