from mdformat_mkdocs.plugin import _separate_indent

_SHOW_TEXT = True  # PLANNED: Make configurable based on pytest CLI


def _show_indent(content: str) -> None:
    for line in content.split("\n"):
        indent, content = _separate_indent(line)
        print(indent.replace(" ", "→").replace("\t", "➤") + content)


def print_text(output: str, expected: str) -> None:
    if _SHOW_TEXT:
        print("--  Output  --")
        _show_indent(output.strip())
        print("-- Expected --")
        _show_indent(expected.strip())
        print("--  <End>   --")
