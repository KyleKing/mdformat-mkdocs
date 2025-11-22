# Development

## API Documentation

A collection of useful resources to reference when developing new features:

- [`markdown-it-py` documentation](https://markdown-it-py.readthedocs.io/en/latest/using.html)
- [`markdown-it` (JS) documentation](https://markdown-it.github.io/markdown-it)
- [`mdformat` documentation](https://mdformat.readthedocs.io/en/stable)

## Local Development

This package utilizes [mise](https://mise.jdx.dev) ([installation guide](https://github.com/jdx/mise/blob/79367a4d382d8ab4cb76afef357d0db4afa33866/docs/installing-mise.md)) for dependency management, [prek](https://github.com/j178/prek) for fast pre-commit hooks, [uv](https://docs.astral.sh/uv) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To install the development dependencies:

```bash
brew install mise  # or see the installation alternatives above

# Install dependencies from mist.toml
mise trust
mise install

# Configure prek
prek install -f
```

To run all tox environments:

```bash
tox
```

or to run specific commands:

```bash
tox -e test
tox -e prek
tox -e hook-min

tox list
```

To run all pre-commit steps:

```sh
prek run --all
```

`pytest-watcher` is configured in `pyproject.toml` for `[tool.pytest-watcher]` to continuously run tests

```sh
ptw .
```

## Local uv/pipx integration testing

Run the local code with `uv tool` (requires `uv` installed globally and first in `$PATH`, e.g. `brew install uv` or `mise use uv --global`)

```sh
uv tool install 'mdformat>=0.7.19' --force --with=.

# Then navigate to a different directory and check that the editable version was installed
cd ~
mdformat --version
which mdformat
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

Use `commitizen` to automatically bump versions (in `pyproject.toml` and `mdformat_mkdocs/__init__.py`) and create a commit with tag:

```sh
# Dry run to preview the version bump
tox -e cz -- --dry-run

# Automatically bump version based on conventional commits
tox -e cz

# Or manually specify the increment type
tox -e cz -- --increment PATCH  # or MINOR or MAJOR

# Push the commit and tag
git push origin main --tags
```

The GitHub Action will automatically build and publish to PyPI using Trusted Publishers (no API tokens needed!).
