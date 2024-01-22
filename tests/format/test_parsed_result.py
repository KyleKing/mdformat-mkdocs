import json
from pathlib import Path

import pytest
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs._indent import process_text

from ..helpers import print_text

FIXTURE_PATH = Path(__file__).parent / "fixtures/parsed_result.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    ("line", "title", "text", "expected"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_parsed_result(line, title, text, expected):
    # TODO: Read these settings from the 'title'
    number_mode = False
    use_sem_break = False

    output = process_text(
        text=text,
        eol="\n",
        number_mode=number_mode,
        use_sem_break=use_sem_break,
    )

    parsed_result = output._asdict()
    pretty_parsed_result = json.dumps(parsed_result, indent=4)
    print_text(pretty_parsed_result, expected)
    assert pretty_parsed_result == expected.strip()
