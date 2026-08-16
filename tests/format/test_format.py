from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TypeVar

import mdformat
import pytest
from _pytest.mark import ParameterSet
from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs.plugin import update_mdit
from tests.helpers import print_text

KNOWN_HTML_STABILITY_LIMITATIONS: set[str] = {
    "Deterministic indents for HTML",
    "Examples from https://python-markdown.github.io/extensions/attr_list",
    "Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/fd82a671015a30a869d740c45c65f5633d1d93c4/docs/en/guides/isolating-segmentation-objects.md?plain=1#L148-L259)",
    "Issue #81: HTML comment on a continuation line followed by a tight sibling",
    "Issue #84: block math with whitespace on one side only",
    "Math with Leading/Trailing Whitespace",
    "or in a list somehow?",
    "ReLU Function with Mixed Syntax (Issue #45)",
}

T = TypeVar("T")


def flatten(nested_list: list[list[T]]) -> list[T]:
    return [*chain(*nested_list)]


fixtures = flatten(
    [
        read_fixture_file(Path(__file__).parent / "fixtures" / fixture_path)
        for fixture_path in (
            "angle_brackets_and_html.md",
            "inline_code_whitespace.md",
            "material_content_tabs.md",
            "material_deflist.md",
            "material_math.md",
            "math_with_mkdocs_features.md",
            "mkdocstrings_autorefs.md",
            "mkdocstrings_injection.md",
            "pymd_abbreviations.md",
            "pymd_arithmatex.md",
            "pymd_arithmatex_ams_environments.md",
            "pymd_arithmatex_edge_cases.md",
            "pymd_snippet.md",
            "python_markdown_attr_list.md",
            "regression.md",
            "text.md",
        )
    ],
)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_format_fixtures(line, title, text, expected):
    output = mdformat.text(text, extensions={"mkdocs"})
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Known limitation: mdformat's markdown-it parser silently truncates content "
        "nested past its default maxNesting (20), which MkDocs-style 4-space list "
        "indentation reaches at ~10 levels. mdformat-mkdocs used to raise maxNesting "
        "itself, but that couldn't tell an explicit user-configured limit from the "
        "default, so it's been removed pending https://github.com/hukkin/mdformat "
        "adding a public `max_nesting` option. Once that ships and the `mdformat` "
        "dependency is pinned to a version that has it, this test should pass "
        "(document deep nesting via `options={'max_nesting': ...}`) and the "
        "xfail should be removed."
    ),
)
def test_format_deeply_nested_list():
    """A list nested 12 levels deep must format and round-trip without error."""
    depth = 12
    text = "\n".join(f"{'    ' * i}- item{i}" for i in range(depth)) + "\n"

    output = mdformat.text(text, extensions={"mkdocs"})

    assert output.rstrip() == text.rstrip()


def test_extensions_mkdocs_alone_chains_hard_dependencies():
    """Issue #87: `extensions={"mkdocs"}` alone must format tables, frontmatter, footnotes.

    mdformat's API never activates an installed plugin unless its name is
    explicitly passed.
    """
    text = (
        "---\n"
        "title: Test\n"
        "---\n"
        "\n"
        "| a | b |\n"
        "|---|---|\n"
        "| 1 | 2 |\n"
        "\n"
        "Footnote ref[^1].\n"
        "\n"
        "[^1]: Footnote def.\n"
    )

    output = mdformat.text(text, extensions={"mkdocs"})

    assert output == (
        "---\n"
        "title: Test\n"
        "---\n"
        "\n"
        "| a   | b   |\n"
        "| --- | --- |\n"
        "| 1   | 2   |\n"
        "\n"
        "Footnote ref[^1].\n"
        "\n"
        "[^1]: Footnote def.\n"
    )


def _stability_params() -> list[ParameterSet]:
    """Mark known limitations xfail(strict=True) so a fixed one becomes a failure."""
    params = []
    for fixture in fixtures:
        title = fixture[1]
        marks = (
            pytest.mark.xfail(strict=True, reason=f"Known limitation: {title}")
            if title in KNOWN_HTML_STABILITY_LIMITATIONS
            else ()
        )
        params.append(pytest.param(*fixture, marks=marks, id=title))
    return params


@pytest.mark.parametrize(("line", "title", "text", "expected"), _stability_params())
def test_format_html_stability(line, title, text, expected):
    """Validate that formatting doesn't change HTML output."""
    output = mdformat.text(text, extensions={"mkdocs"})

    md = MarkdownIt("commonmark")
    md.options.update({"mdformat": {"plugin": {"mkdocs": {}}}})
    update_mdit(md)
    md.options["xhtmlOut"] = False

    original_html = md.render(text)
    formatted_html = md.render(output)

    assert original_html.rstrip() == formatted_html.rstrip(), (
        f"HTML changed for '{title}'.\n"
        f"Original markdown:\n{text}\n"
        f"Formatted markdown:\n{output}\n"
        f"Original HTML:\n{original_html}\n"
        f"Formatted HTML:\n{formatted_html}"
    )
