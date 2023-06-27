import mdformat


def test_align_semantic_breaks_in_numbered_lists():
    """For https://github.com/KyleKing/mdformat-mkdocs/issues/4."""
    input_text = """\
1. Here indent width is
   three.

      2. Here indent width is
       three.

123. Here indent width is
     five. It needs to be so, because

     Otherwise this next paragraph doesn't belong in the same list item.
"""
    expected_output = """\
1. Here indent width is
   three.

    1. Here indent width is
       three.

1. Here indent width is
   five. It needs to be so, because

   Otherwise this next paragraph doesn't belong in the same list item.
"""

    output = mdformat.text(
        input_text,
        options={"align_semantic_breaks_in_numbered_lists": True},
        extensions={"mkdocs"},
    )

    assert output == expected_output
