Prevent regression with non-deflists: https://github.com/KyleKing/mdformat-mkdocs/issues/56
.
::: my_lib.core
.
::: my_lib.core
.

mkdocstrings injection with underscores (issue #79)
.
::: preonpy._preonpy.Buffer
.
::: preonpy._preonpy.Buffer
.

mkdocstrings injection with indented YAML options (issue #79)
.
::: preonpy._preonpy.Buffer
    options:
        heading_level: 2
.
::: preonpy._preonpy.Buffer
    options:
        heading_level: 2
.
Inline snippet with newline before closing backtick
.
`--8<-- "somesnippet.sh"
`
.
`--8<-- "somesnippet.sh" `
.

Inline snippet with newline before closing backtick (idempotency)
.
`--8<-- "somesnippet.sh" `
.
`--8<-- "somesnippet.sh" `
.
