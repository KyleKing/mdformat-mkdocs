Examples from https://python-markdown.github.io/extensions/attr_list
<!-- Note: HTML rendering for attribute lists is minimal (formatting only) -->
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
<p><span attributes="['#someid', '.someclass', &quot;somekey='some&quot;, &quot;value'&quot;, '#id1', '.class1', 'id=id2', 'class=&quot;class2', 'class3&quot;', '.class4']">: #someid .someclass somekey='some value' #id1 .class1 id=id2 class=&quot;class2 class3&quot; .class4 </span></p>
<p>{ not an attribute list, but not escaped because '' is dropped during read_fixture_file }</p>
<p><span attributes="['#someid', '.someclass', &quot;somekey='some&quot;, &quot;value'&quot;]"> #someid .someclass somekey='some value' </span></p>
<p>This is a paragraph.
<span attributes="['#an_id', '.a_class']">: #an_id .a_class </span></p>
<h1>A setext style header {: #setext}</h1>
<h3>A hash style header ### <span attributes="['#hash']">: #hash </span></h3>
<p><a href="http://example.com">link</a><span attributes="['class=&quot;foo', 'bar&quot;', 'title=&quot;Some', 'title!&quot;']">: class=&quot;foo bar&quot; title=&quot;Some title!&quot; </span></p>
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
<p><a href="about/index.md">:material-account-box:+ .lg .middle +  <strong>About</strong>  </a><span attributes="['.md-button', 'style=&quot;text-align:', 'center;', 'display:', 'block;&quot;']"> .md-button style=&quot;text-align: center; display: block;&quot; </span></p>
<p><a href="blog/index.md">:fontawesome-brands-blogger-b:+ .lg .middle +  <strong>Blogs</strong>  </a><span attributes="['.md-button', 'style=&quot;text-align:', 'center;', 'display:', 'block;&quot;']"> .md-button style=&quot;text-align: center; display: block;&quot; </span></p>
</div>
.
