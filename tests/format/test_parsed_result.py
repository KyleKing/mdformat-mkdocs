from pathlib import Path

import pytest
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs._normalize_list import parse_text

FIXTURE_PATH = Path(__file__).parent / "fixtures/parsed_result.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_parsed_result(line, title, text, expected, snapshot):
    output = parse_text(text=text, inc_numbers=False)
    assert output == snapshot
