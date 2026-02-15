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

# Known HTML stability limitations (not worth fixing)
KNOWN_HTML_STABILITY_LIMITATIONS = {
    "ReLU Function with Mixed Syntax (Issue #45)": "Cosmetic: Extra blank lines in math blocks",
    "Math with Leading/Trailing Whitespace": "Cosmetic: Whitespace normalization around math delimiters",
    "Examples from https://python-markdown.github.io/extensions/attr_list": "Structural: Attribute list rendering differences",
    "Hanging List (https://github.com/executablebooks/mdformat/issues/371 and https://github.com/KyleKing/mdformat-mkdocs/issues/4)": "Known mdformat core limitation (issue #371)",
    "Table (squished by mdformat>=0.7.19)": "Known mdformat core behavior change in 0.7.19",
    "or in a list somehow?": "Structural: Admonitions in lists rendering differences",
    "Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/fd82a671015a30a869d740c45c65f5633d1d93c4/docs/en/guides/isolating-segmentation-objects.md?plain=1#L148-L259)": "Complex: Nested content tabs edge case",
    "Deterministic indents for HTML": "Cosmetic: HTML block indentation changes",
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
    """Validate that formatting doesn't change HTML output.

    This test ensures that mdformat-mkdocs preserves HTML semantics
    when formatting markdown, preventing issues like #77 where
    trailing spaces in inline code would cause validation failures.

    Some test cases are marked as expected failures (xfail) to document known
    limitations that are either cosmetic, mdformat core issues, or complex edge
    cases not worth fixing.
    """
    # Mark known limitations as xfail
    if title in KNOWN_HTML_STABILITY_LIMITATIONS:
        reason = KNOWN_HTML_STABILITY_LIMITATIONS[title]
        pytest.xfail(f"Known limitation: {reason}")

    # Format the markdown
    output = mdformat.text(text, extensions={"mkdocs"})

    # Setup markdown-it parser with mkdocs plugins
    md = MarkdownIt("commonmark")
    # Initialize options with empty mdformat config to prevent KeyError
    md.options.update({"mdformat": {"plugin": {"mkdocs": {}}}})
    update_mdit(md)
    md.options["xhtmlOut"] = False

    # Render both original and formatted to HTML
    original_html = md.render(text)
    formatted_html = md.render(output)

    # HTML should be identical
    assert original_html.rstrip() == formatted_html.rstrip(), (
        f"Formatting changed HTML output for '{title}'. "
        f"This indicates that formatting is not HTML-stable.\n"
        f"Original markdown:\n{text}\n"
        f"Formatted markdown:\n{output}\n"
        f"Original HTML:\n{original_html}\n"
        f"Formatted HTML:\n{formatted_html}"
    )
