"""Ignore beartype warnings from tests."""

from contextlib import suppress

with suppress(ImportError):  # Only suppress beartype warnings when installed
    from warnings import filterwarnings

    from beartype.roar import (
        BeartypeClawDecorWarning,
        BeartypeDecorHintPep585DeprecationWarning,
    )

    filterwarnings("ignore", category=BeartypeClawDecorWarning)
    filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
