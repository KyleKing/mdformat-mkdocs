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
