"""Run mdformat --check against real downstream repos (canary testing)."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Repo:
    name: str
    url: str
    patterns: tuple[str, ...]

    @property
    def display(self) -> str:
        """Derive 'org/repo' from URL for display."""
        return "/".join(self.url.rstrip("/").split("/")[-2:])


@dataclass(frozen=True)
class CheckResult:
    repo: Repo
    passed: bool
    output: str


_CANARY_DIR = Path(__file__).parent.parent / ".tox" / "canary" / "tmp"

_REPOS = [
    Repo("ruff",        "https://github.com/astral-sh/ruff",          ("docs/**/*.md",)),
    Repo("supervision", "https://github.com/roboflow/supervision",     ("docs/**/*.md",)),
    Repo("ty",          "https://github.com/astral-sh/ty",            ("docs/**/*.md",)),
    Repo("ultralytics", "https://github.com/ultralytics/ultralytics", ("docs/**/*.md",)),
    Repo("uv",          "https://github.com/astral-sh/uv",            ("docs/**/*.md",)),
    Repo("vizro",       "https://github.com/mckinsey/vizro",          ("docs/**/*.md",)),
]


def _clone_or_pull(repo: Repo, target_dir: Path) -> None:
    if not target_dir.exists():
        subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
             repo.url, str(target_dir)],
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


def _check_repo(repo: Repo, target_dir: Path) -> CheckResult:
    result = subprocess.run(
        [sys.executable, "-m", "mdformat", "--check", "--extension", "mkdocs",
         str(target_dir)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return CheckResult(
        repo=repo,
        passed=(result.returncode == 0),
        output=result.stdout.decode(),
    )


def main(argv: list[str]) -> None:
    repos = list(_REPOS)
    if argv:
        valid = {r.name for r in _REPOS}
        unknown = [name for name in argv if name not in valid]
        if unknown:
            print(f"Unknown repo(s): {', '.join(unknown)}. Valid: {', '.join(sorted(valid))}")
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
        print(f"{label}  {result.repo.display}")
        if not result.passed:
            lines = result.output.splitlines()[:20]
            if lines:
                for line in lines:
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
