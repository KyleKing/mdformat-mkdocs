from pathlib import Path

import pytest
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs._indent import process_text

FIXTURE_PATH = Path(__file__).parent / "fixtures/parsed_result.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_parsed_result(line, title, text, expected, snapshot):
    # TODO: Read these settings from the 'title'
    inc_numbers = False
    use_sem_break = False

    output = process_text(
        text=text,
        eol="\n",
        inc_numbers=inc_numbers,
        use_sem_break=use_sem_break,
    )
    assert output == snapshot
