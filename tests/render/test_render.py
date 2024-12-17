from pathlib import Path

import pytest
from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file

from mdformat_mkdocs.mdit_plugins import (
    material_admon_plugin,
    material_content_tabs_plugin,
    mkdocstrings_autorefs_plugin,
    mkdocstrings_crossreference_plugin,
    pymd_abbreviations_plugin,
)
from tests.helpers import print_text

FIXTURE_PATH = Path(__file__).parent / "fixtures"


def with_plugin(filename, plugins):
    return [(*fix, plugins) for fix in read_fixture_file(FIXTURE_PATH / filename)]


@pytest.mark.parametrize(
    ("line", "title", "text", "expected", "plugins"),
    [
        *with_plugin("material_admonitions.md", [material_admon_plugin]),
        *with_plugin(
            "material_content_tabs.md",
            [material_admon_plugin, material_content_tabs_plugin],
        ),
        *with_plugin("mkdocstrings_autorefs.md", [mkdocstrings_autorefs_plugin]),
        *with_plugin("pymd_abbreviations.md", [pymd_abbreviations_plugin]),
        *with_plugin(
            "mkdocstrings_crossreference.md",
            [mkdocstrings_crossreference_plugin],
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
