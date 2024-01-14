from mdformat_mkdocs.plugin import _separate_indent

_SHOW_TEXT = True  # PLANNED: Make configurable based on pytest CLI


def _print(content: str, show_whitespace: bool) -> None:
    for line in content.split("\n"):
        indent, content = _separate_indent(line)
        visible_indents = indent.replace(" ", "→").replace("\t", "➤")
        print((visible_indents if show_whitespace else indent) + content)


def print_text(output: str, expected: str, show_whitespace: bool = True) -> None:
    if _SHOW_TEXT:
        print("--  Output  --")
        _print(output.strip(), show_whitespace)
        print("-- Expected --")
        _print(expected.strip(), show_whitespace)
        print("--  <End>   --")
