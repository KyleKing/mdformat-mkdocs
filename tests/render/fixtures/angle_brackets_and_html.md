Standalone angle brackets
.
This is an example <appID>
.
<p>This is an example <appID></p>
.


Angle brackets in list
.
- Item with <appID>
- Another with <someVar>
.
<ul>
<li>Item with <appID></li>
<li>Another with <someVar></li>
</ul>
.


HTML comment - material/tags marker
.
<!-- material/tags -->

Some content
.
<!-- material/tags -->
<p>Some content</p>
.


HTML comment with parameters
.
<!-- material/tags { scope: true } -->
.
<!-- material/tags { scope: true } -->
.


Mixed content
.
<!-- material/tags -->

Content with <appID>
.
<!-- material/tags -->
<p>Content with <appID></p>
.


Angle brackets in code blocks
.
```bash
echo <container-name>
```
.
<pre><code class="language-bash">echo &lt;container-name&gt;
</code></pre>
.


Angle brackets in inline code
.
Run `docker exec <container-name>` command
.
<p>Run <code>docker exec &lt;container-name&gt;</code> command</p>
.
