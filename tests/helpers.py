from mdformat_mkdocs._helpers import separate_indent  # noqa: PLC2701

_SHOW_TEXT = True  # PLANNED: Make configurable based on pytest CLI


def _print(content: str, show_whitespace: bool) -> None:
    for line in content.split("\n"):
        indent, content = separate_indent(line)
        visible_indents = indent.replace(" ", "→").replace("\t", "➤")
        print((visible_indents if show_whitespace else indent) + content)


def print_text(output: str, expected: str, show_whitespace: bool = False) -> None:
    if _SHOW_TEXT:
        print("--  Output  --")
        _print(output.strip(), show_whitespace)
        print("-- Expected --")
        _print(expected.strip(), show_whitespace)
        print("--  <End>   --")
