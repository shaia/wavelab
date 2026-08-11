"""Glossary consistency lint over `content/he/**/*.md` and Hebrew quiz banks.

`glossary/terms.yml` is the single source of Hebrew terminology (`.claude/CLAUDE.md`:
"Hebrew terms come ONLY from glossary/terms.yml — never improvise a translation").
This script is what makes that rule enforceable: it flags known-wrong spellings
(`he_reject`) and warns when an English glossary term shows up untranslated in
Hebrew prose. It also validates the glossary file itself.

Run standalone (`python scripts/check_glossary.py`) or import `check()`.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _content import content_root, iter_markdown, mask_non_prose  # noqa: E402
from _findings import Finding, report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY_PATH = ROOT / "glossary" / "terms.yml"
QUIZ_DIR = ROOT / "assessment" / "quizzes"


@dataclass(frozen=True)
class GlossaryTerm:
    key: str
    en: str
    he: str
    he_reject: tuple[str, ...]


def load_glossary(path: Path = GLOSSARY_PATH) -> tuple[list[GlossaryTerm], list[Finding]]:
    if not path.exists():
        return [], []
    findings: list[Finding] = []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entries = raw.get("terms") or []
    seen: set[str] = set()
    terms: list[GlossaryTerm] = []
    for entry in entries:
        key = entry.get("key")
        if key in seen:
            findings.append(Finding(path, None, "error", f"duplicate glossary key: {key}"))
        seen.add(key)
        he = entry.get("he")
        if not he:
            findings.append(
                Finding(
                    path, None, "error", f"glossary term '{key}' is missing a Hebrew (he) value"
                )
            )
        terms.append(
            GlossaryTerm(
                key=key,
                en=entry.get("en", ""),
                he=he or "",
                he_reject=tuple(entry.get("he_reject") or []),
            )
        )
    return terms, findings


def _line_numbers(text: str, pattern: re.Pattern[str]) -> list[int]:
    return [i for i, line in enumerate(text.splitlines(), start=1) if pattern.search(line)]


def check_text(path: Path, text: str, terms: list[GlossaryTerm]) -> list[Finding]:
    """Scan one file's text for rejected spellings and untranslated English terms.

    Both checks run against prose-only text (math, code, MyST labels and directive
    names masked out) so a term embedded in an equation or a code sample never counts.
    """
    findings: list[Finding] = []
    scan_text = mask_non_prose(text)

    for term in terms:
        for bad_spelling in term.he_reject:
            pattern = re.compile(rf"\b{re.escape(bad_spelling)}\b")
            for lineno in _line_numbers(scan_text, pattern):
                findings.append(
                    Finding(
                        path,
                        lineno,
                        "error",
                        f"rejected spelling '{bad_spelling}' for glossary term '{term.key}' "
                        f"— use '{term.he}'",
                    )
                )

    for term in terms:
        if not term.en:
            continue
        # ASCII-letter boundaries rather than \b: Python's \b treats Hebrew letters as
        # word characters too, so an English term glued directly to Hebrew text would
        # not register a boundary against \b.
        pattern = re.compile(rf"(?<![A-Za-z]){re.escape(term.en)}(?![A-Za-z])", re.IGNORECASE)
        for lineno in _line_numbers(scan_text, pattern):
            findings.append(
                Finding(
                    path,
                    lineno,
                    "warning",
                    f"English term '{term.en}' appears verbatim — use glossary Hebrew term "
                    f"'{term.he}' for '{term.key}'",
                )
            )
    return findings


def check(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    terms, glossary_findings = load_glossary(root / "glossary" / "terms.yml")
    findings.extend(glossary_findings)
    if not terms:
        return findings

    for path in iter_markdown(content_root(root, "he")):
        findings.extend(check_text(path, path.read_text(encoding="utf-8"), terms))

    quiz_dir = root / "assessment" / "quizzes"
    if quiz_dir.exists():
        for path in sorted(quiz_dir.glob("*.he.yml")):
            findings.extend(check_text(path, path.read_text(encoding="utf-8"), terms))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    findings = check()
    return report(findings, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
