# mdformat-mkdocs

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

<!-- [![codecov.io][cov-badge]][cov-link]
[cov-badge]: https://codecov.io/gh/executablebooks/mdformat-mkdocs/branch/main/graph/badge.svg
[cov-link]: https://codecov.io/gh/executablebooks/mdformat-mkdocs
 -->

An [mdformat](https://github.com/executablebooks/mdformat) plugin for mkdocs.

## Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. No additional configuration necessary. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

Tip: this package specifies an "extra" (`recommended`) for plugins that work well with mkdocs:

- [mdformat-admon](https://pypi.org/project/mdformat-admon)
- [mdformat-beautysh](https://pypi.org/project/mdformat-beautysh)
- [mdformat-black](https://pypi.org/project/mdformat-black)
- [mdformat-config](https://pypi.org/project/mdformat-config)
- [mdformat-footnote](https://pypi.org/project/mdformat-footnote)
- [mdformat-frontmatter](https://pypi.org/project/mdformat-frontmatter)
- [mdformat-simple-breaks](https://pypi.org/project/mdformat-simple-breaks)
- [mdformat-tables](https://pypi.org/project/mdformat-tables)
- [mdformat-toc](https://pypi.org/project/mdformat-toc)
- [mdformat-web](https://pypi.org/project/mdformat-web)

### Pre-commit

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.16
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-mkdocs
          # Or
          # - "mdformat-mkdocs[recommended]"
```

### pipx

```sh
pipx install mdformat
pipx inject mdformat mdformat-mkdocs
# Or
# pipx inject mdformat "mdformat-mkdocs[recommended]"
```

## Caveats

- All indents are converted to 4-spaces
- This plugin converts all bulleted items to dashes (`-`) and numerals to `1.`

See the example test files, [./tests/pre-commit-test.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/pre-commit-test.md) and [./tests/fixtures.md](https://raw.githubusercontent.com/KyleKing/mdformat-mkdocs/main/tests/fixtures.md)

## Contributing

See [CONTRIBUTING.md](https://github.com/KyleKing/mdformat-mkdocs/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mkdocs/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mkdocs/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mkdocs.svg
[pypi-link]: https://pypi.org/project/mdformat-mkdocs
