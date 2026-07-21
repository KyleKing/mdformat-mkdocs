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


def _is_ambiguous_same_line_close(state: StateBlock, start_line: int) -> bool:
    r"""True if the line opens `$$`, closes it, then has trailing content.

    e.g. `$$b$$ trailing`: dollarmath's block rule only recognizes a
    same-line close when the closing `$$` is the last thing on the line.
    With trailing text present, it instead scans forward for the *next*
    `$$` anywhere in the document, silently swallowing everything in
    between (including subsequent list items) as literal math content.
    """
    pos = state.bMarks[start_line] + state.tShift[start_line]
    end = state.eMarks[start_line]
    stripped = state.src[pos:end].strip()
    return (
        stripped.startswith("$$")
        and "$$" in stripped[2:]
        and not stripped.endswith("$$")
    )


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


def _guard_dollarmath_same_line_close(
    md: MarkdownIt, before_dollarmath: set[int]
) -> None:
    """Wrap dollarmath's own `math_block` rule against the same-line-close bug.

    e.g. `$$b$$ trailing` otherwise swallows subsequent content as literal
    math text. Identified by id, since texmath registers a rule with the
    same name ("math_block") later in `pymd_arithmatex_plugin`.

    TODO: a fix has been proposed upstream in `mdit-py-plugins` (drafted in
    `mdformat-obsidian`'s UPSTREAM_MDIT_PY_PLUGINS_FIX.md) that would make
    this guard unnecessary. Once a released `mdit-py-plugins` includes it,
    bump the version floor in pyproject.toml, run the test suite, and if
    `tests/test_arithmatex_plugin_compat.py::test_same_line_close_with_trailing_text_does_not_swallow_list_items`
    still passes, delete this function and its call site below.
    """
    for rule in md.block.ruler.__rules__:
        if id(rule) not in before_dollarmath and rule.name == DOLLARMATH_BLOCK:
            original_fn = rule.fn

            def guarded(
                state: StateBlock,
                start: int,
                end: int,
                silent: bool,
                _original_fn: Callable[
                    [StateBlock, int, int, bool], bool
                ] = original_fn,
            ) -> bool:
                if _is_ambiguous_same_line_close(state, start):
                    return False
                return _original_fn(state, start, end, silent)

            rule.fn = guarded


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
    before_dollarmath = {id(rule) for rule in md.block.ruler.__rules__}
    md.use(dollarmath_plugin)
    _guard_dollarmath_same_line_close(md, before_dollarmath)

    # Bracket syntax: \(...\) and \[...\]
    # Snapshot existing rules so we only wrap the ones texmath adds here. Other
    # plugins (e.g. mdformat-myst) may already have registered math_block rules,
    # so identifying texmath's rules by position is unreliable (issue #90).
    before = {id(rule) for rule in md.block.ruler.__rules__}
    md.use(texmath_plugin, delimiters="brackets")

    # Fix for issue #72: Wrap texmath block rules to reject \[test\]: value
    def make_wrapper(
        original_fn: Callable[[StateBlock, int, int, bool], bool],
    ) -> Callable[[StateBlock, int, int, bool], bool]:
        def wrapped(state: StateBlock, start: int, end: int, silent: bool) -> bool:
            if _is_escaped_bracket(state, start):
                return False
            return original_fn(state, start, end, silent)

        return wrapped

    wrapped_count = 0
    for rule in md.block.ruler.__rules__:
        if id(rule) not in before and rule.name in {
            DOLLARMATH_BLOCK,
            TEXMATH_BLOCK_EQNO,
        }:
            rule.fn = make_wrapper(rule.fn)
            wrapped_count += 1

    if wrapped_count != _EXPECTED_WRAPPED_RULES:
        msg = dedent(f"""\
            Expected to wrap {_EXPECTED_WRAPPED_RULES} texmath rules (math_block and math_block_eqno), but wrapped {wrapped_count}.
            Plugin configuration may have changed.""")
        raise RuntimeError(msg)

    # LaTeX environments: \begin{env}...\end{env}
    md.use(amsmath_plugin)
