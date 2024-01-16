# mdformat-mkdocs

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

<!-- [![codecov.io][cov-badge]][cov-link]
[cov-badge]: https://codecov.io/gh/executablebooks/mdformat-mkdocs/branch/main/graph/badge.svg
[cov-link]: https://codecov.io/gh/executablebooks/mdformat-mkdocs
 -->

An [mdformat](https://github.com/executablebooks/mdformat) plugin for [mkdocs](https://github.com/mkdocs/mkdocs). Supports:

- Indents are converted to 4-spaces instead of 2
    - *Note*: see caveats for Semantic Indents on bulleted lists which may not be a full multiple of 4
- All bullets are converted to dashes instead of `*`
- Admonitions (extends [`mdformat-admon`](https://pypi.org/project/mdformat-admon))

See the example test files, [./tests/pre-commit-test.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/pre-commit-test.md) and [./tests/fixtures.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/fixtures.md)

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. No additional configuration necessary. For additional information on plugins, see [the official `mdformat` documentation here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

**Tip**: this package specifies an "extra" (`'recommended'`) for plugins that work well with mkdocs:

- [mdformat-beautysh](https://pypi.org/project/mdformat-beautysh)
- [mdformat-black](https://pypi.org/project/mdformat-black)
- [mdformat-config](https://pypi.org/project/mdformat-config)
- [mdformat-footnote](https://pypi.org/project/mdformat-footnote)
- [mdformat-frontmatter](https://pypi.org/project/mdformat-frontmatter)
- [mdformat-simple-breaks](https://pypi.org/project/mdformat-simple-breaks)
- [mdformat-tables](https://pypi.org/project/mdformat-tables)
- [mdformat-toc](https://pypi.org/project/mdformat-toc)
- [mdformat-web](https://pypi.org/project/mdformat-web)

### Pre-Commit

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.16
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-mkdocs>=1.2.0
          # Or
          # - "mdformat-mkdocs[recommended]>=1.2.0"
```

### pipx

```sh
pipx install mdformat
pipx inject mdformat mdformat-mkdocs
# Or
# pipx inject mdformat "mdformat-mkdocs[recommended]"
```

## HTML Rendering

To generate HTML output, `mkdocs_admon_plugin` can be imported from `mdit_plugins`. More plugins can be added in the future as appropriate.

```py
from markdown_it import MarkdownIt
from mdformat_mkdocs.mdit_plugins import mkdocs_admon_plugin

md = MarkdownIt("commonmark")
md.use(mkdocs_admon_plugin)

text = '??? note\n    content'
md.render(text)
# <details class="note">
# <summary>Note</summary>
# <p>content</p>
# </details>
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

See [CONTRIBUTING.md](https://github.com/KyleKing/mdformat-mkdocs/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mkdocs/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mkdocs/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mkdocs.svg
[pypi-link]: https://pypi.org/project/mdformat-mkdocs
