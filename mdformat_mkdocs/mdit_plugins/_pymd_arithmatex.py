"""Python-Markdown Extensions: Arithmatex (Math Support).

Uses existing mdit-py-plugins for LaTeX/MathJax mathematical expressions.

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

from typing import TYPE_CHECKING

from mdit_py_plugins.amsmath import amsmath_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.texmath import texmath_plugin

if TYPE_CHECKING:
    from markdown_it import MarkdownIt

# Token types from the plugins
DOLLARMATH_INLINE = "math_inline"
DOLLARMATH_BLOCK = "math_block"
TEXMATH_INLINE = "math_inline_double"
TEXMATH_BLOCK = "math_block_eqno"
AMSMATH_BLOCK = "amsmath"


def pymd_arithmatex_plugin(md: MarkdownIt) -> None:
    """Register Arithmatex support using existing mdit-py-plugins.

    This is a convenience wrapper that configures three existing plugins:
    - dollarmath_plugin: for $...$ and $$...$$
    - texmath_plugin: for \\(...\\) and \\[...\\]
    - amsmath_plugin: for \\begin{env}...\\end{env}
    """
    # Dollar syntax: $...$ and $$...$$
    # Defaults provide smart dollar mode (no digits/space adjacent to $)
    md.use(dollarmath_plugin)

    # Bracket syntax: \(...\) and \[...\]
    md.use(texmath_plugin, delimiters="brackets")

    # LaTeX environments: \begin{env}...\end{env}
    md.use(amsmath_plugin)


# For backwards compatibility, export the same prefixes
# Map to the actual token types created by the plugins
PYMD_ARITHMATEX_INLINE_PREFIX = DOLLARMATH_INLINE  # "math_inline"
PYMD_ARITHMATEX_BLOCK_PREFIX = DOLLARMATH_BLOCK    # "math_block"
