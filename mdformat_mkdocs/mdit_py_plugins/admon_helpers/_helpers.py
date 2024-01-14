from __future__ import annotations

from contextlib import contextmanager, suppress
import re
from typing import (
    TYPE_CHECKING,
    Callable,
    Generator,
    List,
    NamedTuple,
    Sequence,
    Set,
    Tuple,
    Union,
)

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdit_py_plugins.utils import is_code_block

if TYPE_CHECKING:
    from markdown_it.renderer import RendererProtocol
    from markdown_it.ruler import RuleOptionsType
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict


def _get_multiple_tags(meta_text: str) -> Tuple[List[str], str]:
    """Check for multiple tags when the title is double quoted."""
    re_tags = re.compile(r'^\s*(?P<tokens>[^"]+)\s+"(?P<title>.*)"\S*$')
    match = re_tags.match(meta_text)
    if match:
        tags = match["tokens"].strip().split(" ")
        return [tag.lower() for tag in tags], match["title"]
    raise ValueError("No match found for parameters")


def parse_tag_and_title(admon_meta_text: str) -> Tuple[List[str], str]:
    """Separate the tag name from the admonition title."""
    meta_text = admon_meta_text.strip()
    if not meta_text:
        return [""], ""

    with suppress(ValueError):
        return _get_multiple_tags(meta_text)

    tag, *_title = meta_text.split(" ")
    joined = " ".join(_title)

    title = ""
    if not joined:
        title = tag.title()
    elif joined != '""':  # Specifically check for no title
        title = joined
    return [tag.lower()], title


def validate_admon_meta(meta_text: str) -> bool:
    """Validate the presence of the tag name after the marker."""
    tag = meta_text.strip().split(" ", 1)[-1] or ""
    return bool(tag)


class AdmonState(NamedTuple):
    """Frozen state."""

    parentType: str
    lineMax: int
    blkIndent: int


class Admonition(NamedTuple):
    """Admonition data for rendering."""

    old_state: AdmonState
    marker: str
    markup: str
    meta_text: str
    next_line: int


def search_admon_end(state: StateBlock, start_line: int, end_line: int) -> int:
    was_empty = False

    # Search for the end of the block
    next_line = start_line
    while True:
        next_line += 1
        if next_line >= end_line:
            # unclosed block should be autoclosed by end of document.
            # also block seems to be autoclosed by end of parent
            break
        pos = state.bMarks[next_line] + state.tShift[next_line]
        maximum = state.eMarks[next_line]
        is_empty = state.sCount[next_line] < state.blkIndent

        # two consecutive empty lines autoclose the block
        if is_empty and was_empty:
            break
        was_empty = is_empty

        if pos < maximum and state.sCount[next_line] < state.blkIndent:
            # non-empty line with negative indent should stop the block:
            # - !!!
            #  test
            break

    return next_line


def parse_possible_admon_factory(
    markers: Set[str],
) -> Callable[[StateBlock, int, int, bool], Union[Admonition, bool]]:
    expected_marker_len = 3  # Regardless of extra chars, block indent stays the same
    marker_first_chars = {_m[0] for _m in markers}
    max_marker_len = max(len(_m) for _m in markers)

    def parse_possible_admon(
        state: StateBlock, start_line: int, end_line: int, silent: bool
    ) -> Union[Admonition, bool]:
        if is_code_block(state, start_line):
            return False

        start = state.bMarks[start_line] + state.tShift[start_line]
        maximum = state.eMarks[start_line]

        # Exit quickly on a non-match for first char
        if state.src[start] not in marker_first_chars:
            return False

        # Check out the rest of the marker string
        marker = ""
        marker_len = max_marker_len
        while marker_len > 0:
            marker_pos = start + marker_len
            markup = state.src[start:marker_pos]
            if markup in markers:
                marker = markup
                break
            marker_len -= 1
        else:
            return False

        admon_meta_text = state.src[marker_pos:maximum]
        if not validate_admon_meta(admon_meta_text):
            return False
        # Since start is found, we can report success here in validation mode
        if silent:
            return True

        old_state = AdmonState(
            parentType=state.parentType,
            lineMax=state.lineMax,
            blkIndent=state.blkIndent,
        )
        state.parentType = "admonition"

        blk_start = marker_pos
        while blk_start < maximum and state.src[blk_start] == " ":
            blk_start += 1

        # Correct block indentation when extra marker characters are present
        marker_alignment_correction = expected_marker_len - len(marker)
        state.blkIndent += blk_start - start + marker_alignment_correction

        next_line = search_admon_end(state, start_line, end_line)

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = next_line
        return Admonition(
            old_state=old_state,
            marker=marker,
            markup=markup,
            meta_text=admon_meta_text,
            next_line=next_line,
        )

    return parse_possible_admon


@contextmanager
def new_token(state: StateBlock, name: str, kind: str) -> Generator[Token, None, None]:
    yield state.push(f"{name}_open", kind, 1)
    state.push(f"{name}_close", kind, -1)


def format_python_markdown_admon_markup(
    state: StateBlock,
    start_line: int,
    admonition: Admonition,
) -> None:
    tags, title = parse_tag_and_title(admonition.meta_text)
    tag = tags[0]

    with new_token(state, "admonition", "div") as token:
        token.markup = admonition.markup
        token.block = True
        token.attrs = {"class": " ".join(["admonition", *tags])}
        token.meta = {"tag": tag}
        token.info = admonition.meta_text
        token.map = [start_line, admonition.next_line]

        if title:
            title_markup = f"{admonition.markup} {tag}"
            with new_token(state, "admonition_title", "p") as token:
                token.markup = title_markup
                token.attrs = {"class": "admonition-title"}
                token.map = [start_line, start_line + 1]

                token = state.push("inline", "", 0)
                token.content = title
                token.map = [start_line, start_line + 1]
                token.children = []

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    state.parentType = admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.blkIndent = admonition.old_state.blkIndent
    state.line = admonition.next_line


def default_render(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    _options: OptionsDict,
    env: EnvType,
) -> str:
    """Default render if not specified."""
    return self.renderToken(tokens, idx, _options, env)  # type: ignore


RenderType = Callable[..., str]


def admon_plugin_factory(
    prefix: str, logic: Callable[[StateBlock, int, int, bool], bool]
) -> Callable[[MarkdownIt, None | RenderType], None]:
    def admon_plugin(md: MarkdownIt, render: None | RenderType = None) -> None:
        """Plugin to use
        `python-markdown style admonitions
        <https://python-markdown.github.io/extensions/admonition>`_.

        .. code-block:: md

            !!! note
                *content*

        `And mkdocs-style collapsible blocks
        <https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks>`_.

        .. code-block:: md

            ???+ note
                *content*

        Note, this is ported from
        `markdown-it-admon
        <https://github.com/commenthol/markdown-it-admon>`_.
        """
        render = render or default_render

        md.add_render_rule(f"{prefix}_open", render)
        md.add_render_rule(f"{prefix}_close", render)
        md.add_render_rule(f"{prefix}_title_open", render)
        md.add_render_rule(f"{prefix}_title_close", render)

        options: RuleOptionsType = {
            "alt": ["paragraph", "reference", "blockquote", "list"]
        }
        md.block.ruler.before("fence", prefix, logic, options)

    return admon_plugin
