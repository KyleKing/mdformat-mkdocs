from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

# from mdformat_mkdocs.mdit_py_plugins.admon_mkdocs import admon_mkdocs_plugin
from mdformat_mkdocs.mdit_py_plugins.admon_helpers import (
    admon_plugin_wrapper,
    admonition_logic,
)
from .helpers import print_text

# HACK: used to test refactoring against regressions
admon_mkdocs_plugin = admon_plugin_wrapper("admonition_mkdocs", admonition_logic)

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
