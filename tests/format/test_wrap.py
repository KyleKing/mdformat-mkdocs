import mdformat
import pytest

from tests.helpers import print_text

# FYI: indented text that starts with a number is parsed as the start of a numbered list

CASE_1 = """
# Content

- Test Testing Test Testing Test Testing Test Testing Test Testing
    Test Testing
  - Test Testing Test Testing Test Testing Test Testing Test Testing
      Test Testing Test Testing Test Testing Test Testing Test Testing
      Test Testing

1. Test Testing Test Testing Test Testing Test Testing Test Testing
    Test Testing
  1. Test Testing Test Testing Test Testing Test Testing Test Testing
      Test Testing Test Testing Test Testing Test Testing Test Testing
      Test Testing
"""

CASE_1_FALSE_40 = """
# Content

- Test Testing Test Testing Test Testing
    Test Testing Test Testing Test
    Testing
    - Test Testing Test Testing Test
        Testing Test Testing Test Testing
        Test Testing Test Testing Test
        Testing Test Testing Test Testing
        Test Testing

1. Test Testing Test Testing Test
    Testing Test Testing Test Testing
    Test Testing
1. Test Testing Test Testing Test
    Testing Test Testing Test Testing
    Test Testing Test Testing Test
    Testing Test Testing Test Testing
    Test Testing
"""

CASE_1_FALSE_80 = """
# Content

- Test Testing Test Testing Test Testing Test Testing Test Testing Test Testing
    - Test Testing Test Testing Test Testing Test Testing Test Testing Test
        Testing Test Testing Test Testing Test Testing Test Testing Test Testing

1. Test Testing Test Testing Test Testing Test Testing Test Testing Test Testing
1. Test Testing Test Testing Test Testing Test Testing Test Testing Test Testing
    Test Testing Test Testing Test Testing Test Testing Test Testing
"""

CASE_1_TRUE_40 = """
# Content

- Test Testing Test Testing Test Testing
  Test Testing Test Testing Test
  Testing
    - Test Testing Test Testing Test
      Testing Test Testing Test Testing
      Test Testing Test Testing Test
      Testing Test Testing Test Testing
      Test Testing

1. Test Testing Test Testing Test
   Testing Test Testing Test Testing
   Test Testing
1. Test Testing Test Testing Test
   Testing Test Testing Test Testing
   Test Testing Test Testing Test
   Testing Test Testing Test Testing
   Test Testing
"""

CASE_1_TRUE_80 = """
# Content

- Test Testing Test Testing Test Testing Test Testing Test Testing Test Testing
    - Test Testing Test Testing Test Testing Test Testing Test Testing Test
      Testing Test Testing Test Testing Test Testing Test Testing Test Testing

1. Test Testing Test Testing Test Testing Test Testing Test Testing Test Testing
1. Test Testing Test Testing Test Testing Test Testing Test Testing Test Testing
   Test Testing Test Testing Test Testing Test Testing Test Testing
"""

SPACE = " "
TICKET_020 = f"""
- first line first line first line first line first line first line first line
    whitespace{SPACE}
- second line
"""
TICKET_020_TRUE_79 = """
- first line first line first line first line first line first line first line
  whitespace
- second line
"""

WITH_CODE = """
# A B C

1. Create a `.pre-commit-config.yaml` file in your repository and add the desired
   hooks. For example:

   ```yaml
   repos:
     - repo: https://github.com/psf/black
       rev: v24.4

   ```

   ```md
   # Title
   Content
   1. Numbered List
     * Unordered Sub-List
   ```
"""
WITH_CODE_TRUE_80 = """
# A B C

1. Create a `.pre-commit-config.yaml` file in your repository and add the
   desired hooks. For example:

    ```yaml
    repos:
      - repo: https://github.com/psf/black
        rev: v24.4

    ```

    ```md
    # Title
    Content
    1. Numbered List
      * Unordered Sub-List
    ```
"""
"""Do not format code (https://github.com/KyleKing/mdformat-mkdocs/issues/36).

FYI: See `test_parsed` for debugging internal representation.

"""


@pytest.mark.parametrize(
    ("text", "expected", "align_lists", "wrap"),
    [
        (CASE_1, CASE_1_FALSE_40, False, 40),
        (CASE_1, CASE_1_FALSE_80, False, 80),
        (CASE_1, CASE_1_TRUE_40, True, 40),
        (CASE_1, CASE_1_TRUE_80, True, 80),
        (TICKET_020, TICKET_020_TRUE_79, True, 79),
        (WITH_CODE, WITH_CODE_TRUE_80, True, 80),
    ],
    ids=[
        "CASE_1_FALSE_40",
        "CASE_1_FALSE_80",
        "CASE_1_TRUE_40",
        "CASE_1_TRUE_80",
        "TICKET_020_TRUE_79",
        "WITH_CODE_TRUE_80",
    ],
)
def test_wrap(text: str, expected: str, align_lists: bool, wrap: int):
    output = mdformat.text(
        text,
        options={"align_semantic_breaks_in_lists": align_lists, "wrap": wrap},
        extensions={"mkdocs"},
    )
    print_text(output, expected)
    assert output.lstrip() == expected.lstrip()
