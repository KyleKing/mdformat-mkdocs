"""Verify that custom inline rules follow the markdown-it silent-mode protocol.

Rules called in silent mode (e.g. via skipToken during parseLinkLabel) must
advance state.pos when returning True.  skipToken only auto-advances by 1 when
ok=False; a True return with an unchanged pos causes an infinite loop.
"""

from __future__ import annotations

import pytest
from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from mdformat_mkdocs.mdit_plugins._python_markdown_attr_list import (
    _ATTR_LIST_PATTERN,
    _python_markdown_attr_list,
)

_SILENT = True
_NOT_SILENT = False


def _make_state(src: str) -> StateInline:
    md = MarkdownIt("commonmark")
    return StateInline(src, md, {}, [])


@pytest.mark.parametrize(
    "src",
    [
        '{ width="960" height="540" }',
        "{: .class #id }",
        '{ loading="lazy" decoding="async" }',
    ],
)
def test_silent_mode_advances_pos_on_match(src: str) -> None:
    state = _make_state(src)
    assert _ATTR_LIST_PATTERN.match(src), "fixture must match the pattern"

    pos_before = state.pos
    result = _python_markdown_attr_list(state, _SILENT)

    assert result is True
    assert state.pos > pos_before, "silent=True must advance state.pos on a match"
    assert state.pos == len(src), "state.pos must reach the end of the match"


def test_silent_mode_does_not_advance_pos_on_no_match() -> None:
    src = "no attr list here"
    state = _make_state(src)

    pos_before = state.pos
    result = _python_markdown_attr_list(state, _NOT_SILENT)

    assert result is False
    assert state.pos == pos_before, "non-match must not move state.pos"


def test_silent_mode_skips_escaped_brace() -> None:
    src = '\\{ width="960" }remaining'
    state = _make_state(src)
    state.pos = 1  # position at '{', with '\' just before

    result = _python_markdown_attr_list(state, _SILENT)

    assert result is False
    assert state.pos == 1


def test_silent_mode_skips_when_link_level_nonzero() -> None:
    src = '{ width="960" height="540" }'
    state = _make_state(src)
    state.linkLevel = 1

    result = _python_markdown_attr_list(state, _SILENT)

    assert result is False
    assert state.pos == 0


def test_silent_mode_skips_attr_list_inside_linked_image() -> None:
    """Rule must return False when inside link text, even for long URLs.

    The previous 100-char lookback limit caused this guard to fail for URLs
    longer than ~100 chars, which then triggered the infinite-loop bug.
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
