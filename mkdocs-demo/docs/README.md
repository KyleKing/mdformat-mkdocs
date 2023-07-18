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
   five (three). The following indent needs to be four (but it is 3 with semantic change).

   Otherwise this next paragraph doesn't belong in the same list item.

---

### With current behavior

1. Here indent width is
    three (four).

    1. Here indent width is
        three (four).

1. Here indent width is
    five (four). The following indent needs to be four.

    Otherwise this next paragraph doesn't belong in the same list item.

---

### With proposed change for bullets

1. Line
   semantic line 1 (3 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)

---

### With proposed change for bullets nested in a numbered list

- Line
  semantic line 1 (2 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)
