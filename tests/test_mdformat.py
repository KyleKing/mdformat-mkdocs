from pathlib import Path

import mdformat


def test_mdformat_text():
    """Verify that using mdformat works as expected."""
    pth = Path(__file__).parent / "pre-commit-test.md"
    content = pth.read_text()

    result = mdformat.text(content, extensions={"mkdocs"})

    pth.write_text(result)  # Easier to debug with git
    assert result == content, "Differences found in format. Review in git."
