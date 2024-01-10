# Development

This package utilizes [flit](https://flit.readthedocs.io) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To install these development dependencies:

```bash
pipx install tox
```

To run the tests:

```bash
tox
```

and with test coverage:

```bash
tox -e py38-cov
```

The easiest way to write tests, is to edit `tests/fixtures.md`

To run the code formatting and style checks:

```bash
tox -e py38-pre-commit
```

or directly

```bash
pip install pre-commit
pre-commit run --all
```

To run the pre-commit hook test:

```bash
tox -e py38-hook
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

## Publish to PyPi

Either use flit directly:

```bash
pipx install flit

# envchain --set FLIT FLIT_PASSWORD
export FLIT_USERNAME=__token__
export eval $(envchain FLIT env | grep FLIT_PASSWORD=)

flit publish
```

or trigger the GitHub Action job, by creating a release with a tag equal to the version, e.g. `v0.0.1` and updating the version in `mdformat_mkdocs/__init__.py`.

Note, this requires generating an API key on PyPi and adding it to the repository `Settings/Secrets`, under the name `PYPI_KEY`.
