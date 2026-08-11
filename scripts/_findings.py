"""Shared finding/reporting types for the content-validation scripts.

Every validator in `scripts/check_*.py` needs the same three things — a uniform way
to record a problem, a human-readable printout, and a machine-readable one — so this
module implements those once instead of five times. It intentionally knows nothing
about content, glossaries, or quizzes; it only formats what the checkers found.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class Finding:
    """One thing a validator noticed.

    `line` is None when the problem belongs to the file as a whole (e.g. a missing
    front-matter key) rather than to a specific line.
    """

    path: Path
    line: int | None
    severity: Severity
    message: str

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path.as_posix() if isinstance(self.path, Path) else str(self.path),
            "line": self.line,
            "severity": self.severity,
            "message": self.message,
        }

    def __str__(self) -> str:
        location = str(self.path) if self.line is None else f"{self.path}:{self.line}"
        return f"{self.severity.upper():7} {location}: {self.message}"


def ensure_stdout_can_print_unicode() -> None:
    """Some Windows terminals leave stdout on a legacy code page (cp1252) that cannot
    represent Hebrew text, which would otherwise crash `print()` mid-report. Since
    this project's content is bilingual EN/HE by design, replace unencodable
    characters instead of raising — best effort, and a no-op on streams that don't
    support reconfiguring (e.g. already redirected to something unusual).
    """
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


def report(findings: Sequence[Finding], as_json: bool) -> int:
    """Print `findings` and return the process exit code.

    Only "error" severity fails the build (return 1); warnings are surfaced but never
    fail it, mirroring how ruff/pytest already behave in this project's toolchain.
    """
    ensure_stdout_can_print_unicode()
    if as_json:
        print(json.dumps([f.to_json() for f in findings], indent=2, ensure_ascii=False))
    else:
        if not findings:
            print("OK - no findings")
        for finding in sorted(findings, key=lambda f: (str(f.path), f.line or 0)):
            print(finding)
        n_errors = sum(1 for f in findings if f.severity == "error")
        n_warnings = sum(1 for f in findings if f.severity == "warning")
        if findings:
            print(f"\n{n_errors} error(s), {n_warnings} warning(s)")
    return 1 if any(f.severity == "error" for f in findings) else 0
