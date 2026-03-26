"""Plugins."""

from ._material_admon import MATERIAL_ADMON_MARKERS, material_admon_plugin
from ._material_content_tabs import (
    MATERIAL_CONTENT_TAB_MARKERS,
    material_content_tabs_plugin,
)
from ._material_deflist import (
    escape_deflist,
    material_deflist_plugin,
    render_material_definition_body,
    render_material_definition_list,
    render_material_definition_term,
)
from ._mkdocstrings_autorefs import (
    MKDOCSTRINGS_AUTOREFS_PREFIX,
    MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX,
    mkdocstrings_autorefs_plugin,
)
from ._mkdocstrings_crossreference import (
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
    mkdocstrings_crossreference_plugin,
)
from ._mkdocstrings_injection import (
    MKDOCSTRINGS_INJECTION_PREFIX,
    mkdocstrings_injection_plugin,
)
from ._pymd_abbreviations import PYMD_ABBREVIATIONS_PREFIX, pymd_abbreviations_plugin
from ._pymd_admon import pymd_admon_plugin
from ._pymd_arithmatex import (
    AMSMATH_BLOCK,
    DOLLARMATH_BLOCK,
    DOLLARMATH_BLOCK_LABEL,
    DOLLARMATH_INLINE,
    TEXMATH_BLOCK_EQNO,
    pymd_arithmatex_plugin,
)
from ._pymd_captions import PYMD_CAPTIONS_PREFIX, pymd_captions_plugin
from ._pymd_snippet import PYMD_SNIPPET_PREFIX, pymd_snippet_plugin
from ._python_markdown_attr_list import (
    PYTHON_MARKDOWN_ATTR_LIST_PREFIX,
    python_markdown_attr_list_plugin,
)
from ._spaced_url_link import SPACED_URL_LINK_PREFIX, spaced_url_link_plugin

__all__ = (
    "AMSMATH_BLOCK",
    "DOLLARMATH_BLOCK",
    "DOLLARMATH_BLOCK_LABEL",
    "DOLLARMATH_INLINE",
    "MATERIAL_ADMON_MARKERS",
    "MATERIAL_CONTENT_TAB_MARKERS",
    "MKDOCSTRINGS_AUTOREFS_PREFIX",
    "MKDOCSTRINGS_CROSSREFERENCE_PREFIX",
    "MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX",
    "MKDOCSTRINGS_INJECTION_PREFIX",
    "PYMD_ABBREVIATIONS_PREFIX",
    "PYMD_CAPTIONS_PREFIX",
    "PYMD_SNIPPET_PREFIX",
    "PYTHON_MARKDOWN_ATTR_LIST_PREFIX",
    "SPACED_URL_LINK_PREFIX",
    "TEXMATH_BLOCK_EQNO",
    "escape_deflist",
    "material_admon_plugin",
    "material_content_tabs_plugin",
    "material_deflist_plugin",
    "mkdocstrings_autorefs_plugin",
    "mkdocstrings_crossreference_plugin",
    "mkdocstrings_injection_plugin",
    "pymd_abbreviations_plugin",
    "pymd_admon_plugin",
    "pymd_arithmatex_plugin",
    "pymd_captions_plugin",
    "pymd_snippet_plugin",
    "python_markdown_attr_list_plugin",
    "render_material_definition_body",
    "render_material_definition_list",
    "render_material_definition_term",
    "spaced_url_link_plugin",
)
