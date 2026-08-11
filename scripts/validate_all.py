"""Run the full content-validation pipeline in one command: ruff, the fast pytest
suite, notebook execution, then all five content checkers.

Every stage always runs to completion — a failing stage does not stop the ones after
it — so a single invocation reports everything wrong at once instead of one failure
at a time. `.claude/CLAUDE.md` names this the pre-"done" gate for a module.

Run standalone (`python scripts/validate_all.py [--fast] [--module SLUG]`).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_assessment  # noqa: E402
import check_glossary  # noqa: E402
import check_modelspec  # noqa: E402
import check_notebooks  # noqa: E402
import check_parity  # noqa: E402

from _findings import report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class StageResult:
    name: str
    passed: bool
    detail: str = ""


def run_subprocess_stage(name: str, cmd: list[str]) -> StageResult:
    print(f"\n=== {name} ===")
    result = subprocess.run(cmd, cwd=ROOT)
    return StageResult(name, result.returncode == 0)


def run_check_stage(name: str, findings) -> StageResult:
    print(f"\n=== {name} ===")
    code = report(findings, as_json=False)
    return StageResult(name, code == 0)


def find_existing_notebooks(root: Path) -> list[Path]:
    notebooks: list[Path] = []
    for lang in ("en", "he"):
        nb_dir = root / "notebooks" / lang
        if nb_dir.exists():
            notebooks.extend(sorted(nb_dir.rglob("*.ipynb")))
    return notebooks


def run_nbmake_stage(fast: bool, module: str | None) -> StageResult:
    print("\n=== nbmake ===")
    if fast:
        print("skipped (--fast)")
        return StageResult("nbmake", True, "skipped (--fast)")

    notebooks = find_existing_notebooks(ROOT)
    if module:
        notebooks = [n for n in notebooks if n.stem == module]
    if not notebooks:
        print("no notebooks found — skipped")
        return StageResult("nbmake", True, "no notebooks found")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--nbmake", *(str(n) for n in notebooks)], cwd=ROOT
    )
    return StageResult("nbmake", result.returncode == 0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fast", action="store_true", help="skip the nbmake notebook-execution stage"
    )
    parser.add_argument(
        "--module", help="scope the notebook and content-lint stages to one module slug"
    )
    args = parser.parse_args(argv)

    stages: list[StageResult] = []

    stages.append(run_subprocess_stage("ruff check", [sys.executable, "-m", "ruff", "check", "."]))
    stages.append(
        run_subprocess_stage(
            "pytest (not slow)", [sys.executable, "-m", "pytest", "tests", "-m", "not slow"]
        )
    )
    stages.append(run_nbmake_stage(args.fast, args.module))

    stages.append(run_check_stage("check_modelspec", check_modelspec.check(module=args.module)))
    stages.append(run_check_stage("check_notebooks", check_notebooks.check()))
    stages.append(run_check_stage("check_glossary", check_glossary.check()))
    stages.append(run_check_stage("check_assessment", check_assessment.check(module=args.module)))
    stages.append(run_check_stage("check_parity", check_parity.check()))

    print("\n=== summary ===")
    width = max(len(stage.name) for stage in stages)
    for stage in stages:
        status = "PASS" if stage.passed else "FAIL"
        suffix = f"  ({stage.detail})" if stage.detail else ""
        print(f"{stage.name.ljust(width)}  {status}{suffix}")

    return 0 if all(stage.passed for stage in stages) else 1


if __name__ == "__main__":
    raise SystemExit(main())
