from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TypeVar

import mdformat
import pytest
from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs.plugin import update_mdit
from tests.helpers import print_text

KNOWN_HTML_STABILITY_LIMITATIONS: set[str] = {
    "Deterministic indents for HTML",
    "Examples from https://python-markdown.github.io/extensions/attr_list",
    "Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/fd82a671015a30a869d740c45c65f5633d1d93c4/docs/en/guides/isolating-segmentation-objects.md?plain=1#L148-L259)",
    "Hanging List (https://github.com/executablebooks/mdformat/issues/371 and https://github.com/KyleKing/mdformat-mkdocs/issues/4)",
    "Math with Leading/Trailing Whitespace",
    "or in a list somehow?",
    "ReLU Function with Mixed Syntax (Issue #45)",
    "Table (squished by mdformat>=0.7.19)",
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


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_format_html_stability(line, title, text, expected):
    """Validate that formatting doesn't change HTML output."""
    if title in KNOWN_HTML_STABILITY_LIMITATIONS:
        pytest.xfail(f"Known limitation: {title}")

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
