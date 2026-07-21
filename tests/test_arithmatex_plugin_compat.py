"""Regression tests for arithmatex coexisting with other math plugins (issue #90)."""

import mdformat
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.texmath import texmath_plugin

from mdformat_mkdocs.mdit_plugins import pymd_arithmatex_plugin


def test_coexists_with_preexisting_dollarmath():
    """mdformat-myst registers dollarmath; the ordinal wrap heuristic over-wrapped."""
    md = MarkdownIt("commonmark")
    md.use(dollarmath_plugin)
    md.use(pymd_arithmatex_plugin)


def test_coexists_with_preexisting_texmath():
    md = MarkdownIt("commonmark")
    md.use(dollarmath_plugin)
    md.use(texmath_plugin, delimiters="brackets")
    md.use(pymd_arithmatex_plugin)


def test_same_line_close_with_trailing_text_does_not_swallow_list_items():
    """Regression test: same-line-closed $$...$$ with trailing text must stay idempotent."""
    text = "1. $$a$$\n1. $$b$$ trailing\n   3) $$c$$\n"
    once = mdformat.text(text, extensions={"mkdocs"})
    twice = mdformat.text(once, extensions={"mkdocs"})
    assert once == twice
