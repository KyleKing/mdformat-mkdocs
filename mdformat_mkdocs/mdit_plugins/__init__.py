"""Plugins."""

from ._material_admon import MATERIAL_ADMON_MARKERS, material_admon_plugin
from ._material_content_tabs import (
    MATERIAL_CONTENT_TAB_MARKERS,
    material_content_tabs_plugin,
)
from ._mkdocstrings_autorefs import (
    MKDOCSTRINGS_AUTOREFS_PREFIX,
    MKDOCSTRINGS_HEADER_AUTOREFS_PREFIX,
    mkdocstrings_autorefs_plugin,
)
from ._mkdocstrings_crossreference import (
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
    mkdocstrings_crossreference_plugin,
)
from ._pymd_abbreviations import PYMD_ABBREVIATIONS_PREFIX, pymd_abbreviations_plugin
