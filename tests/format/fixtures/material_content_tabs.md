Do not modify multi-line code from: https://github.com/KyleKing/mdformat-mkdocs/issues/23
.
=== "duty"
    ```python title="duties.py"
    @duty(silent=True)
    def coverage(ctx):
        ctx.run("coverage combine", nofail=True)
        ctx.run("coverage report --rcfile=config/coverage.ini", capture=False)
        ctx.run("coverage html --rcfile=config/coverage.ini")


    @duty
    def test(ctx, match: str = ""):
        py_version = f"{sys.version_info.major}{sys.version_info.minor}"
        os.environ["COVERAGE_FILE"] = f".coverage.{py_version}"
        ctx.run(
            ["pytest", "-c", "config/pytest.ini", "-n", "auto", "-k", match, "tests"],
            title="Running tests",
        )
    ```
.
=== "duty"

    ```python title="duties.py"
    @duty(silent=True)
    def coverage(ctx):
        ctx.run("coverage combine", nofail=True)
        ctx.run("coverage report --rcfile=config/coverage.ini", capture=False)
        ctx.run("coverage html --rcfile=config/coverage.ini")


    @duty
    def test(ctx, match: str = ""):
        py_version = f"{sys.version_info.major}{sys.version_info.minor}"
        os.environ["COVERAGE_FILE"] = f".coverage.{py_version}"
        ctx.run(
            ["pytest", "-c", "config/pytest.ini", "-n", "auto", "-k", match, "tests"],
            title="Running tests",
        )
    ```
.
