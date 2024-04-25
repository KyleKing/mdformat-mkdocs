import mdformat
import pytest

from ..helpers import print_text

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

CASE_2 = """
0. xyz
1. abc
"""


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (CASE_1, CASE_1_NUMBERED),
        (CASE_2, CASE_2),
    ],
    ids=[
        "CASE_1_NUMBERED",
        "CASE_2_NUMBERED",
    ],
)
def test_number(text: str, expected: str):
    output = mdformat.text(
        text,
        options={"number": True},
        extensions={"mkdocs"},
    )
    print_text(output, expected)
    assert output.strip() == expected.strip()
