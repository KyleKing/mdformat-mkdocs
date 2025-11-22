"""Python-Markdown Extensions: Arithmatex (Math Support).

Supports LaTeX/MathJax mathematical expressions using PyMdown Extensions Arithmatex syntax.

Inline math delimiters:
- $...$ (with smart_dollar rules: no whitespace adjacent to $)
- \\(...\\)

Block math delimiters:
- $$...$$
- \\[...\\]
- \\begin{env}...\\end{env}

Docs: <https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex>

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from mdit_py_plugins.utils import is_code_block

from mdformat_mkdocs._synced.admon_factories import new_token

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_block import StateBlock
    from markdown_it.rules_inline import StateInline

# Inline math patterns (adapted from Arithmatex)
# Smart dollar: requires non-whitespace adjacent to $
_INLINE_DOLLAR_SMART = re.compile(
    r"(?:(?<!\\)((?:\\{2})+)(?=\$)|(?<!\\)(\$)(?!\s)((?:\\.|[^\$])+?)(?<!\s)(?:\$))"
)

# Parenthesis notation: \(...\)
_INLINE_PAREN = re.compile(
    r"(?:(?<!\\)((?:\\{2})+?)(?=\\[(])|(?<!\\)(\\[(])((?:\\[^)]|[^\\])+?)(\\[)]))"
)

# Block math patterns
# Double dollar: $$...$$
_BLOCK_DOLLAR = re.compile(r"^[$]{2}[ \t]*$")

# Square brackets: \[...\]
_BLOCK_SQUARE = re.compile(r"^\\[\[][ \t]*$")
_BLOCK_SQUARE_END = re.compile(r"^\\[\]][ \t]*$")

# LaTeX environments: \begin{env}...\end{env}
_BLOCK_BEGIN = re.compile(r"^\\begin\{(?P<env>[a-z]+\*?)\}[ \t]*$")

PYMD_ARITHMATEX_INLINE_PREFIX = "pymd_arithmatex_inline"
PYMD_ARITHMATEX_BLOCK_PREFIX = "pymd_arithmatex_block"


def _pymd_arithmatex_inline(state: StateInline, silent: bool) -> bool:
    """Parse inline math expressions ($...$ or \\(...\\))."""
    # Try dollar sign first
    match = _INLINE_DOLLAR_SMART.match(state.src[state.pos : state.posMax])
    if match:
        # Check if it's an escaped sequence (even number of backslashes before $)
        if match.group(1):  # Even backslashes before $, not math
            return False

        if silent:
            return True

        math_content = match.group(3)  # The content between $...$
        original_pos = state.pos

        with new_token(state, PYMD_ARITHMATEX_INLINE_PREFIX, "span") as token:
            token.meta = {"delimiter": "$", "content": math_content}
            token.content = f"${math_content}$"

        state.pos = original_pos + match.end()
        return True

    # Try parenthesis notation
    match = _INLINE_PAREN.match(state.src[state.pos : state.posMax])
    if match:
        # Check if it's an escaped sequence
        if match.group(1):  # Even backslashes before \(, not math
            return False

        if silent:
            return True

        math_content = match.group(3)  # The content between \(...\)
        original_pos = state.pos

        with new_token(state, PYMD_ARITHMATEX_INLINE_PREFIX, "span") as token:
            token.meta = {"delimiter": "paren", "content": math_content}
            token.content = f"\\({math_content}\\)"

        state.pos = original_pos + match.end()
        return True

    return False


def _get_line_content(state: StateBlock, line: int) -> str:
    """Get the content of a line."""
    if line >= state.lineMax:
        return ""
    start = state.bMarks[line] + state.tShift[line]
    maximum = state.eMarks[line]
    return state.src[start:maximum]


def _pymd_arithmatex_block(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    """Parse block math expressions ($$...$$, \\[...\\], \\begin{}...\\end{})."""
    if is_code_block(state, start_line):
        return False

    # Check if line is indented (would be code block)
    if state.sCount[start_line] - state.blkIndent >= 4:
        return False

    first_line = _get_line_content(state, start_line)

    # Try to match block delimiters
    delimiter_type = None
    env_name = None

    if _BLOCK_DOLLAR.match(first_line):
        delimiter_type = "dollar"
        end_pattern = _BLOCK_DOLLAR
    elif _BLOCK_SQUARE.match(first_line):
        delimiter_type = "square"
        end_pattern = _BLOCK_SQUARE_END
    else:
        begin_match = _BLOCK_BEGIN.match(first_line)
        if begin_match:
            delimiter_type = "begin"
            env_name = begin_match.group("env")
            end_pattern = re.compile(rf"^\\end\{{{re.escape(env_name)}\}}[ \t]*$")
        else:
            return False

    if silent:
        return True

    # Find the end of the math block
    current_line = start_line + 1
    content_lines: list[str] = []
    found_end = False

    while current_line < end_line:
        line_content = _get_line_content(state, current_line)

        # Check for end delimiter
        if end_pattern.match(line_content):
            found_end = True
            break

        # Check for empty line (not allowed in math blocks)
        if not line_content.strip():
            # Empty line found, not a valid math block
            return False

        content_lines.append(line_content)
        current_line += 1

    # Must find closing delimiter
    if not found_end:
        return False

    # Construct the full math block content
    if delimiter_type == "dollar":
        full_content = "$$\n" + "\n".join(content_lines) + "\n$$"
    elif delimiter_type == "square":
        full_content = "\\[\n" + "\n".join(content_lines) + "\n\\]"
    elif delimiter_type == "begin":
        full_content = (
            f"\\begin{{{env_name}}}\n" + "\n".join(content_lines) + f"\n\\end{{{env_name}}}"
        )
    else:
        return False

    # Create the token
    with new_token(state, PYMD_ARITHMATEX_BLOCK_PREFIX, "div"):
        tkn_inline = state.push("inline", "", 0)
        tkn_inline.content = full_content
        tkn_inline.map = [start_line, current_line + 1]
        tkn_inline.children = []

    state.line = current_line + 1

    return True


def pymd_arithmatex_plugin(md: MarkdownIt) -> None:
    """Register the Arithmatex plugin with markdown-it."""
    # Register inline math parser
    md.inline.ruler.before(
        "escape",
        PYMD_ARITHMATEX_INLINE_PREFIX,
        _pymd_arithmatex_inline,
    )

    # Register block math parser
    md.block.ruler.before(
        "fence",
        PYMD_ARITHMATEX_BLOCK_PREFIX,
        _pymd_arithmatex_block,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )
