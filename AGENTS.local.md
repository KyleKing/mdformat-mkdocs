## Project-Specific Notes

- This project layers `syrupy` on top of the fixtures in `tests/format/fixtures/` and `tests/render/fixtures/`, so `--snapshot-update` applies
- `tests/test_inline_rule_protocol.py`: unit tests for the `StateInline` rule contract

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
