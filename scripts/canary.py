"""Run mdformat idempotency checks against real downstream repos (canary testing)."""

# ruff: noqa: T201, S603, S607

from __future__ import annotations

import difflib
import subprocess  # noqa: S404
import sys
from dataclasses import dataclass
from pathlib import Path

import mdformat


@dataclass(frozen=True)
class Repo:
    """A downstream repository to check for idempotent mdformat output."""

    name: str
    url: str
    patterns: tuple[str, ...]
    excludes: tuple[str, ...] = ()

    @property
    def display(self) -> str:
        """Derive 'org/repo' from URL for display."""
        return "/".join(self.url.rstrip("/").split("/")[-2:])


@dataclass(frozen=True)
class FileResult:
    """Result of running mdformat idempotency check on a single file."""

    path: Path
    error: str | None = None
    diff: str | None = None

    @property
    def passed(self) -> bool:
        """Return True if the file produced no errors and no diff."""
        return self.error is None and self.diff is None


@dataclass(frozen=True)
class CheckResult:
    """Aggregated idempotency check results for a single repository."""

    repo: Repo
    file_results: tuple[FileResult, ...]

    @property
    def passed(self) -> bool:
        """Return True if all file results passed."""
        return all(r.passed for r in self.file_results)

    @property
    def output(self) -> str:
        """Format failure details for display."""
        lines: list[str] = []
        for result in self.file_results:
            if result.error:
                lines.extend((f"Error: {result.path}", f"  {result.error}"))
            elif result.diff:
                lines.append(f"Not idempotent: {result.path}")
                lines.extend(f"  {line}" for line in result.diff.splitlines()[:40])
        return "\n".join(lines)


_CANARY_DIR = Path(__file__).parent.parent / ".tox" / "canary" / "tmp"

# Each entry documents whether the repo uses mdformat-mkdocs and how.
# This context drives exclude decisions — if a repo excludes files from their
# own mdformat run, we mirror that here so canary tracks what they actually format.
#
# Repos that don't use mdformat are included as idempotency smoke tests: we
# verify our plugin doesn't crash or produce unstable output on real MkDocs content,
# even if that content has never been run through mdformat.
#
# To update: run `git -C .tox/canary/tmp/<name> show HEAD:.pre-commit-config.yaml`
# and check for mdformat hooks + their args/excludes.
_REPOS = [
    # Does NOT use mdformat. Included as a smoke test for real-world MkDocs content.
    Repo("ruff", "https://github.com/astral-sh/ruff", ("docs/**/*.md",)),
    # Uses mdformat-mkdocs[recommended]>=2.1.0 with --number in pre-commit (rev 1.0.0).
    # Explicitly excludes changelog.md and deprecated.md from their own hook — both
    # contain code blocks with embedded triple-backtick strings (e.g. """```json...""")
    # that trigger an idempotency edge case. Mirror their excludes here.
    Repo(
        "supervision",
        "https://github.com/roboflow/supervision",
        ("docs/**/*.md",),
        excludes=("docs/changelog.md", "docs/deprecated.md"),
    ),
    # Does NOT use mdformat. Included as a smoke test for real-world MkDocs content.
    Repo("ty", "https://github.com/astral-sh/ty", ("docs/**/*.md",)),
    # Does NOT use mdformat. Included as a smoke test for real-world MkDocs content.
    Repo(
        "ultralytics", "https://github.com/ultralytics/ultralytics", ("docs/**/*.md",)
    ),
    # Does NOT use mdformat. Included as a smoke test for real-world MkDocs content.
    Repo("uv", "https://github.com/astral-sh/uv", ("docs/**/*.md",)),
    # Does NOT use mdformat. Included as a smoke test for real-world MkDocs content.
    Repo("vizro", "https://github.com/mckinsey/vizro", ("docs/**/*.md",)),
]


def _clone_or_pull(repo: Repo, target_dir: Path) -> None:
    if not target_dir.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--filter=blob:none",
                "--sparse",
                repo.url,
                str(target_dir),
            ],
            check=True,
        )
        subprocess.run(
            ["git", "sparse-checkout", "set", "--no-cone", *repo.patterns],
            cwd=target_dir,
            check=True,
        )
    else:
        subprocess.run(
            ["git", "fetch", "--depth", "1", "origin"],
            cwd=target_dir,
            check=True,
        )
        subprocess.run(
            ["git", "reset", "--hard", "FETCH_HEAD"],
            cwd=target_dir,
            check=True,
        )


def _collect_files(repo: Repo, target_dir: Path) -> list[Path]:
    """Expand glob patterns and filter excludes, returning sorted file list."""
    included: set[Path] = set()
    for pattern in repo.patterns:
        included.update(target_dir.glob(pattern))

    excluded: set[Path] = set()
    for pattern in repo.excludes:
        excluded.update(target_dir.glob(pattern))

    return sorted(included - excluded)


def _check_file(path: Path) -> FileResult:
    """Verify mdformat produces idempotent output for a single file."""
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as err:
        return FileResult(path=path, error=f"read error: {err}")

    try:
        pass1 = mdformat.text(original, extensions={"mkdocs"})
        pass2 = mdformat.text(pass1, extensions={"mkdocs"})
    except Exception as err:
        return FileResult(path=path, error=f"mdformat error: {err}")

    if pass1 == pass2:
        return FileResult(path=path)

    diff = "".join(
        difflib.unified_diff(
            pass1.splitlines(keepends=True),
            pass2.splitlines(keepends=True),
            fromfile=f"{path} (pass 1)",
            tofile=f"{path} (pass 2)",
            n=3,
        )
    )
    return FileResult(path=path, diff=diff)


def _check_repo(repo: Repo, target_dir: Path) -> CheckResult:
    files = _collect_files(repo, target_dir)
    return CheckResult(
        repo=repo,
        file_results=tuple(_check_file(f) for f in files),
    )


def main(argv: list[str]) -> None:
    """Run canary checks against all or a named subset of repos."""
    repos = list(_REPOS)
    if argv:
        valid = {r.name for r in _REPOS}
        unknown = [name for name in argv if name not in valid]
        if unknown:
            print(
                f"Unknown repo(s): {', '.join(unknown)}. Valid: {', '.join(sorted(valid))}"
            )
            sys.exit(1)
        repos = [r for r in _REPOS if r.name in argv]

    _CANARY_DIR.mkdir(parents=True, exist_ok=True)
    results: list[CheckResult] = []
    for repo in repos:
        target_dir = _CANARY_DIR / repo.name
        _clone_or_pull(repo, target_dir)
        results.append(_check_repo(repo, target_dir))

    print("--- Canary Results ---")
    for result in results:
        label = "PASS" if result.passed else "FAIL"
        failures = [r for r in result.file_results if not r.passed]
        suffix = f" ({len(failures)} file(s))" if failures else ""
        print(f"{label}  {result.repo.display}{suffix}")
        if not result.passed:
            output = result.output
            if output:
                for line in output.splitlines()[:30]:
                    print(f"      {line}")
            else:
                print("      (no output)")

    failures = [r for r in results if not r.passed]
    count = len(failures)
    if count:
        noun = "failure" if count == 1 else "failures"
        names = "  ".join(r.repo.name for r in failures)
        print(f"\n{count} {noun}. Run: tox -e canary -- {names}  to isolate.")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
