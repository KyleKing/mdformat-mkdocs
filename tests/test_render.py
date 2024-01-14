from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdformat_mkdocs.mdit_py_plugins.admon import admon_plugin
from mdformat_mkdocs.mdit_py_plugins.admon_mkdocs import admon_mkdocs_plugin
from .helpers import print_text

FIXTURE_PATH = Path(__file__).parent


@pytest.mark.parametrize(
    "line,title,text,expected,plugin",
    (
        [
            *read_fixture_file(FIXTURE_PATH / "fixtures-admon.md"),
            admon_plugin,
        ],
        [
            *read_fixture_file(FIXTURE_PATH / "fixtures-admon.md"),
            admon_mkdocs_plugin,
        ],
        [
            *read_fixture_file(FIXTURE_PATH / "fixtures-admon-mkdocs.md"),
            admon_mkdocs_plugin,
        ],
    ),
)
def test_render(line, title, text, expected, plugin):
    md = MarkdownIt("commonmark").use(plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    output = md.render(text)
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()
