# Prevention Strategies

Five remaining strategies to prevent the kinds of issues that have appeared in the past two years, ordered by priority. See `docs/downstream.md` for the issue-theme analysis behind these.

Already implemented: Hypothesis property-based testing (`tox -e test`) and canary testing on real repos (`tox -e canary`).

## 1. Centralized Bracket Tokenization

Categories prevented: bracket/escape collisions (#72, #74, #75, #80)

The biggest systemic issue: multiple regex-based plugins independently match `[...]` patterns, causing collisions. Instead of each plugin applying its own regex in isolation:

- Introduce a single tokenization pass that classifies all bracket pairs before any plugin processes them
- Each bracket pair gets a kind: link, cross-reference, attribute list, escaped, math
- Each plugin operates only on its classified spans, eliminating cross-plugin collisions

This is the highest architectural ROI change but also the highest effort.

## 2. Unit Tests for `_normalize_list` Internals

Categories prevented: list indentation bugs (#6, #7, #9, #13, #35, #50, #63)

The `ParsedText` debug fields (`debug_original_lines`, `debug_block_indents`) exist but no unit tests use them. Target:

- `Syntax.from_content()`: edge cases of content classification
- `acc_line_results()`: parent/peer detection
- `_parse_code_block` / `_parse_html_line`: state machine transitions
- `_trim_semantic_indent`: all `SemanticIndent` variants
- `_format_new_indent`: indent calculation for various `LineResult` shapes

Low effort, high value for the most persistent bug category.

## 3. Typed Config and Indent Types

Categories prevented: list indentation off-by-one, config misuse

Two changes:

1. Replace `get_conf` returning `Any` with a frozen dataclass:

    ```python
    @dataclass(frozen=True)
    class MkDocsConfig:
        ignore_missing_references: bool = False
        align_semantic_breaks_in_lists: bool = False
        no_mkdocs_math: bool = False
    ```

1. Replace raw `str` indents with a typed representation to catch off-by-one errors at the type level (e.g., `NewType("Indent", str)` or a dataclass with `depth: int`).

Low effort.

## 4. Mutation Testing

Categories prevented: bracket/escape regex issues (#72, #74, #75), insufficient test coverage

Use `mutmut` to verify that tests detect when regex patterns are altered. Many bracket-escaping bugs involved regexes that were too broad, and mutation testing would flag insufficient coverage of regex boundary conditions.

Low effort to set up, ongoing value.

## 5. Decompose `_normalize_list.py`

Categories prevented: list indentation bugs (#6, #7, #9, #13, #35, #50, #63)

The ~500-line state machine handles too many concerns. Split into:

- `_list_parser.py`: pure parsing (`ParsedLine`, `LineResult`, `acc_line_results`)
- `_block_tracker.py`: code/HTML block state tracking
- `_indent_formatter.py`: indent normalization and semantic breaks
- `_list_formatter.py`: bullet/number normalization

Each piece becomes independently testable with simpler fixtures. Medium effort, enables better unit testing (strategy 2).
