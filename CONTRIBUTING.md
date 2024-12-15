# Development

## API Documentation

A collection of useful resources to reference when developing new features:

- [`markdown-it-py` documentation](https://markdown-it-py.readthedocs.io/en/latest/using.html)
- [`markdown-it` (JS) documentation](https://markdown-it.github.io/markdown-it)

## Local Development

This package utilizes [flit](https://flit.readthedocs.io) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To install these development dependencies:

```bash
pipx install tox
# or: uv tool install tox --with tox-uv
```

To run the tests:

```bash
tox
```

and with test coverage:

```bash
tox -e py39-cov
```

The easiest way to write tests, is to edit `tests/fixtures.md`

To run the code formatting and style checks:

```bash
tox -e py312-pre-commit
```

or directly

```bash
pipx install pre-commit
# or: uv tool install pre-commit
pre-commit run --all
```

To run the pre-commit hook test:

```bash
tox -e py39-hook
```

## `ptw` testing

See configuration in `pyproject.toml` for `[tool.pytest-watcher]`

```sh
pipx install pytest-watcher

ptw .
```

## Local pipx testing

Run the latest local code anywhere with pipx.

```sh
pipx install . --include-deps --force --editable
```

Or with uv:

```sh
uv tool install mdformat --force --with-editable=.
```

## Publish to PyPi

First, update the version in `mdformat_mkdocs/__init__.py`

Then, either use the Github Action by committing the new version in `__init__.py` and pushing an associated tag in format: `v#.#.#` (e.g. `v1.3.2` for `__version__ = '1.3.2'`)

Or run flit locally:

```bash
# envchain --set FLIT FLIT_PASSWORD
export FLIT_USERNAME=__token__
export eval $(envchain FLIT env | grep FLIT_PASSWORD=)

flit publish
```

> [!NOTE]
> The Github Action requires generating an API key on PyPi and adding it to the repository `Settings/Secrets`, under the name `PYPI_KEY`
