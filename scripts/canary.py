"""Run mdformat idempotency checks against real downstream repos (canary testing)."""

# ruff: noqa: T201, S603, S607

from __future__ import annotations

import difflib
import re
import subprocess  # noqa: S404
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mdformat


@dataclass(frozen=True)
class Repo:
    """A downstream repository to check for idempotent mdformat output."""

    name: str
    url: str
    patterns: tuple[str, ...]
    excludes: tuple[str, ...] = ()
    options: dict[str, Any] = field(default_factory=dict)

    @property
    def display(self) -> str:
        """Derive 'org/repo' from URL for display."""
        return "/".join(self.url.rstrip("/").split("/")[-2:])


# Idempotency misses escapes mdformat adds to the original (e.g. autorefs
# [`pkg`][] -> \[`pkg`\][]); the original-vs-pass-1 diff catches them. See #80, #84.
_ESCAPE_RE = re.compile(r"\\([\[\]<>])")


def _new_escapes(original: str, formatted: str) -> int:
    """Count markup escapes formatting introduced that were not in the original."""
    return max(
        0, len(_ESCAPE_RE.findall(formatted)) - len(_ESCAPE_RE.findall(original))
    )


@dataclass(frozen=True)
class FileResult:
    """Result of running mdformat idempotency check on a single file."""

    path: Path
    error: str | None = None
    diff: str | None = None
    new_escapes: int = 0

    @property
    def passed(self) -> bool:
        """True if the file produced no errors and no diff.

        ``new_escapes`` is a warning surfaced separately, not a failure.
        """
        return self.error is None and self.diff is None


@dataclass(frozen=True)
class CheckResult:
    """Aggregated idempotency check results for a single repository."""

    repo: Repo
    file_results: tuple[FileResult, ...]

    @property
    def passed(self) -> bool:
        """True if all file results passed."""
        return all(r.passed for r in self.file_results)

    @property
    def escape_warnings(self) -> tuple[tuple[Path, int], ...]:
        """(path, count) for files where formatting introduced markup escapes."""
        return tuple(
            (r.path, r.new_escapes) for r in self.file_results if r.new_escapes
        )

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


# Not "tmp" — tox wipes the env_tmp_dir at the start of every run, which would
# defeat clone caching. "cache" persists until `tox -e canary --recreate`.
_CANARY_DIR = Path(__file__).parent.parent / ".tox" / "canary" / "cache"

# Each entry documents whether the repo uses mdformat-mkdocs and how.
# This context drives exclude decisions — if a repo excludes files from their
# own mdformat run, we mirror that here so canary tracks what they actually format.
#
# Repos that don't use mdformat are included as idempotency smoke tests: we
# verify our plugin doesn't crash or produce unstable output on real MkDocs content,
# even if that content has never been run through mdformat.
#
# To update: run `git -C .tox/canary/cache/<name> show HEAD:.pre-commit-config.yaml`
# and check for mdformat hooks + their args/excludes.
_REPOS = [
    # Fork disabled its mdformat-mkdocs==5.2.0b2 hook (issue #80): dev-docs autorefs
    # like [`pkg`][] were escaped to \[`pkg`\][]. --ignore-missing-references is the fix.
    Repo(
        "deeplabcut",
        "https://github.com/deruyter92/DeepLabCut",
        ("dev-docs/**/*.md",),
        options={"ignore_missing_references": True},
    ),
    # Uses mdformat-mkdocs==5.1.4 with --wrap=120 --number in pre-commit (rev 1.0.0).
    # Excludes extended-json.md from their own hook; mirror that here.
    Repo(
        "mongodb",
        "https://github.com/mongodb/specifications",
        ("source/**/*.md",),
        excludes=("source/extended-json/extended-json.md",),
        options={"number": True, "wrap": 120},
    ),
    # Uses mdformat-mkdocs==5.1.4 with --number --compact-tables
    # --align-semantic-breaks-in-lists in pre-commit (rev 1.0.0), over all *.md.
    # --compact-tables needs mdformat-tables, which the canary env does not
    # install, so it is not replicated here.
    Repo(
        "prek",
        "https://github.com/j178/prek",
        ("**/*.md",),
        options={"number": True, "align_semantic_breaks_in_lists": True},
    ),
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
        options={"number": True},
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
    # Monorepo: docs live under vizro-core/docs/, vizro-ai/docs/, etc.
    Repo("vizro", "https://github.com/mckinsey/vizro", ("*/docs/**/*.md",)),
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
            ["git", "sparse-checkout", "set", "--no-cone", *repo.patterns],
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


def _check_file(path: Path, options: dict[str, Any]) -> FileResult:
    """Verify mdformat produces idempotent output for a single file."""
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as err:
        return FileResult(path=path, error=f"read error: {err}")

    try:
        pass1 = mdformat.text(original, options=options, extensions={"mkdocs"})
        pass2 = mdformat.text(pass1, options=options, extensions={"mkdocs"})
    except Exception as err:
        return FileResult(path=path, error=f"mdformat error: {err}")

    new_escapes = _new_escapes(original, pass1)
    if pass1 == pass2:
        return FileResult(path=path, new_escapes=new_escapes)

    diff = "".join(
        difflib.unified_diff(
            pass1.splitlines(keepends=True),
            pass2.splitlines(keepends=True),
            fromfile=f"{path} (pass 1)",
            tofile=f"{path} (pass 2)",
            n=3,
        )
    )
    return FileResult(path=path, diff=diff, new_escapes=new_escapes)


def _check_repo(repo: Repo, target_dir: Path) -> CheckResult:
    files = _collect_files(repo, target_dir)
    if not files:
        no_match = FileResult(
            path=target_dir,
            error=f"no files matched patterns {repo.patterns}",
        )
        return CheckResult(repo=repo, file_results=(no_match,))
    return CheckResult(
        repo=repo,
        file_results=tuple(_check_file(f, repo.options) for f in files),
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
    with ThreadPoolExecutor(max_workers=len(repos)) as pool:
        list(pool.map(lambda r: _clone_or_pull(r, _CANARY_DIR / r.name), repos))
    results = [_check_repo(repo, _CANARY_DIR / repo.name) for repo in repos]

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
        warnings = result.escape_warnings
        if warnings:
            total = sum(count for _, count in warnings)
            print(
                f"      WARN  formatting introduced {total} markup escape(s) in "
                f"{len(warnings)} file(s) — review for broken autorefs/links:"
            )
            for path, count in warnings[:10]:
                print(f"        {count:>4}  {path}")

    failures = [r for r in results if not r.passed]
    count = len(failures)
    if count:
        noun = "failure" if count == 1 else "failures"
        names = "  ".join(r.repo.name for r in failures)
        print(f"\n{count} {noun}. Run: tox -e canary -- {names}  to isolate.")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
