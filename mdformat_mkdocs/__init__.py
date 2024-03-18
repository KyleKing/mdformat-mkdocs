"""An mdformat plugin for mkdocs."""

__version__ = "2.0.4"

# FYI see source code for available interfaces:
#   https://github.com/executablebooks/mdformat/blob/5d9b573ce33bae219087984dd148894c774f41d4/src/mdformat/plugins.py
from .plugin import POSTPROCESSORS, RENDERERS, add_cli_options, update_mdit
