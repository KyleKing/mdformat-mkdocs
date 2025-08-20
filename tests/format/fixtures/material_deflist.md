Pandoc (with slightly changed indents):
.
paragraph

Term 1

: Definition 1

Term 2 with *inline markup*

: Definition 2

      { some code, part of Definition 2 }

  Third paragraph of definition 2.

paragraph
.
paragraph

Term 1

:   Definition 1

Term 2 with *inline markup*

:   Definition 2

    ```
    { some code, part of Definition 2 }
    ```

    Third paragraph of definition 2.

paragraph
.

Pandoc 2:
.
Term 1

: Definition
with lazy continuation.

  Second paragraph of the definition.
.
Term 1

:   Definition
    with lazy continuation.

    Second paragraph of the definition.
.

Pandoc 3
.
paragraph

Term 1
  ~ Definition 1

Term 2
  ~ Definition 2a
  ~ Definition 2b

paragraph
.
paragraph

Term 1
:   Definition 1

Term 2
:   Definition 2a
:   Definition 2b

paragraph
.

Spaces after a colon:
.
Term 1
  :    paragraph

Term 2
  :     code block
.
Term 1
:   paragraph

Term 2
:   ```
    code block
    ```
.

List is tight, only if all dts are tight:
.
Term 1
: foo
: bar

Term 2
: foo

: bar
.
Term 1

:   foo

:   bar

Term 2

:   foo

:   bar
.


Regression test (first paragraphs shouldn't be tight):
.
Term 1
: foo

  bar

Term 2
: foo
.
Term 1

:   foo

    bar

Term 2

:   foo
.

Nested definition lists:

.
test
  : foo
      : bar
          : baz
      : bar
  : foo
.
test
:   foo
    :   bar
        :   baz
    :   bar
:   foo
.

Regression test (blockquote inside deflist)
.
foo
: > bar
: baz
.
foo
:   > bar
:   baz
.

Escaped deflist (supported by the deflist plugin, but not mdformat-mkdocs for now - see https://github.com/KyleKing/mdformat-mkdocs/issues/56)
.
Term 1
\: Definition
.
Term 1
: Definition
.
