_SHOW_TEXT = True  # PLANNED: Make configurable based on pytest CLI


def print_text(output: str, expected: str) -> None:
    if _SHOW_TEXT:
        print("--  Output  --")
        print(output.strip())
        print("-- Expected --")
        print(expected.strip())
        print("--  <End>   --")
