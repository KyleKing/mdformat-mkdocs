Examples from https://python-markdown.github.io/extensions/attr_list
.
{: #someid .someclass somekey='some value' #id1 .class1 id=id2 class="class2 class3" .class4 }

\{ not an attribute list, but not escaped because '\' is dropped during read_fixture_file }

{ #someid .someclass somekey='some value' }

This is a paragraph.
{: #an_id .a_class }

A setext style header {: #setext}
=================================

### A hash style header ### {: #hash }

[link](http://example.com){: class="foo bar" title="Some title!" }
.
{: #someid .someclass somekey='some value' #id1 .class1 id=id2 class="class2 class3" .class4 }

{ not an attribute list, but not escaped because '' is dropped during read_fixture_file }

{ #someid .someclass somekey='some value' }

This is a paragraph.
{: #an_id .a_class }

# A setext style header {: #setext}

### A hash style header ### {: #hash }

[link](http://example.com){: class="foo bar" title="Some title!" }
.

Example from https://github.com/KyleKing/mdformat-mkdocs/issues/45 and source https://raw.githubusercontent.com/arv-anshul/arv-anshul.github.io/refs/heads/main/docs/index.md
.
<div class="grid cards" markdown>

<!-- Note: &nbsp; HTML entities are converted to Unicode by mdformat (core behavior) -->

[:material-account-box:+ .lg .middle +&nbsp; **About** &nbsp;](about/index.md){ .md-button style="text-align: center; display: block;" }

[:fontawesome-brands-blogger-b:+ .lg .middle +&nbsp; **Blogs** &nbsp;](blog/index.md){ .md-button style="text-align: center; display: block;" }

</div>
.
<div class="grid cards" markdown>

<!-- Note: &nbsp; HTML entities are converted to Unicode by mdformat (core behavior) -->

[:material-account-box:+ .lg .middle +  **About**  ](about/index.md){ .md-button style="text-align: center; display: block;" }

[:fontawesome-brands-blogger-b:+ .lg .middle +  **Blogs**  ](blog/index.md){ .md-button style="text-align: center; display: block;" }

</div>
.
