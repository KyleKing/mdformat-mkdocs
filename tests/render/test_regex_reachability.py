"""AST reachability check: every plugin regex must be reached by a render fixture.

The behavioral guard in `test_security.py` amplifies the render fixtures, but a
regex anchored past a lead-in that no fixture produces (e.g. ``^```math``) is never
reached, and the miss is silent. This test closes that gap: it statically extracts
every regex literal from the plugin package, reconstructs each pattern's leading
literal, and asserts that at least one fixture-derived payload contains it.

See `SECURITY_GUARD.md` for how this fits alongside the fixture-derived ReDoS/XSS
guard and the optional Hypothesis deep-fuzz.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from markdown_it.utils import read_fixture_file

PACKAGE = Path(__file__).parents[2] / "mdformat_mkdocs"
FIXTURE_PATH = Path(__file__).parent / "fixtures"

_RE_FUNCS = {"compile", "match", "search", "fullmatch", "findall", "finditer", "sub"}
# Metacharacters that end the run of leading literal characters.
_METACHARS = set(".^$*+?()[]{}|")
# Escapes that denote a character class, not a literal.
_CLASS_ESCAPES = set("sSdDwWbBAZ")
# Escapes that denote a control character rather than the escaped letter itself.
_CONTROL_ESCAPES = {"a": "\a", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v"}


def _literal_prefix(pattern: str) -> str:
    r"""Best-effort leading literal of a regex, so anchored patterns are matched.

    Walks the source until the first metacharacter or character class, decoding
    control escapes such as ``\n``, treating any other ``\x`` as literal ``x``,
    and expanding a ``{n}`` repeat of the preceding literal (so ```` `{3} ````
    yields three backticks).
    """
    pattern = pattern.removeprefix("^")
    out: list[str] = []
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "\\" and i + 1 < len(pattern):
            nxt = pattern[i + 1]
            if nxt in _CLASS_ESCAPES:
                break
            out.append(_CONTROL_ESCAPES.get(nxt, nxt))
            i += 2
        elif char == "{" and out:
            end = pattern.find("}", i)
            count = pattern[i + 1 : end] if end != -1 else ""
            if not (repeats := count.split(",")[0]).isdigit():
                break
            out.append(out[-1] * (int(repeats) - 1))
            i = end + 1
        elif char in _METACHARS:
            break
        else:
            out.append(char)
            i += 1
    return "".join(out)


def _regex_literal(node: ast.AST) -> str | None:
    """The pattern source if ``node`` is ``re.<func>("literal", ...)``, else None."""
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
        return None
    if node.func.attr not in _RE_FUNCS or not node.args:
        return None
    first = node.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value
    return None


def _iter_regex_literals() -> list[tuple[str, str]]:
    """Every ``(where, pattern_source)`` from ``re.<func>("literal", ...)`` calls."""
    found: list[tuple[str, str]] = []
    for path in PACKAGE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        found.extend(
            (f"{path.name}:{node.lineno}", pattern)
            for node in ast.walk(tree)
            if (pattern := _regex_literal(node)) is not None
        )
    return found


def _fixture_corpus() -> str:
    return "\n".join(
        text
        for path in sorted(FIXTURE_PATH.glob("*.md"))
        for _l, _t, text, _e in read_fixture_file(path)
    )


_REGEX_LITERALS = _iter_regex_literals()


@pytest.mark.parametrize(
    ("where", "pattern"), _REGEX_LITERALS, ids=[w for w, _p in _REGEX_LITERALS]
)
def test_regex_is_reachable(where: str, pattern: str) -> None:
    prefix = _literal_prefix(pattern)
    # An empty prefix matches everywhere (unanchored), so it is trivially reachable.
    if not prefix:
        return
    assert prefix in _fixture_corpus(), (
        f"{where}: {pattern!r} is never reached by a render fixture "
        "(add a fixture exercising this syntax)"
    )
