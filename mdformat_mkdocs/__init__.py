"""An mdformat plugin for mkdocs."""

__version__ = "1.2.0"

from .plugin import (  # noqa: F401
    POSTPROCESSORS,
    RENDERERS,
    add_cli_options,
    update_mdit,
)
