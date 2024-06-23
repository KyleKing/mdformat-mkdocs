import mdformat
import pytest

from tests.helpers import print_text

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
    ("text", "expected"),
    [
        (TABBED_CODE_BLOCK, TABBED_CODE_BLOCK),
    ],
    ids=["TABBED_CODE_BLOCK"],
)
def test_tabbed_code_block(text: str, expected: str):
    output = mdformat.text(text, extensions={"mkdocs", "admon"})
    print_text(output, expected)
    assert output.strip() == expected.strip()
