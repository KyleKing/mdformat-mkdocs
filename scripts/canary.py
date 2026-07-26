"""Run mdformat idempotency checks against real downstream repos (canary testing).

Repos to check are configured in 'scripts/canary_repos.json', which is not
overwritten by 'copier update' once it exists (see '_skip_if_exists' in
'copier.yml'). It starts empty: canary testing is entirely opt-in per
project. JSON (not a Python module of 'Repo(...)' calls) so this script can
change the 'Repo' shape across template syncs without breaking every
downstream project's frozen, un-synced entries; unknown or missing fields
are ignored or defaulted rather than raising.

To add or update an entry, run
`git -C .tox/canary/cache/<name> show HEAD:.pre-commit-config.yaml` and check
for a mdformat hook plus its args/excludes, then mirror them in the JSON
entry so canary tracks what the downstream repo actually formats. Only
'name' and 'url' are required.

Example entry, appended to the 'repos' array in 'canary_repos.json'::

    {
        "name": "some-project",
        "url": "https://github.com/some-org/some-project",
        "patterns": ["docs/**/*.md"],
        "excludes": ["docs/changelog.md"],
        "options": {"wrap": 120}
    }
"""

# ruff:file-ignore[print, subprocess-without-shell-equals-true, start-process-with-partial-path]

from __future__ import annotations

import difflib
import json
import re
import subprocess  # ruff:ignore[suspicious-subprocess-import]
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mdformat

# Idempotency misses escapes mdformat adds to the original (e.g. autorefs
# [`pkg`][] -> \[`pkg`\][]); the original-vs-pass-1 diff catches them.
_ESCAPE_RE = re.compile(r"\\([\[\]<>])")


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

        'new_escapes' is a warning surfaced separately, not a failure.
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

_REPOS_PATH = Path(__file__).parent / "canary_repos.json"

_EXTENSIONS = {"mkdocs"}


def _load_repos(path: Path) -> list[Repo]:
    """Parse 'canary_repos.json', defaulting/ignoring fields this version doesn't know."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        Repo(
            name=entry["name"],
            url=entry["url"],
            patterns=tuple(entry.get("patterns", ())),
            excludes=tuple(entry.get("excludes", ())),
            options=entry.get("options", {}),
        )
        for entry in data.get("repos", [])
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
        pass1 = mdformat.text(original, options=options, extensions=_EXTENSIONS)
        pass2 = mdformat.text(pass1, options=options, extensions=_EXTENSIONS)
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


def _resolve_repos(argv: list[str], all_repos: list[Repo]) -> list[Repo]:
    if not argv:
        return list(all_repos)
    valid = {r.name for r in all_repos}
    unknown = [name for name in argv if name not in valid]
    if unknown:
        print(
            f"Unknown repo(s): {', '.join(unknown)}. Valid: {', '.join(sorted(valid))}"
        )
        sys.exit(1)
    return [r for r in all_repos if r.name in argv]


def _print_results(results: list[CheckResult]) -> None:
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


def main(argv: list[str]) -> None:
    """Run canary checks against all or a named subset of repos."""
    all_repos = _load_repos(_REPOS_PATH)

    if not all_repos:
        print(
            "No canary repos configured in scripts/canary_repos.json. Skipping "
            "(canary testing is opt-in; see this module's docstring)."
        )
        return

    repos = _resolve_repos(argv, all_repos)

    _CANARY_DIR.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=len(repos)) as pool:
        list(pool.map(lambda r: _clone_or_pull(r, _CANARY_DIR / r.name), repos))
    results = [_check_repo(repo, _CANARY_DIR / repo.name) for repo in repos]

    _print_results(results)

    failures = [r for r in results if not r.passed]
    count = len(failures)
    if count:
        noun = "failure" if count == 1 else "failures"
        names = "  ".join(r.repo.name for r in failures)
        print(f"\n{count} {noun}. Run: tox -e canary -- {names}  to isolate.")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
