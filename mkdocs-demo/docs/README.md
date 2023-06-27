# mkdocs-demo

Minimum example code to test MkDocs behavior

## Semantic Line Indents

See discussion on: https://github.com/KyleKing/mdformat-mkdocs/issues/4

### With proposed change

1. Here indent width is
   three.

    1. Here indent width is
       three.

1. Here indent width is
   five (three). It needs to be so, because

   Otherwise this next paragraph doesn't belong in the same list item.

---

### With current behavior

1. Here indent width is
    three (four).

    1. Here indent width is
        three (four).

1. Here indent width is
    five (four). It needs to be so, because

    Otherwise this next paragraph doesn't belong in the same list item.
