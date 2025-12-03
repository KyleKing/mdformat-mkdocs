Standalone angle brackets (Issue #71)
.
This is an example <appID>

Another example with <someTag>
.
This is an example <appID>

Another example with <someTag>
.


Angle brackets in list
.
- Item with <appID>
- Another item with <someVar>
    - Nested with <nestedTag>
.
- Item with <appID>
- Another item with <someVar>
    - Nested with <nestedTag>
.


Angle brackets in ordered list
.
1. First item <appID>
2. Second item <someVar>
    1. Nested with <nestedTag>
.
1. First item <appID>
1. Second item <someVar>
    1. Nested with <nestedTag>
.


Angle brackets in blockquote
.
> Quote with <appID> placeholder
>
> Another line with <someVar>
.
> Quote with <appID> placeholder
>
> Another line with <someVar>
.


Angle brackets in admonition
.
!!! note

    Content with <appID>

    Another paragraph with <someVar>
.
!!! note

    Content with <appID>

    Another paragraph with <someVar>
.


Angle brackets in content tabs
.
=== "Tab 1"

    Content with <appID>

=== "Tab 2"

    More content with <someVar>
.
=== "Tab 1"

    Content with <appID>

=== "Tab 2"

    More content with <someVar>
.


HTML comment - material/tags marker
.
<!-- material/tags -->

Some content after the marker
.
<!-- material/tags -->

Some content after the marker
.


HTML comment - material/tags with scope
.
<!-- material/tags { scope: true } -->

Some content
.
<!-- material/tags { scope: true } -->

Some content
.


HTML comment - material/tags with include filter
.
<!-- material/tags { include: [Foo, Bar] } -->
.
<!-- material/tags { include: [Foo, Bar] } -->
.


HTML comment - material/tags with exclude filter
.
<!-- material/tags { exclude: [Internal, Draft] } -->
.
<!-- material/tags { exclude: [Internal, Draft] } -->
.


HTML comment - material/tags with toc control
.
<!-- material/tags { toc: false } -->
.
<!-- material/tags { toc: false } -->
.


HTML comment - material/tags named reference
.
<!-- material/tags scoped -->
.
<!-- material/tags scoped -->
.


Mixed HTML comments and angle brackets
.
<!-- material/tags -->

Content with <appID> placeholder

<!-- material/tags { scope: true } -->

More content with <someVar>
.
<!-- material/tags -->

Content with <appID> placeholder

<!-- material/tags { scope: true } -->

More content with <someVar>
.


Angle brackets that look like HTML tags
.
This is not a tag <div> but treated as text

Also <span class="foo"> is text
.
This is not a tag <div> but treated as text

Also <span class="foo"> is text
.


Angle brackets in code blocks (should be preserved)
.
```bash
echo <container-name>
echo $VAR
```
.
```bash
echo <container-name>
echo $VAR
```
.


Angle brackets in inline code
.
Run `docker exec <container-name>` to enter the container
.
Run `docker exec <container-name>` to enter the container
.


Angle brackets in nested contexts
.
!!! example

    === "CLI"

        ```bash
        command <argument>
        ```

    === "Python"

        Content with <placeholder>
.
!!! example

    === "CLI"

        ```bash
        command <argument>
        ```

    === "Python"

        Content with <placeholder>
.
