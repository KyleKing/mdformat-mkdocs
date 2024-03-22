import mdformat
import pytest

from .helpers import print_text

TICKET_019 = """Example python mkdocstring snippets

[package.module.object][]
[Object][package.module.object]

- [package.module.object][]
- [Object][package.module.object]
"""


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (TICKET_019, TICKET_019),
    ],
    ids=["TICKET_019"],
)
def test_align_semantic_breaks_in_lists(text, expected):
    output = mdformat.text(
        text,
        options={"ignore_missing_reference": True},
        extensions={"mkdocs"},
    )
    print_text(output, expected)
    assert output == expected
