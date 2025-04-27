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

WITH_ATTR_LIST = r"""
{: #someid .someclass somekey='some value' #id1 .class1 id=id2 class="class2 class3" .class4 }

\\{ not an attribute list and should be wrapped at 80 characters and not kept inline }

This is a long paragraph that is more than 80 characters long and should be wrapped.
{: #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class }

A setext style header {: #setext}
=================================

### A hash style header ### {: #hash }

[link](http://example.com){: class="foo bar" title="Some title!" .a_class1 .a_class2 .a_class1 .a_class2 .a_class1 .a_class2 }
"""
WITH_ATTR_LIST_TRUE_80 = r"""
{: #someid .someclass somekey='some value' #id1 .class1 id=id2 class="class2 class3" .class4 }

\\{ not an attribute list and should be wrapped at 80 characters and not kept
inline }

This is a long paragraph that is more than 80 characters long and should be
wrapped.
{: #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class  #an_id .a_class }

# A setext style header {: #setext}

### A hash style header ### {: #hash }

[link](http://example.com){: class="foo bar" title="Some title!" .a_class1 .a_class2 .a_class1 .a_class2 .a_class1 .a_class2 }
"""

CASE_ATTR_LIST_WRAP = """
This is a paragraph with a long attribute list that should not be wrapped {: .class1 .class2 .class3 .class4 .class5 .class6 .class7 .class8 .class9 .class10 .class11 .class12 .class13 .class14 .class15 .class16 .class17 .class18 .class19 .class20 }
"""

CASE_ATTR_LIST_WRAP_TRUE_80 = """
This is a paragraph with a long attribute list that should not be wrapped
{: .class1 .class2 .class3 .class4 .class5 .class6 .class7 .class8 .class9 .class10 .class11 .class12 .class13 .class14 .class15 .class16 .class17 .class18 .class19 .class20 }
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
        (WITH_ATTR_LIST, WITH_ATTR_LIST_TRUE_80, True, 80),
        (CASE_ATTR_LIST_WRAP, CASE_ATTR_LIST_WRAP_TRUE_80, True, 80),
    ],
    ids=[
        "CASE_1_FALSE_40",
        "CASE_1_FALSE_80",
        "CASE_1_TRUE_40",
        "CASE_1_TRUE_80",
        "TICKET_020_TRUE_79",
        "WITH_CODE_TRUE_80",
        "WITH_ATTR_LIST_TRUE_80",
        "CASE_ATTR_LIST_WRAP_TRUE_80",
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
