"""Verify that custom inline rules follow the markdown-it silent-mode protocol.

Rules called in silent mode (e.g. via skipToken during parseLinkLabel) must
advance state.pos when returning True.  skipToken only auto-advances by 1 when
ok=False; a True return with an unchanged pos causes an infinite loop.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest
from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from mdformat_mkdocs.mdit_plugins._mkdocstrings_autorefs import (
    _AUTOREFS_PATTERN,
    _mkdocstrings_autorefs_plugin,
)
from mdformat_mkdocs.mdit_plugins._mkdocstrings_crossreference import (
    _CROSSREFERENCE_PATTERN,
    _mkdocstrings_crossreference,
)
from mdformat_mkdocs.mdit_plugins._python_markdown_attr_list import (
    _ATTR_LIST_PATTERN,
    _python_markdown_attr_list,
)
from mdformat_mkdocs.mdit_plugins._spaced_url_link import _spaced_url_link

_SILENT = True
_NOT_SILENT = False

_InlineRule = Callable[[StateInline, bool], bool]


def _make_state(src: str) -> StateInline:
    md = MarkdownIt("commonmark")
    return StateInline(src, md, {}, [])


@pytest.mark.parametrize(
    ("rule", "pattern", "src"),
    [
        (
            _python_markdown_attr_list,
            _ATTR_LIST_PATTERN,
            '{ width="960" height="540" }',
        ),
        (
            _python_markdown_attr_list,
            _ATTR_LIST_PATTERN,
            "{: .class #id }",
        ),
        (
            _python_markdown_attr_list,
            _ATTR_LIST_PATTERN,
            '{ loading="lazy" decoding="async" }',
        ),
        (
            _mkdocstrings_autorefs_plugin,
            _AUTOREFS_PATTERN,
            "[](){#some-anchor}",
        ),
        (
            _mkdocstrings_crossreference,
            _CROSSREFERENCE_PATTERN,
            "[Package.Module][]",
        ),
        (
            _mkdocstrings_crossreference,
            _CROSSREFERENCE_PATTERN,
            "[Object][package.module.object]",
        ),
    ],
)
def test_silent_mode_advances_pos_on_match(
    rule: _InlineRule,
    pattern: object,
    src: str,
) -> None:
    state = _make_state(src)
    assert pattern.match(src), "fixture must match the pattern"

    pos_before = state.pos
    result = rule(state, _SILENT)

    assert result is True
    assert state.pos > pos_before, (
        f"{rule.__name__}: silent=True must advance state.pos"
    )
    assert state.pos == len(src), f"{rule.__name__}: state.pos must reach end of match"


@pytest.mark.parametrize(
    ("rule", "src"),
    [
        (_python_markdown_attr_list, "no attr list here"),
        (_mkdocstrings_autorefs_plugin, "not an autoref"),
        (_mkdocstrings_crossreference, "not a cross-reference"),
        (_spaced_url_link, "not a link"),
    ],
)
def test_silent_mode_does_not_advance_pos_on_no_match(
    rule: _InlineRule, src: str
) -> None:
    state = _make_state(src)

    pos_before = state.pos
    result = rule(state, _NOT_SILENT)

    assert result is False
    assert state.pos == pos_before, (
        f"{rule.__name__}: non-match must not move state.pos"
    )


def test_spaced_url_link_advances_pos_in_silent_mode() -> None:
    src = "[text](url with spaces)"
    state = _make_state(src)

    result = _spaced_url_link(state, _SILENT)

    assert result is True
    assert state.pos == len(src)


def test_attr_list_silent_skips_escaped_brace() -> None:
    src = '\\{ width="960" }remaining'
    state = _make_state(src)
    state.pos = 1

    result = _python_markdown_attr_list(state, _SILENT)

    assert result is False
    assert state.pos == 1


def test_attr_list_silent_skips_when_link_level_nonzero() -> None:
    src = '{ width="960" height="540" }'
    state = _make_state(src)
    state.linkLevel = 1

    result = _python_markdown_attr_list(state, _SILENT)

    assert result is False
    assert state.pos == 0


def test_attr_list_silent_skips_inside_linked_image_with_long_url() -> None:
    """Guard must fire even when the outer '[' is more than 100 chars back.

    The previous 100-char lookback limit caused this guard to fail for URLs
    longer than ~100 chars, which then triggered the infinite-loop bug (#83).
    """
    long_url = "https://storage.googleapis.com/com-roboflow-marketing/trackers/docs/roboflow-piotr-rf-detr-trackers-v1b-callout.png"
    src = f'[![alt]({long_url}){{ width="960" height="540" }}](https://example.com)'
    brace_pos = src.index("{")
    state = _make_state(src)
    state.pos = brace_pos
    state.posMax = len(src)

    result = _python_markdown_attr_list(state, _SILENT)

    assert result is False, "attr_list inside link label must be skipped"
    assert state.pos == brace_pos, "pos must be unchanged when returning False"
