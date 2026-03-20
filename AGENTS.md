# AGENTS.md

## Fixing Issues (Test-Driven Development)

1. **Add failing test** in `tests/format/fixtures/` (format: description, input, expected output separated by `.`)
1. **Run test**: `tox -e test -- -vv`
1. **Fix code**: implement minimal fix
1. **Verify**: `tox -e test -- --snapshot-update`
1. **Full suite**: `tox`

## Testing

```bash
# Run all tests using tox
tox

# Run tests with coverage (Python 3.14 - current version)
tox -e test

# Run tests with coverage (Python 3.10 - minimum version)
tox -e test-min

# Run specific tests with pytest flags
tox -e test -- --exitfirst --failed-first --new-first -vv --snapshot-update
```

## Linting and Formatting

```bash
# Run all pre-commit hooks (using prek)
tox -e prek
# Or run directly with prek
prek run --all

# Run ruff for linting and formatting
tox -e ruff
# With unsafe fixes
tox -e ruff -- --unsafe-fixes
```

## Type Checking

```bash
# Run mypy type checking
tox -e type
```

## Canary Testing (Real Downstream Repos)

```bash
# Run mdformat --check against all tracked downstream repos
tox -e canary

# Test a subset by name
tox -e canary -- uv ruff
```

Clones real consumer repos (ruff, uv, vizro, etc.) via git sparse checkout and runs
`mdformat --check` against their docs. Not in the default `tox` run — invoke explicitly
before releasing to catch integration regressions that synthetic fixtures miss.

## Pre-commit Hook Testing

```bash
# Test the plugin as a pre-commit hook
tox -e hook-min
```

## One-Off Testing

```bash
# Create a development environment with local code installed
tox devenv .venv

# Test mdformat on inline content
echo '- \[test\]: value' | .venv/bin/mdformat - --extension mkdocs 2>&1

# Test mdformat on a specific file
.venv/bin/mdformat tests/pre-commit-test.md --extension mkdocs

# Run Python code with local package installed
.venv/bin/python3 << 'PYTHON'
import mdformat
output = mdformat.text("- \[test\]: value", extensions={"mkdocs"})
print(output)
PYTHON
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

- **Do not use `uv` commands**—there is no `uv.lock` file. Always use `tox` (installed via mise and available on PATH) which manages environments and dependencies.

## mdformat-mkdocs Specific Guidance

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
