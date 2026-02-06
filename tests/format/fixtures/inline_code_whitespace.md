Trailing space only (no leading space) - stripped by best-effort
.
`code `
.
`code`
.
Leading space only - preserved
.
` code`
.
` code`
.
Both leading and trailing spaces - both stripped (mdformat behavior)
.
` code `
.
`code`
.
Multiple trailing spaces - stripped by best-effort
.
`code  `
.
`code`
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
Newline before closing backtick (snippet case) - stripped by best-effort
.
`--8<-- "somesnippet.sh"
`
.
`--8<-- "somesnippet.sh"`
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
Code with trailing and internal spaces - trailing stripped
.
`foo bar `
.
`foo bar`
.
Double backticks with trailing space - preserved (processed differently)
.
``code` ``
.
`` code`  ``
.
Trailing space before horizontal rule - stripped (best-effort)
.
`test `

---
.
`test`

______________________________________________________________________
.
Trailing space before heading - stripped (best-effort)
.
`test `

# Heading
.
`test`

# Heading
.
Trailing space in middle of paragraph - stripped (best-effort)
.
This is `code ` in text.
.
This is `code` in text.
.
Multiple inline codes with trailing spaces - all stripped
.
`first ` and `second ` and `third `
.
`first` and `second` and `third`
.
Trailing space in list item - stripped
.
- Item with `code `
.
- Item with `code`
.
Trailing space in blockquote - stripped
.
> Quote with `code `
.
> Quote with `code`
.
Trailing space in admonition - stripped
.
!!! note

    Content with `code `
.
!!! note

    Content with `code`
.
