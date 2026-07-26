r"""Security guard: ReDoS and XSS regression tests for the render layer.

Two failure modes matter when a plugin renders untrusted markdown to HTML:

- **ReDoS** — a regex with overlapping/nested quantifiers backtracks
  super-linearly on adversarial input. The guard below *derives* payloads from
  the plugin's own render fixtures: each fixture input is a known-valid
  activation, so amplifying a homogeneous character run inside it drives the
  plugin's real regexes without hand-authoring per-rule payloads. Add a fixture
  and the fuzz corpus grows for free.

- **XSS** — a default render rule interpolates captured token content into markup
  without escaping. This cannot be derived from fixtures (the probe has to land
  in the specific sink), so `_INJECTION_CASES` is an explicit list you extend as
  the plugin grows sinks. Each case asserts the raw marker never survives in the
  output (``markdown-it`` runs with raw HTML disabled, so a correctly-escaped
  plugin emits ``&lt;xss&gt;``).

See `SECURITY_GUARD.md` for how to keep this corpus healthy (fixture coverage,
the AST reachability check in `test_regex_reachability.py`, and the optional
Hypothesis deep-fuzz).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import pytest
from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs.plugin import update_mdit

FIXTURE_PATH = Path(__file__).parent / "fixtures"

# Homogeneous runs of one character class are what push overlapping quantifiers
# into catastrophic backtracking; amplify each fixture with every class.
_FILLERS = [" ", "\t", "$", "`", "\\", '"', "-"]
_RUN = 15_000
_BUDGET_SECONDS = 1.0  # Safe threshold relaxed for CI


def _make_md() -> MarkdownIt:
    md = MarkdownIt("commonmark")
    md.options.update({"mdformat": {"plugin": {"mkdocs": {}}}})
    update_mdit(md)
    return md


def _fixture_inputs() -> list[str]:
    return [
        text
        for path in sorted(FIXTURE_PATH.glob("*.md"))
        for _line, _title, text, _expected in read_fixture_file(path)
    ]


def _amplified(text: str, filler: str) -> str:
    """Insert a long homogeneous run into a valid activation.

    Expanding the first internal whitespace keeps the run *inside* the construct
    (many rules strip a trailing run before the vulnerable scan); if there is no
    internal whitespace, append the run to the first line instead.
    """
    run = filler * _RUN
    for i, char in enumerate(text):
        if char in " \t" and 0 < i < len(text) - 1:
            return text[:i] + run + text[i:]
    head, _, tail = text.partition("\n")
    return f"{head}{run}\n{tail}" if tail else head + run


_REDOS_PARAMS = [(text, filler) for text in _fixture_inputs() for filler in _FILLERS]


@pytest.mark.timeout(10)
@pytest.mark.parametrize(
    ("text", "filler"),
    _REDOS_PARAMS,
    ids=[f"{i}-{filler!r}" for i, (_t, filler) in enumerate(_REDOS_PARAMS)],
)
def test_render_is_redos_safe(text: str, filler: str) -> None:
    source = _amplified(text, filler)
    start = time.perf_counter()
    _make_md().render(source)
    elapsed = time.perf_counter() - start
    assert elapsed < _BUDGET_SECONDS, (
        f"render took {elapsed:.3f}s on a {_RUN}x{filler!r} run amplified from "
        f"{text!r}; likely catastrophic backtracking (ReDoS)"
    )


# A live-element / attribute-breakout probe and the marker that only survives if
# the plugin emitted it without HTML-escaping.
_TAG = '"><xss>'
_TAG_MARKER = "<xss"


@dataclass(frozen=True)
class Injection:
    """A probe payload and the marker that must not survive escaping."""

    id: str
    payload: str
    marker: str = _TAG_MARKER


# Extend this as the plugin gains render sinks: add one entry per sink, placing
# the _TAG probe where the plugin captures attacker-controlled content (a block
# body, a label, an attribute value).
_INJECTION_CASES: list[Injection] = []


@pytest.mark.parametrize("case", _INJECTION_CASES, ids=lambda case: case.id)
def test_render_escapes_injection(case: Injection) -> None:
    out = _make_md().render(case.payload)
    assert case.marker not in out, (
        f"{case.id} emitted {case.marker!r} unescaped: {out!r}"
    )


def test_security_corpus_is_populated() -> None:
    """Fail loudly if there is nothing to fuzz, so the guard can't silently no-op."""
    assert _REDOS_PARAMS or _INJECTION_CASES, (
        "no render fixtures and no injection cases: the security guard is inert"
    )
