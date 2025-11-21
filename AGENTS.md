# AGENTS.md

## Testing

```bash
# Run all tests using tox
tox

# Run tests with coverage (Python 3.10)
tox -e py310-test

# Run tests with coverage (Python 3.12)
tox -e py312-test

# Run specific tests with pytest flags
tox -e py312-test -- --exitfirst --failed-first --new-first -vv --snapshot-update
```

## Linting and Formatting

```bash
# Run all pre-commit hooks (using prek)
tox -e py312-prek
# Or run directly with prek
prek run --all

# Run ruff for linting and formatting
tox -e py312-ruff
# With unsafe fixes
tox -e py312-ruff -- --unsafe-fixes
```

## Type Checking

```bash
# Run mypy type checking
tox -e py312-type
```

## Pre-commit Hook Testing

```bash
# Test the plugin as a pre-commit hook
tox -e py310-hook
```

## Architecture

### Plugin System

The package implements mdformat's plugin interface with up to four key exports in `__init__.py`:

- `update_mdit`: Registers markdown-it parser extensions
- `add_cli_argument_group`: Optionally adds CLI flags
- `RENDERERS`: Maps syntax tree node types to render functions
- `POSTPROCESSORS`: Post-processes rendered output (list normalization, inline wrapping, deflist escaping)

### Core Components

**mdformat_mkdocs/plugin.py**

- Entry point that configures the mdformat plugin, registers all mdit_plugins, defines custom renders, and handles CLI configuration options

**mdformat_mkdocs/\_normalize_list.py**

- Complex list indentation normalization logic
- Enforces 4-space indentation (MkDocs standard) instead of mdformat's default 2-space
- Handles semantic line breaks with 3-space alignment for numbered lists when `--align-semantic-breaks-in-lists` is enabled
- Parses list structure, code blocks, HTML blocks, and nested content
- Uses functional programming patterns with `map_lookback` for stateful line processing

**mdformat_mkdocs/mdit_plugins/**

- Each file implements a markdown-it plugin for specific MkDocs/Python-Markdown syntax
- Plugins parse syntax into tokens during the parsing phase
- Corresponding renderers in `plugin.py` convert tokens back to formatted markdown

**mdformat_mkdocs/\_helpers.py**

- Shared utilities: `MKDOCS_INDENT_COUNT` (4 spaces), `separate_indent`, `get_conf`
- Configuration reading from mdformat options (CLI, TOML, or API)

**mdformat_mkdocs/\_synced/**

- Contains code synced from other projects (admonition factories)
- Check the README in these directories before modifying

### Configuration Options

Configuration can be passed via:

1. Example CLI arguments: `--cli-argument`
1. Example TOML config file (`.mdformat.toml`):
    ```toml
    [plugin.mkdocs]
    cli_argument = true
    ```
1. API: `mdformat.text(content, extensions={"mkdocs"}, options={...})`

### Testing Strategy

**Snapshot Testing**

- Uses `syrupy` for snapshot testing
- Test fixtures in `tests/format/fixtures/` and `tests/render/fixtures/`
- Main test file: `tests/test_mdformat.py` verifies idempotent formatting against `tests/pre-commit-test.md`

**Test Organization**

- `tests/format/`: Tests formatting output (input markdown → formatted markdown)
- `tests/render/`: Tests HTML rendering (markdown → HTML via markdown-it)

## Development Notes

- This project uses `flit` as the build backend
- Uses `tox` for test automation with multiple Python versions (3.10, 3.12)
- Pre-commit is configured but the project now uses `prek` (faster alternative)
- Python 3.10+ is required (see `requires-python` in `pyproject.toml`)
- Version is defined in `mdformat_mkdocs/__init__.py` as `__version__`

### Special Handling

**List Indentation**

- MkDocs requires 4-space indentation for nested list items
- When `--align-semantic-breaks-in-lists` is enabled, continuation lines in ordered lists use 3-space indent (align with text after "1. ")
- The `_normalize_list.py` module handles this complex logic with state machines tracking code blocks, HTML blocks, and list nesting

**Link References**

- By default, escapes undefined link references `[foo]` → `\[foo\]`
- With `--ignore-missing-references`, leaves them as-is (required for mkdocstrings dynamic references)

**Definition Lists**

- Material for MkDocs definition lists require blank line between term and definition
- Handled by `_material_deflist.py` plugin and special rendering in `plugin.py`
