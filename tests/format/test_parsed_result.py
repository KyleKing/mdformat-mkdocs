from itertools import chain
from pathlib import Path

import pytest
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs._normalize_list import parse_text

FIXTURE_PATHS = [
    Path(__file__).parent / "fixtures/parsed_result.md",
    Path(__file__).parent / "fixtures/mkdocstrings_injection.md",
]
fixtures = list(
    chain.from_iterable(
        read_fixture_file(path) for path in FIXTURE_PATHS
    )
)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_parsed_result(line, title, text, expected, snapshot):
    output = parse_text(text=text, inc_numbers=False, use_sem_break=True)
    assert output == snapshot
