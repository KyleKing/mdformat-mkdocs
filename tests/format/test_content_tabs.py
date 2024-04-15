from pathlib import Path

import mdformat
import pytest
from markdown_it.utils import read_fixture_file

from ..helpers import print_text

FIXTURE_PATH = Path(__file__).parent / "fixtures/content_tabs.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_content_tabs_fixtures(line, title, text, expected):
    output = mdformat.text(text, extensions={"mkdocs", "admon"})
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()
