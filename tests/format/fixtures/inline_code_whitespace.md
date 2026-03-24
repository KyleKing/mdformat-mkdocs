Trailing space only (no leading space) - preserved
.
`code `
.
`code `
.
Leading space only - preserved
.
` code`
.
` code`
.
Both leading and trailing spaces - mdformat strips both
.
` code `
.
`code`
.

Both leading and trailing spaces - mdformat strips both (idempotency)
.
`code`
.
`code`
.
Multiple trailing spaces - preserved
.
`code  `
.
`code  `
.
Trailing tab - preserved (tabs not normalized)
.
`code	`
.
`code	`
.
All whitespace - preserved
.
` `
.
` `
.
Empty code - gets escaped
.
``
.
\`\`
.

Empty code - gets escaped (idempotency)
.
\`\`
.
\`\`
.
Newline before closing backtick (snippet case) - preserved as space
.
`--8<-- "somesnippet.sh"
`
.
`--8<-- "somesnippet.sh" `
.

Newline before closing backtick (snippet case) (idempotency)
.
`--8<-- "somesnippet.sh" `
.
`--8<-- "somesnippet.sh" `
.
Code with internal spaces - preserved
.
`foo bar baz`
.
`foo bar baz`
.
Code with leading and internal spaces - preserved
.
` foo bar`
.
` foo bar`
.
Code with trailing and internal spaces - preserved
.
`foo bar `
.
`foo bar `
.
Double backticks with trailing space - preserved differently
.
``code` ``
.
`` code`  ``
.

Double backticks with trailing space (idempotency)
.
`` code`  ``
.
`` code`  ``
.
Trailing space before horizontal rule - preserved (rule normalized to underscores)
.
`test `

---
.
`test `

______________________________________________________________________
.
Trailing space before heading - preserved
.
`test `

# Heading
.
`test `

# Heading
.
Trailing space in middle of paragraph - preserved
.
This is `code ` in text.
.
This is `code ` in text.
.
Multiple inline codes with trailing spaces - all preserved
.
`first ` and `second ` and `third `
.
`first ` and `second ` and `third `
.
Trailing space in list item - preserved
.
- Item with `code `
.
- Item with `code `
.
Trailing space in blockquote - preserved
.
> Quote with `code `
.
> Quote with `code `
.
Trailing space in admonition - preserved
.
!!! note

    Content with `code `
.
!!! note

    Content with `code `
.
