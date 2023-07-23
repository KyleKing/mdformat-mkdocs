# mkdocs-demo

Minimum example code to test MkDocs behavior

## Semantic Line Indents

See discussion on: https://github.com/KyleKing/mdformat-mkdocs/issues/4

### Default without Semantic Indents

1. Here indent width is
    three (four).

    1. Here indent width is
        three (four).

1. Here indent width is
    five (four). The following indent needs to be four.

    Otherwise this next paragraph doesn't belong in the same list item.

### With Smart Semantic Indents ON

1. Here indent width is
   three.

    1. Here indent width is
       three.

1. Here indent width is
   five (three). The following indent needs to be four (but it is 3 with semantic change).

    Otherwise this next paragraph doesn't belong in the same list item.

#### For bullets

1. Line
   semantic line 1 (3 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)

#### For bullets nested in a numbered list

- Line
  semantic line 1 (2 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)
