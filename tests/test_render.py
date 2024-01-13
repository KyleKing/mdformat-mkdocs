from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

# from mdformat_mkdocs.mdit_py_plugins.admon_mkdocs import admon_mkdocs_plugin
# PLANNED: used to test refactoring against regressions
from mdformat_mkdocs.mdit_py_plugins.admon_helpers import (
    admon_plugin as admon_mkdocs_plugin,
)
from .helpers import print_text

FIXTURE_PATH = Path(__file__).parent


@pytest.mark.parametrize(
    "line,title,text,expected",
    read_fixture_file(FIXTURE_PATH / "fixtures-admon.md"),
)
def test_render(line, title, text, expected):
    md = MarkdownIt("commonmark").use(admon_mkdocs_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    output = md.render(text)
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()
