"""Plugins."""

from ._content_tabs import CONTENT_TAB_MARKERS, content_tabs_plugin
from ._mkdocs_admon import MKDOCS_ADMON_MARKERS, mkdocs_admon_plugin
from ._mkdocs_anchors import MKDOCS_ANCHORS_PREFIX, mkdocs_anchors_plugin
from ._mkdocstrings_crossreference import (
    MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
    mkdocstrings_crossreference_plugin,
)
from ._pymd_abbreviations import PYMD_ABBREVIATIONS_PREFIX, pymd_abbreviations_plugin
