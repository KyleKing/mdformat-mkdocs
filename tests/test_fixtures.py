from pathlib import Path

from markdown_it.utils import read_fixture_file
import mdformat
import pytest

from .helpers import print_text

FIXTURE_PATH = Path(__file__).parent / "fixtures.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    "line,title,text,expected", fixtures, ids=[f[1] for f in fixtures]
)
def test_fixtures(line, title, text, expected):
    output = mdformat.text(text, extensions={"mkdocs"}, options={"wrap": "keep"})
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()


TABBED_CODE_BLOCK = '''
1. Add a serializer class

    ```python
    class RecurringEventSerializer(serializers.ModelSerializer):  # (1)!
    \t"""Used to retrieve recurring_event info"""

    \tclass Meta:
    \t\tmodel = RecurringEvent  # (2)!
    ```
'''


@pytest.mark.parametrize(
    "text,expected",
    [
        (TABBED_CODE_BLOCK, TABBED_CODE_BLOCK),
    ],
    ids=[
        "TABBED_CODE_BLOCK",
    ],
)
def test_tabbed_code_block(text: str, expected: str):
    output = mdformat.text(text, extensions={"mkdocs"}, options={"wrap": "keep"})
    print_text(output, expected)
    assert output.strip() == expected.strip()
