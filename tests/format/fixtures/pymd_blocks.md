Issue #88: preserve option indentation in pymdownx.blocks
.
/// details-example
    open: True

Content
///
.
/// details-example
    open: True

Content
///
.

Issue #88: preserve option indentation in pymdownx.blocks with extra indent
.
/// details-example
     open: True

Content
///
.
/// details-example
     open: True

Content
///
.

pymdownx.blocks without options
.
/// note
Content
///
.
/// note

Content
///
.

pymdownx.blocks without options (idempotency)
.
/// note

Content
///
.
/// note

Content
///
.

pymdownx.blocks with an argument
.
/// html | div
    attrs: {style: 'font-size: xx-large'}

Content
///
.
/// html | div
    attrs: {style: 'font-size: xx-large'}

Content
///
.

pymdownx.blocks nested
.
//// tab | Tab A
/// note
Content
///
////
.
//// tab | Tab A

/// note

Content
///
////
.
