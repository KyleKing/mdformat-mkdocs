import mdformat
import pytest

from ..helpers import print_text

CASE_0 = """
0. One
    1. AAA
    1. BBB
    1. CCC
0. Two
0. Three
0. Four
    1. AAA
    1. BBB
    1. CCC
0. Five
0. Six
    1. AAA
    1. BBB
    1. CCC
        1. aaa
        1. bbb
        1. ccc
        1. ddd
0. Seven
"""
CASE_0_NUMBERED = """
0. One
    1. AAA
    2. BBB
    3. CCC
1. Two
2. Three
3. Four
    1. AAA
    2. BBB
    3. CCC
4. Five
5. Six
    1. AAA
    2. BBB
    3. CCC
        1. aaa
        2. bbb
        3. ccc
        4. ddd
6. Seven
"""


CASE_1 = """
1. One
    1. AAA
    1. BBB
    1. CCC
1. Two
1. Three
1. Four
    1. AAA
    1. BBB
    1. CCC
1. Five
1. Six
    1. AAA
    1. BBB
    1. CCC
        1. aaa
        1. bbb
        1. ccc
        1. ddd
1. Seven
"""


CASE_1_NUMBERED = """
1. One
    1. AAA
    2. BBB
    3. CCC
2. Two
3. Three
4. Four
    1. AAA
    2. BBB
    3. CCC
5. Five
6. Six
    1. AAA
    2. BBB
    3. CCC
        1. aaa
        2. bbb
        3. ccc
        4. ddd
7. Seven
"""


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (CASE_0, CASE_0_NUMBERED),
        (CASE_1, CASE_1_NUMBERED),
    ],
    ids=[
        "CASE_0",
        "CASE_1",
    ],
)
def test_number(text: str, expected: str):
    """Test CLI argument for ordered lists, `--number`."""
    # Check that when --number is set, ordered lists are incremented
    output_numbered = mdformat.text(
        text,
        options={"number": True},
        extensions={"mkdocs"},
    )
    print_text(output_numbered, expected)
    assert output_numbered.strip() == expected.strip()

    # Check when not set that ordered lists use a constant 0 or 1
    output = mdformat.text(text, extensions={"mkdocs"})
    print_text(output, text)
    assert output.strip() == text.strip()
