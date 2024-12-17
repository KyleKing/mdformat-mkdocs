# mdformat-mkdocs

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

<!-- [![codecov.io][cov-badge]][cov-link]
[cov-badge]: https://codecov.io/gh/executablebooks/mdformat-mkdocs/branch/main/graph/badge.svg
[cov-link]: https://codecov.io/gh/executablebooks/mdformat-mkdocs
 -->

An [mdformat](https://github.com/executablebooks/mdformat) plugin for [mkdocs](https://github.com/mkdocs/mkdocs) and packages commonly used with MkDocs ([mkdocs-material](https://squidfunk.github.io/mkdocs-material), [mkdocstrings](https://mkdocstrings.github.io), and [python-markdown](https://python-markdown.github.io))

Supports:

- Indents are converted to four-spaces instead of two
    - *Note*: when specifying `--align-semantic-breaks-in-lists`, the nested indent for ordered lists is three, but is otherwise a multiple of four
- Unordered list bullets are converted to dashes (`-`) instead of `*`
- By default, ordered lists are standardized on a single digit (`1.` or `0.`) unless `--number` is specified, then `mdformat-mkdocs` will apply consecutive numbering to ordered lists [for consistency with `mdformat`](https://github.com/executablebooks/mdformat?tab=readme-ov-file#options)
- [MkDocs-Material Admonitions\*](https://squidfunk.github.io/mkdocs-material/reference/admonitions)
    - \*Note: `mdformat-admon` will format the same admonitions, but for consistency with the mkdocs styleguide, an extra space will be added by this package ([#22](https://github.com/KyleKing/mdformat-admon/pull/22))
- [MkDocs-Material Content Tabs\*](https://squidfunk.github.io/mkdocs-material/reference/content-tabs)
    - \*Note: the markup (HTML) rendered by this plugin is sufficient for formatting but not for viewing in a browser. Please open an issue if you have a need to generate valid HTML.
- [mkdocstrings Anchors (autorefs)](https://mkdocstrings.github.io/autorefs/#markdown-anchors)
- [mkdocstrings Cross-References](https://mkdocstrings.github.io/usage/#cross-references)
- [Python Markdown "Abbreviations"\*](https://squidfunk.github.io/mkdocs-material/reference/tooltips/#adding-abbreviations)
    - \*Note: the markup (HTML) rendered for abbreviations is not useful for rendering. If important, I'm open to contributions because the implementation could be challenging
- [Python Markdown "Snippets"\*](https://facelessuser.github.io/pymdown-extensions/extensions/snippets)
    - \*Note: the markup (HTML) renders the plain text without implementing the snippet logic. I'm open to contributions if anyone needs full support for snippets

See the example test files, [./tests/pre-commit-test.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/pre-commit-test.md) and [./tests/format/fixtures.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/format/fixtures.md)

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. No additional configuration necessary. For additional information on plugins, see [the official `mdformat` documentation here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

**Tip**: this package specifies an "extra" (`'recommended'`) for plugins that work well with typical documentation managed by `mkdocs`:

- [mdformat-beautysh](https://pypi.org/project/mdformat-beautysh)
- [mdformat-black](https://pypi.org/project/mdformat-black)
- [mdformat-config](https://pypi.org/project/mdformat-config)
- [mdformat-footnote](https://pypi.org/project/mdformat-footnote)
- [mdformat-frontmatter](https://pypi.org/project/mdformat-frontmatter)
- [mdformat-simple-breaks](https://pypi.org/project/mdformat-simple-breaks)
- [mdformat-tables](https://pypi.org/project/mdformat-tables)
- [mdformat-web](https://pypi.org/project/mdformat-web)
- [mdformat-wikilink](https://github.com/tmr232/mdformat-wikilink)

### Pre-Commit

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.18
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-mkdocs
          # Or
          # - "mdformat-mkdocs[recommended]"
```

### pipx/uv

```sh
pipx install mdformat
pipx inject mdformat mdformat-mkdocs
```

Or with uv:

```sh
uv tool run --from mdformat-mkdocs mdformat
```

## HTML Rendering

To generate HTML output, any of the plugins can be imported from `mdit_plugins`. For more guidance on `MarkdownIt`, see the docs: <https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser>

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

## CLI Options

`mdformat-mkdocs` adds the CLI argument `--align-semantic-breaks-in-lists` to optionally align line breaks in numbered lists to 3-spaces. If not specified, the default of 4-indents is followed universally.

```txt
# with: mdformat
1. Semantic line feed where the following line is
    three spaces deep

# vs. with: mdformat --align-semantic-breaks-in-lists
1. Semantic line feed where the following line is
   three spaces deep
```

Note: the `align-semantic-breaks-in-lists` setting is not supported in the configuration file yet (https://github.com/executablebooks/mdformat/issues/378)

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-mkdocs/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mkdocs/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mkdocs/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mkdocs.svg
[pypi-link]: https://pypi.org/project/mdformat-mkdocs
