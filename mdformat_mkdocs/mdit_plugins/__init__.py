"""Plugins."""

from ._material_admon import MATERIAL_ADMON_MARKERS, material_admon_plugin
from ._material_content_tabs import (
    MATERIAL_CONTENT_TAB_MARKERS,
    material_content_tabs_plugin,
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
from ._pymd_abbreviations import PYMD_ABBREVIATIONS_PREFIX, pymd_abbreviations_plugin

__all__ = (
    "MATERIAL_ADMON_MARKERS",
    "MATERIAL_CONTENT_TAB_MARKERS",
    "MKDOCSTRINGS_AUTOREFS_PREFIX",
    "MKDOCSTRINGS_CROSSREFERENCE_PREFIX",
    "MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX",
    "PYMD_ABBREVIATIONS_PREFIX",
    "material_admon_plugin",
    "material_content_tabs_plugin",
    "mkdocstrings_autorefs_plugin",
    "mkdocstrings_crossreference_plugin",
    "pymd_abbreviations_plugin",
)
