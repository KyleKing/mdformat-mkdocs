# Testing `--align-semantic-breaks-in-numbered-lists`

## Semantic Line Indents

See discussion on: https://github.com/KyleKing/mdformat-mkdocs/issues/4

1. Here indent width is
   three.

    1. Here indent width is
       three.

1. Here indent width is
   five (three). It needs to be so, because

   Otherwise this next paragraph doesn't belong in the same list item.

## Code block in semantic indent

From: https://github.com/KyleKing/mdformat-mkdocs/issues/6

1. Item 1
   with a semantic line feed

   ```bash
   echo "I get moved around by prettier/mdformat, originally I am 3 spaces deep"
   ```

1. Item 2

1. Item 3

## Nested semantic lines

From: https://github.com/KyleKing/mdformat-mkdocs/issues/7

1. Line
   semantic line 1 (3 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)
