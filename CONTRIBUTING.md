# Development

## API Documentation

A collection of useful resources to reference when developing new features:

- [`markdown-it-py` documentation](https://markdown-it-py.readthedocs.io/en/latest/using.html)
- [`markdown-it` (JS) documentation](https://markdown-it.github.io/markdown-it)

## Local Development

This package utilizes [uv](https://docs.astral.sh/uv) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To install these development dependencies:

```bash
uv tool install tox --with tox-uv
# or: pipx install tox
```

To run the tests:

```bash
tox
```

and with test coverage:

```bash
tox -e py310-test
```

The easiest way to write tests, is to edit `tests/fixtures.md`

To run the code formatting and style checks:

```bash
tox -e py312-prek
```

or directly with [prek](https://github.com/j178/prek) (or pre-commit)

```bash
uv tool install prek
# or: pipx install prek, brew install prek, etc.

prek install -f
prek run --all
```

To run the pre-commit hook test:

```bash
tox -e py310-hook
```

## `ptw` testing

See configuration in `pyproject.toml` for `[tool.pytest-watcher]`

```sh
uv tool install pytest-watcher
# or: pipx install pytest-watcher

ptw .
```

## Local uv/pipx testing

Run the latest local code anywhere with uv tool.

```sh
uv tool install . --editable --force --with="mdformat>=0.7.19"
```

Or with pipx:

```sh
pipx install . --include-deps --force --editable
```

## Publish to PyPI

This project uses [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers) for secure, token-free publishing from GitHub Actions, with [uv](https://docs.astral.sh/uv) for building packages.

### Initial Setup (One-time)

Before publishing for the first time, you need to configure Trusted Publishing on PyPI:

1. Go to your project's page on PyPI: `https://pypi.org/manage/project/mdformat_mkdocs/settings/publishing/`
    - If the project doesn't exist yet, go to [PyPI's publishing page](https://pypi.org/manage/account/publishing) to add a "pending" publisher
1. Add a new Trusted Publisher with these settings:
    - **PyPI Project Name**: `mdformat_mkdocs`
    - **Owner**: `kyleking`
    - **Repository name**: `mdformat-mkdocs`
    - **Workflow name**: `tests.yml` (`.github/workflows/tests.yml`)
    - **Environment name**: `pypi`
1. Configure the GitHub Environment:
    - Go to your repository's `Settings` → `Environments`
    - Create an environment named `pypi`
    - (Recommended) Enable "Required reviewers" for production safety

### Publishing a Release

#### Option 1: Using commitizen (Recommended)

Use commitizen to automatically bump versions and create a commit with tag:

```sh
# Dry run to preview the version bump
tox -e py312-cz -- --dry-run

# Automatically bump version based on conventional commits
tox -e py312-cz

# Or manually specify the increment type
tox -e py312-cz -- --increment PATCH  # or MINOR or MAJOR

# Push the commit and tag
git push origin main --tags
```

Commitizen will automatically update versions in `pyproject.toml` and `mdformat_mkdocs/__init__.py`.

#### Option 2: Manual Version Bump

Update the versions in both `pyproject.toml` under `[project].version` and `mdformat_mkdocs/__init__.py` for `__version__`. Commit the change and push a tag in the form `vX.Y.Z` (for example, `v1.3.2` when the project version is `1.3.2`):

```sh
TAG=1.3.2
git add pyproject.toml mdformat_mkdocs/__init__.py
git commit -m "release: v$TAG"
git tag v$TAG
git push origin main --tags
```

The GitHub Action will automatically build and publish to PyPI using Trusted Publishers (no API tokens needed!).
