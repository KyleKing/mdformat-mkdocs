Simple admonition
.
!!! note
    *content*
.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p><em>content</em></p>
</div>
.


Simple admonition without title
.
!!! note ""
    *content*
.
<div class="admonition note">
<p><em>content</em></p>
</div>
.


Does not render
.
!!!
    content
.
<p>!!!
content</p>
.



MKdocs Closed Collapsible Sections
.
??? note
    content
.
<details class="note">
<summary>Note</summary>
<p>content</p>
</details>
.


MKdocs Open Collapsible Sections
.
???+ note
    content
.
<details class="note" open="open">
<summary>Note</summary>
<p>content</p>
</details>
.
