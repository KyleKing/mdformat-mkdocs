from itertools import chain
from pathlib import Path

import mdformat
import pytest
from markdown_it.utils import read_fixture_file

from tests.helpers import print_text

FIXTURE_PATHS = [
    Path(__file__).parent / "fixtures/mkdocstrings_injection.md",
    Path(__file__).parent / "fixtures/semantic_indent.md",
]
fixtures = list(chain.from_iterable(read_fixture_file(path) for path in FIXTURE_PATHS))


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_align_semantic_breaks_in_lists(line, title, text, expected):
    output = mdformat.text(
        text,
        options={"align_semantic_breaks_in_lists": True, "wrap": "keep"},
        extensions={"mkdocs"},
    )
    print_text(output, expected)
    assert output == expected
