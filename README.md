# mdformat-mkdocs

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for [mkdocs](https://github.com/mkdocs/mkdocs) and packages commonly used with MkDocs ([mkdocs-material](https://squidfunk.github.io/mkdocs-material), [mkdocstrings](https://mkdocstrings.github.io), and [python-markdown](https://python-markdown.github.io))

mdformat-mkdocs also intentionally supports [Zensical](https://zensical.org), which is working toward feature parity with mkdocs ([as of mid-2026](https://zensical.org/compatibility)) and may ship features ahead of it.

Supports:

- Indents are converted to four-spaces instead of two
    - *Note*: when specifying `--align-semantic-breaks-in-lists`, the nested indent for ordered lists is three, but is otherwise a multiple of four
- Unordered list bullets are converted to dashes (`-`) instead of `*`
- By default, `mdformat-mkdocs` standardizes ordered lists on a single digit (`1.` or `0.`); with `--number`, it applies consecutive numbering instead, [for consistency with `mdformat`](https://github.com/executablebooks/mdformat?tab=readme-ov-file#options)
- [MkDocs-Material Admonitions\*](https://squidfunk.github.io/mkdocs-material/reference/admonitions)
    - \*Note: `mdformat-admon` formats the same admonitions; this package adds an extra space for consistency with the mkdocs styleguide ([#22](https://github.com/KyleKing/mdformat-admon/pull/22))
- [MkDocs-Material Content Tabs\*](https://squidfunk.github.io/mkdocs-material/reference/content-tabs)
    - \*Note: this plugin renders markup (HTML) good enough for formatting but not for viewing in a browser. Open an issue if you need valid HTML.
- [MkDocs-Material Definition Lists](https://squidfunk.github.io/mkdocs-material/reference/lists/#using-definition-lists)
- [mkdocstrings Injection Blocks](https://mkdocstrings.github.io/usage/)
    - Preserves `:::` identifier blocks and their indented YAML options verbatim, including when nested inside lists with `--align-semantic-breaks-in-lists`
- [mkdocstrings Anchors (autorefs)](https://mkdocstrings.github.io/autorefs/#markdown-anchors)
- [mkdocstrings Cross-References](https://mkdocstrings.github.io/usage/#cross-references)
- [Python Markdown "Abbreviations"\*](https://squidfunk.github.io/mkdocs-material/reference/tooltips/#adding-abbreviations)
    - \*Note: the abbreviation markup (HTML) isn't useful for rendering. If you need it, I'm open to contributions; the implementation isn't simple
- [Python Markdown "Attribute Lists"](https://python-markdown.github.io/extensions/attr_list)
    - Preserves attribute list syntax when using `--wrap` mode
- [PyMdown Extensions "Arithmatex" (Math/LaTeX Support)](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex) ([Material for MkDocs Math](https://squidfunk.github.io/mkdocs-material/reference/math))
    - This plugin combines three math rendering plugins from mdit-py-plugins:
        1. **dollarmath**: Handles `$...$` (inline) and `$$...$$` (block) with smart dollar mode that prevents false positives (e.g., `$3.00` is not treated as math)
        1. **texmath**: Handles `\(...\)` (inline) and `\[...\]` (block) LaTeX bracket notation
        1. **amsmath**: Handles LaTeX environments like `\begin{align}...\end{align}`, `\begin{cases}...\end{cases}`, `\begin{matrix}...\end{matrix}`, etc.
    - Can be deactivated entirely with the `--no-mkdocs-math` flag
- [Python Markdown "Snippets"\*](https://facelessuser.github.io/pymdown-extensions/extensions/snippets)
    - \*Note: the markup (HTML) renders the plain text without implementing the snippet logic. I'm open to contributions if anyone needs full support for snippets

### Features with Implicit Support

The following MkDocs/Material/PyMdown syntax passes through mdformat-mkdocs unchanged, preserved as written but not actively normalized:

- [PyMdown Keys](https://facelessuser.github.io/pymdown-extensions/extensions/keys/): `++ctrl+alt+del++` isn't markdown, so it's preserved as-is
- [PyMdown Critic Markup](https://facelessuser.github.io/pymdown-extensions/extensions/critic/): `{--deleted--}`, `{++added++}`, `{~~old~>new~~}`, `{==highlight==}`, `{>>comment<<}`
- [PyMdown Highlight](https://facelessuser.github.io/pymdown-extensions/extensions/mark/): `==marked text==`
- [PyMdown Caret / Tilde](https://facelessuser.github.io/pymdown-extensions/extensions/caret/): `H^2^O`, `CH~3~OH`
- [PyMdown Emoji](https://facelessuser.github.io/pymdown-extensions/extensions/emoji/): `:smile:`, `:material-icon:`
- [PyMdown InlineHilite](https://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite/): language hints inside backtick spans (`:::python code`) are never modified
- [PyMdown SmartSymbols](https://facelessuser.github.io/pymdown-extensions/extensions/smartsymbols/): `(c)`, `(tm)`, `--`, `-->` are plain ASCII in the source, so they're left alone
- [PyMdown MagicLink](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink/): `@username`, `#123` are plain text and pass through untouched
- [Material Grids](https://squidfunk.github.io/mkdocs-material/reference/grids/): `<div class="grid cards" markdown>` is an HTML block; its content is preserved, but the markdown inside it isn't reformatted
- [Mermaid / Superfences](https://squidfunk.github.io/mkdocs-material/reference/diagrams/): diagram code inside fenced blocks is never modified

**Note on [PyMdown ProgressBar](https://facelessuser.github.io/pymdown-extensions/extensions/progressbar/)**: the syntax `[=50% "50%"]` looks like an undefined link reference, so mdformat-mkdocs escapes it to `\[=50% "50%"\]` by default. Use `--ignore-missing-references` to keep it as-is, or skip this extension if you run mdformat without that flag.

See the example test files, [./tests/pre-commit-test.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/pre-commit-test.md) and [./tests/format/fixtures.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/format/fixtures.md)

## `mdformat` Usage

Add this package wherever you use `mdformat`; it auto-recognizes the plugin, no configuration needed. For more on plugins, see [the official `mdformat` documentation](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### Required Extras

Always installed to prevent corruption to footnotes and frontmatter syntaxes supported by MkDocs out of the box:

- [mdformat-gfm](https://github.com/hukkin/mdformat-gfm) for tables, strikethrough, task lists, and autolinks
- [mdformat-front-matters](https://pypi.org/project/mdformat-front-matters) (previously [mdformat-frontmatter](https://pypi.org/project/mdformat-frontmatter)) for yaml frontmatter parsed by MkDocs
- [mdformat-footnote](https://pypi.org/project/mdformat-footnote) for `[^1]: ...` footnote definitions

The `mkdocs` extension chains all three automatically, so `mdformat.text(src, extensions={"mkdocs"})` formats tables, frontmatter, and footnotes without naming each plugin.

This only affects the Python API. `mdformat`'s CLI auto-activates every installed plugin, so it never needed this fix. The API activates only the extensions you name, even when a plugin's package is installed. Before this chaining was added, `extensions={"mkdocs"}` alone left tables squished and footnote references escaped ([#87](https://github.com/KyleKing/mdformat-mkdocs/issues/87)).

### Optional Extras

This package also specifies two "extra" plugins (`'recommended'` and `'recommended-mdsf'`) for plugins that work well with typical documentation managed by `mkdocs`:

- For `'recommended'`:
    - [mdformat-beautysh](https://pypi.org/project/mdformat-beautysh)
    - [mdformat-config](https://pypi.org/project/mdformat-config)
    - [mdformat-ruff](https://github.com/Freed-Wu/mdformat-ruff)
    - [mdformat-simple-breaks](https://pypi.org/project/mdformat-simple-breaks)
    - [mdformat-web](https://pypi.org/project/mdformat-web)
    - [mdformat-wikilink](https://github.com/tmr232/mdformat-wikilink)
- For `'recommended-mdsf'`:
    - Instead of `mdformat-beautysh`, `mdformat-config`, `mdformat-ruff`, and `mdformat-web`, the "mdsf" extras install `mdformat-hooks`, which lets `mdsf` format code blocks in hundreds of languages using CLI formatters you already have installed. This needs extra configuration; see the README: <https://github.com/KyleKing/mdformat-hooks>

### pre-commit/prek

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 1.0.0
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-mkdocs
          # Or
          # - "mdformat-mkdocs[recommended-mdsf]>=5.3.0"
          # Or
          # - "mdformat-mkdocs[recommended]>=5.3.0"
```

### uvx

```sh
uvx --with=mdformat-mkdocs mdformat
```

Or with pipx:

```sh
pipx install mdformat
pipx inject mdformat mdformat-mkdocs
```

## HTML Rendering

To generate HTML output, import any of the plugins from `mdit_plugins`. For more on `MarkdownIt`, see the docs: <https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser>

```py
from markdown_it import MarkdownIt

from mdformat_mkdocs.mdit_plugins import (
    material_admon_plugin,
    material_content_tabs_plugin,
    mkdocstrings_autorefs_plugin,
    mkdocstrings_crossreference_plugin,
    pymd_abbreviations_plugin,
)

md = MarkdownIt()
md.use(material_admon_plugin)
md.use(material_content_tabs_plugin)
md.use(mkdocstrings_autorefs_plugin)
md.use(mkdocstrings_crossreference_plugin)
md.use(pymd_abbreviations_plugin)

text = "- Line 1\n    - `bash command`\n    - Line 3"
md.render(text)
# <ul>
# <li>Line 1
# <ul>
# <li><code>bash command</code></li>
# <li>Line 3</li>
# </ul>
# </li>
# </ul>
```

## Configuration

`mdformat-mkdocs` adds the CLI arguments:

- `--align-semantic-breaks-in-lists` optionally aligns semantic line breaks (continuation lines that aren't a nested list, code block, or admonition) to the width of the list marker: 3 spaces for numbered lists, 2 spaces for bulleted lists. Without it, mdformat-mkdocs applies the 4-space indent everywhere.

    ```txt
    # with: mdformat
    1. Semantic line feed where the following line is
        three spaces deep

    - Semantic line feed where the following line is
        two spaces deep

    # vs. "mdformat --align-semantic-breaks-in-lists"
    1. Semantic line feed where the following line is
       three spaces deep

    - Semantic line feed where the following line is
      two spaces deep
    ```

- `--ignore-missing-references`, if set, stops mdformat-mkdocs from escaping link references that have no definition. Required when references are dynamic, such as with python mkdocstrings

- `--no-mkdocs-math`, if set, turns off math/LaTeX rendering (Arithmatex), which is on by default. Useful for formatting markdown without processing math syntax.

You can also use the toml configuration (https://mdformat.readthedocs.io/en/stable/users/configuration_file.html):

```toml
# .mdformat.toml

[plugin.mkdocs]
align_semantic_breaks_in_lists = true
ignore_missing_references = true
no_mkdocs_math = true
```

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-mkdocs/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mkdocs/actions/workflows/tests.yml/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mkdocs/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mkdocs.svg
[pypi-link]: https://pypi.org/project/mdformat-mkdocs
