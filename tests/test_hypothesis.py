"""Property-based tests using Hypothesis."""

from __future__ import annotations

import os
import re

import mdformat
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from markdown_it import MarkdownIt

from mdformat_mkdocs.plugin import update_mdit

settings.register_profile(
    "ci",
    max_examples=50,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
)
settings.register_profile("dev", max_examples=25)
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "ci"))

_SAFE_TEXT = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
)

_MAX_LIST_DEPTH = 3
_MAX_CODE_DEPTH = 2


def _render(text: str) -> str:
    md = MarkdownIt("commonmark")
    md.options.update({"mdformat": {"plugin": {"mkdocs": {}}}})
    update_mdit(md)
    md.options["xhtmlOut"] = False
    return md.render(text).rstrip()


def _has_known_html_limitation(text: str) -> bool:
    if re.search(r"<[a-zA-Z]", text):
        return True
    if any("|" in line for line in text.splitlines()):
        return True
    if re.search(r"\$\s|\s\$", text):
        return True
    return bool(re.search(r"^\d+\.\s{2,}", text, re.MULTILINE))


@st.composite
def bullet_list(draw: st.DrawFn, depth: int = 1) -> str:
    indent = "    " * (depth - 1)
    items = draw(st.lists(_SAFE_TEXT, min_size=1, max_size=3))
    lines: list[str] = []
    for item in items:
        lines.append(f"{indent}- {item}")
        if depth < _MAX_LIST_DEPTH and draw(st.booleans()):
            nested = draw(bullet_list(depth=depth + 1))
            lines.append(nested)
    return "\n".join(lines)


@st.composite
def numbered_list(draw: st.DrawFn, depth: int = 1) -> str:
    indent = "    " * (depth - 1)
    items = draw(st.lists(_SAFE_TEXT, min_size=1, max_size=3))
    lines: list[str] = []
    for i, item in enumerate(items, start=1):
        lines.append(f"{indent}{i}. {item}")
        if depth < _MAX_LIST_DEPTH and draw(st.booleans()):
            nested = draw(numbered_list(depth=depth + 1))
            lines.append(nested)
    return "\n".join(lines)


@st.composite
def bracketed_inline(draw: st.DrawFn) -> str:
    text = draw(
        st.one_of(
            st.just("$math$"),
            st.just("{attr}"),
            st.just("\\[escaped\\]"),
            _SAFE_TEXT,
        )
    )
    return f"[{text}](https://example.com)"


@st.composite
def deflist_block(draw: st.DrawFn) -> str:
    term = draw(_SAFE_TEXT)
    definition = draw(_SAFE_TEXT)
    return f"{term}\n\n:   {definition}"


@st.composite
def fenced_code_block(draw: st.DrawFn, depth: int = 0) -> str:
    lang = draw(st.sampled_from(["python", "bash", "text", ""]))
    content = draw(_SAFE_TEXT)
    fence = "```"
    indent = "    " * depth
    inner = f"{indent}{fence}{lang}\n{indent}{content}\n{indent}{fence}"
    if depth < _MAX_CODE_DEPTH and draw(st.booleans()):
        wrapper_content = draw(fenced_code_block(depth=depth + 1))
        return f"{indent}- item\n\n{wrapper_content}"
    return inner


@st.composite
def injection_block(draw: st.DrawFn) -> str:
    # Identifier: letters only (no spaces/punctuation that break ::: syntax)
    module = draw(
        st.text(
            alphabet=st.characters(whitelist_categories=("L",)), min_size=1, max_size=20
        )
    )
    return f"::: {module}"


@st.composite
def admonition_block(draw: st.DrawFn) -> str:
    admon_type = draw(
        st.sampled_from(["note", "tip", "warning", "danger", "info", "success"])
    )
    title = draw(_SAFE_TEXT)
    content = draw(_SAFE_TEXT)
    return f'!!! {admon_type} "{title}"\n    {content}'


@st.composite
def content_tab_block(draw: st.DrawFn) -> str:
    label = draw(_SAFE_TEXT)
    content = draw(_SAFE_TEXT)
    return f'=== "{label}"\n    {content}'


@st.composite
def markdown_document(draw: st.DrawFn) -> str:
    block_strategy = st.one_of(
        bullet_list(),
        numbered_list(),
        bracketed_inline(),
        deflist_block(),
        fenced_code_block(),
        injection_block(),
        admonition_block(),
        content_tab_block(),
    )
    blocks = draw(st.lists(block_strategy, min_size=1, max_size=5))
    return "\n\n".join(blocks)


@given(markdown_document())
def test_idempotency(text: str) -> None:
    once = mdformat.text(text, extensions={"mkdocs"})
    twice = mdformat.text(once, extensions={"mkdocs"})
    assert once == twice


@given(markdown_document())
def test_html_round_trip(text: str) -> None:
    output = mdformat.text(text, extensions={"mkdocs"})
    assume(not _has_known_html_limitation(output))
    assert _render(text) == _render(output)
