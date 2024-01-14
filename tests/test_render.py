from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdformat_mkdocs.mdit_py_plugins.admon import admon_plugin
from mdformat_mkdocs.mdit_py_plugins.admon_mkdocs import admon_mkdocs_plugin
from mdformat_mkdocs.mdit_py_plugins.content_tabs import content_tabs_plugin
from .helpers import print_text

FIXTURE_PATH = Path(__file__).parent


def with_plugin(filename, plugins):
    return [(*fix, plugins) for fix in read_fixture_file(FIXTURE_PATH / filename)]


@pytest.mark.parametrize(
    "line,title,text,expected,plugins",
    [
        *with_plugin("fixtures-admon.md", [admon_plugin]),
        *with_plugin("fixtures-admon.md", [admon_mkdocs_plugin]),
        *with_plugin("fixtures-admon-mkdocs.md", [admon_mkdocs_plugin]),
        *with_plugin(
            "fixtures-mkdocs-content-tabs.md",
            [admon_mkdocs_plugin, content_tabs_plugin],
        ),
    ],
)
def test_render(line, title, text, expected, plugins):
    md = MarkdownIt("commonmark")
    for plugin in plugins:
        md.use(plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    output = md.render(text)
    print_text(output, expected, show_whitespace=False)
    assert output.rstrip() == expected.rstrip()
