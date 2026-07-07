import mdformat
import pytest

from tests.helpers import print_text

TICKET_019 = """Example python mkdocstring snippets

[package.module.object][]
[Object][package.module.object]

- [package.module.object][]
- [Object][package.module.object]
"""

# Backtick-wrapped autorefs (DeepLabCut dev-docs); escaped without the flag. See #80.
DLC_AUTOREFS = """The [`deeplabcut.pose_estimation_pytorch.models`][] package.

- [`deeplabcut.pose_estimation_pytorch.models.backbones`][]
- [Object][deeplabcut.pose_estimation_pytorch.models]
"""


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (TICKET_019, TICKET_019),
        (DLC_AUTOREFS, DLC_AUTOREFS),
    ],
    ids=["TICKET_019", "DLC_AUTOREFS"],
)
def test_ignore_missing_references(text, expected):
    output = mdformat.text(
        text,
        options={"ignore_missing_references": True},
        extensions={"mkdocs"},
    )
    print_text(output, expected)
    assert output == expected


def test_default_escapes_backtick_autorefs():
    """Without the flag, backtick-wrapped autorefs are escaped (the DeepLabCut bug)."""
    output = mdformat.text(DLC_AUTOREFS, extensions={"mkdocs"})
    assert r"\[`deeplabcut.pose_estimation_pytorch.models`\][]" in output
