"""Quiz/exam QA: quiz-bank schema, objective coverage, misconception coverage, and
answer-key safety.

Exam-style problem sets are course content students read on the site, so they live
in the content tree (`content/<lang>/**/*-problems.md`), not under `assessment/`
— only quiz banks and the misconception registry do. Objective coverage is computed
per language from that language's own module pages, quiz bank and exam files, so a
missing Hebrew exam shows up as a Hebrew coverage gap rather than passing silently
on English's coverage.

Run standalone (`python scripts/check_assessment.py`) or import `check()`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _content import LANGS, iter_content_pages  # noqa: E402
from _findings import Finding, report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

QUESTION_TYPES = frozenset({"multiple-choice", "numeric", "prediction", "short-answer"})
EXAM_GLOB = "*-problems.md"
OBJECTIVE_COMMENT_RE = re.compile(r"<!--\s*objectives:\s*(.+?)\s*-->")
FORBIDDEN_SUBSTRINGS = ("answer_key", "instructor/")
PROBLEM_HEADING_RE = re.compile(r"^##\s+Problem\s+(\d+)\b", re.MULTILINE)


# ---------------------------------------------------------------------------
# Quiz bank schema
# ---------------------------------------------------------------------------


def check_multiple_choice(path: Path, qid: str, choices: object) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(choices, list) or not choices:
        return [Finding(path, None, "error", f"multiple-choice question '{qid}' needs choices")]
    correct_count = 0
    for i, choice in enumerate(choices):
        if not isinstance(choice, dict) or "text" not in choice or "correct" not in choice:
            findings.append(
                Finding(path, None, "error", f"question '{qid}' choice {i} missing text/correct")
            )
            continue
        if choice.get("correct"):
            correct_count += 1
        if not choice.get("feedback"):
            findings.append(
                Finding(path, None, "error", f"question '{qid}' choice {i} missing feedback")
            )
    if correct_count != 1:
        findings.append(
            Finding(
                path,
                None,
                "error",
                f"multiple-choice question '{qid}' has {correct_count} correct choices, "
                f"expected exactly 1",
            )
        )
    return findings


def check_ascii_math(path: Path, qid: str, question: dict) -> list[Finding]:
    """Quiz text is plain ASCII math — `N^(-1/2)`, not `$N^{-1/2}$`.

    Not a style rule. `render_quizzes.py` writes these strings into real page pairs under
    `content/*/_generated/`, so a `$…$` here becomes an entry in `check_parity`'s equation
    multiset that the other language must then reproduce character for character — and
    `check_sign_convention` scans those generated pages too. Keeping the banks ASCII keeps a
    whole class of parity failures from existing.
    """
    fields: list[tuple[str, object]] = [
        ("prompt", question.get("prompt")),
        ("feedback", question.get("feedback")),
        ("discussion", question.get("discussion")),
    ]
    choices = question.get("choices")
    if isinstance(choices, list):
        for i, choice in enumerate(choices):
            if isinstance(choice, dict):
                fields.append((f"choices[{i}].text", choice.get("text")))
                fields.append((f"choices[{i}].feedback", choice.get("feedback")))

    return [
        Finding(
            path,
            None,
            "error",
            f"question '{qid}' {name} contains '$' — quiz banks use plain ASCII math "
            f"(N^(-1/2), not $N^{{-1/2}}$), because the rendered pages are parity-checked",
        )
        for name, value in fields
        if isinstance(value, str) and "$" in value
    ]


def check_quiz_schema(path: Path, bank: dict, misconception_ids: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    if not bank.get("module"):
        findings.append(Finding(path, None, "error", "quiz bank missing module:"))

    questions = bank.get("questions")
    if not isinstance(questions, list) or not questions:
        findings.append(Finding(path, None, "error", "quiz bank has no questions"))
        return findings

    seen_ids: set[str] = set()
    for question in questions:
        qid = question.get("id")
        if not qid:
            findings.append(Finding(path, None, "error", "question missing id"))
            continue
        if qid in seen_ids:
            findings.append(Finding(path, None, "error", f"duplicate question id: {qid}"))
        seen_ids.add(qid)

        qtype = question.get("type")
        if qtype not in QUESTION_TYPES:
            findings.append(
                Finding(path, None, "error", f"question '{qid}' has invalid type {qtype!r}")
            )
        if not question.get("prompt"):
            findings.append(Finding(path, None, "error", f"question '{qid}' missing prompt"))
        objectives = question.get("objectives")
        if not isinstance(objectives, list) or not objectives:
            findings.append(
                Finding(
                    path, None, "error", f"question '{qid}' objectives must be a non-empty list"
                )
            )

        findings.extend(check_ascii_math(path, qid, question))

        misconception = question.get("misconception")
        if misconception and misconception not in misconception_ids:
            findings.append(
                Finding(
                    path,
                    None,
                    "error",
                    f"question '{qid}' references unknown misconception id '{misconception}'",
                )
            )

        if qtype == "multiple-choice":
            findings.extend(check_multiple_choice(path, qid, question.get("choices")))
        elif qtype == "numeric":
            if question.get("answer") is None or question.get("tolerance") is None:
                findings.append(
                    Finding(
                        path, None, "error", f"numeric question '{qid}' needs answer and tolerance"
                    )
                )
        elif qtype in ("prediction", "short-answer"):
            if not question.get("discussion"):
                findings.append(
                    Finding(path, None, "error", f"question '{qid}' ({qtype}) needs discussion")
                )
    return findings


# ---------------------------------------------------------------------------
# Exam problem sets: content/<lang>/**/*-problems.md
# ---------------------------------------------------------------------------


def iter_exam_files(root: Path, lang: str) -> list[Path]:
    lang_root = root / "content" / lang
    if not lang_root.exists():
        return []
    return sorted(p for p in lang_root.rglob(EXAM_GLOB) if "_build" not in p.parts)


def exam_objective_ids(path: Path) -> list[str]:
    ids: list[str] = []
    for match in OBJECTIVE_COMMENT_RE.finditer(path.read_text(encoding="utf-8")):
        ids.extend(part.strip() for part in match.group(1).split(",") if part.strip())
    return ids


# ---------------------------------------------------------------------------
# Objective coverage, per language
# ---------------------------------------------------------------------------


def check_objective_coverage(
    root: Path, lang: str, module: str | None, quiz_banks: dict[Path, dict]
) -> list[Finding]:
    findings: list[Finding] = []

    declared: dict[str, tuple[Path, str]] = {}
    for page in iter_content_pages(root):
        if page.lang != lang:
            continue
        slug = page.frontmatter.get("module")
        if not isinstance(slug, str) or not slug:
            continue
        if module and slug != module:
            continue
        for objective in page.frontmatter.get("objectives") or []:
            if not isinstance(objective, dict):
                continue
            oid = objective.get("id")
            if not oid:
                continue
            if oid in declared:
                findings.append(
                    Finding(
                        page.path,
                        None,
                        "error",
                        f"objective id '{oid}' declared more than once "
                        f"({declared[oid][0]} and {page.path})",
                    )
                )
                continue
            declared[oid] = (page.path, slug)

    referenced: dict[str, list[Path]] = {}
    for quiz_path, bank in quiz_banks.items():
        if not quiz_path.name.endswith(f".{lang}.yml"):
            continue
        if module and bank.get("module") != module:
            continue
        for question in bank.get("questions") or []:
            for oid in question.get("objectives") or []:
                referenced.setdefault(oid, []).append(quiz_path)

    for exam_path in iter_exam_files(root, lang):
        if module and exam_path.stem != f"{module}-problems":
            continue
        for oid in exam_objective_ids(exam_path):
            referenced.setdefault(oid, []).append(exam_path)

    for oid, (page_path, slug) in declared.items():
        if oid not in referenced:
            findings.append(
                Finding(
                    page_path,
                    None,
                    "error",
                    f"objective '{oid}' ({lang}, module {slug}) is not covered by any "
                    f"quiz or exam question",
                )
            )

    for oid, sources in referenced.items():
        if oid not in declared:
            for source in sources:
                findings.append(
                    Finding(
                        source, None, "error", f"references unknown objective id '{oid}' ({lang})"
                    )
                )

    return findings


# ---------------------------------------------------------------------------
# Misconception coverage
# ---------------------------------------------------------------------------


def load_misconceptions(root: Path) -> tuple[list[dict], list[Finding]]:
    path = root / "assessment" / "misconceptions.yml"
    if not path.exists():
        return [], []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get("misconceptions") or [], []


def collect_known_modules(root: Path, quiz_banks: dict[Path, dict]) -> set[str]:
    modules = {
        page.frontmatter.get("module")
        for page in iter_content_pages(root)
        if isinstance(page.frontmatter.get("module"), str) and page.frontmatter.get("module")
    }
    modules |= {bank.get("module") for bank in quiz_banks.values() if bank.get("module")}
    return modules  # type: ignore[return-value]


def check_misconceptions(
    root: Path, quiz_banks: dict[Path, dict], known_modules: set[str], module: str | None = None
) -> list[Finding]:
    """Check the registry against the quiz banks.

    `quiz_banks` must be *every* bank even on a scoped run: coverage is a whole-repo
    invariant, and collecting references from one module's banks alone would report every
    other module's addressed misconception as unreferenced. `module` narrows which entries
    are reported on, not which banks are consulted.
    """
    path = root / "assessment" / "misconceptions.yml"
    entries, findings = load_misconceptions(root)
    if not entries:
        return findings
    if module:
        entries = [entry for entry in entries if entry.get("assigned_module") == module]

    referenced_ids: set[str] = set()
    for bank in quiz_banks.values():
        for question in bank.get("questions") or []:
            misconception = question.get("misconception")
            if misconception:
                referenced_ids.add(misconception)

    seen_ids: set[str] = set()
    for entry in entries:
        mid = entry.get("id")
        if mid in seen_ids:
            findings.append(Finding(path, None, "error", f"duplicate misconception id: {mid}"))
        seen_ids.add(mid)

        status = entry.get("status")
        assigned_module = entry.get("assigned_module")
        if status == "addressed":
            if not assigned_module or assigned_module not in known_modules:
                findings.append(
                    Finding(
                        path,
                        None,
                        "error",
                        f"misconception '{mid}' is addressed but assigned_module "
                        f"'{assigned_module}' does not exist",
                    )
                )
            if mid not in referenced_ids:
                findings.append(
                    Finding(
                        path,
                        None,
                        "error",
                        f"misconception '{mid}' is addressed but no quiz question references it",
                    )
                )
        elif status == "pending":
            if mid in referenced_ids:
                message = (
                    f"misconception '{mid}' is pending but a quiz question already "
                    f"references it — consider flipping status to addressed"
                )
            else:
                message = (
                    f"misconception '{mid}' is pending — module '{assigned_module}' "
                    f"still owes a quiz question referencing it"
                )
            findings.append(Finding(path, None, "warning", message))
    return findings


# ---------------------------------------------------------------------------
# Answer-key safety
# ---------------------------------------------------------------------------


def check_answer_key_safety(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    content_dir = root / "content"
    if not content_dir.exists():
        return findings
    for path in sorted(content_dir.rglob("*")):
        if not path.is_file() or "_build" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            low = line.lower()
            if "answer_key" in low:
                findings.append(
                    Finding(
                        path,
                        lineno,
                        "error",
                        "content file contains 'answer_key' — solutions must never reach "
                        "the built site",
                    )
                )
            if "instructor/" in low:
                findings.append(
                    Finding(
                        path,
                        lineno,
                        "error",
                        "content file references instructor/ — solutions/rubrics must "
                        "never be included in content",
                    )
                )
    return findings


# ---------------------------------------------------------------------------
# Instructor solution coverage
# ---------------------------------------------------------------------------


def check_solution_coverage(root: Path, module: str | None = None) -> list[Finding]:
    """Every problem set must have instructor solutions covering every problem in it.

    Answer-key safety (above) guarantees solutions never reach the site; this is the other
    half — that they exist at all. Without it a problem set can promise "solutions live with
    the instructor material" while `instructor/` is empty, which is exactly what happened
    after Milestone 1: nothing failed, because nothing was looking.

    `instructor/` is gitignored — the repository is public, and publishing worked solutions
    would hand students the answers — so a clone legitimately has no instructor tree at all.
    When the directory is absent entirely this check stays silent, because "you are not an
    instructor" is not a defect. It bites for anyone who has the tree, which is exactly the
    person who can act on it. The cost of that trade-off is real and worth naming: an author
    who deletes `instructor/` wholesale silences the check rather than failing it.

    Only English problem sets are checked. Solutions are deliberately not translated — the
    bilingual contract covers what students read, and the physics is the same in both.
    """
    findings: list[Finding] = []
    exams_root = root / "content" / "en"
    if not exams_root.exists() or not (root / "instructor").exists():
        return findings

    for exam_path in sorted(exams_root.rglob(EXAM_GLOB)):
        if "_build" in exam_path.parts:
            continue
        slug = exam_path.name[: -len("-problems.md")]
        if module and slug != module:
            continue

        solution_path = root / "instructor" / "solutions" / f"{slug}.md"
        if not solution_path.exists():
            findings.append(
                Finding(
                    exam_path,
                    None,
                    "error",
                    f"problem set has no instructor solutions — expected "
                    f"instructor/solutions/{slug}.md",
                )
            )
            continue

        posed = set(PROBLEM_HEADING_RE.findall(exam_path.read_text(encoding="utf-8")))
        solved = set(PROBLEM_HEADING_RE.findall(solution_path.read_text(encoding="utf-8")))
        missing = sorted(posed - solved, key=int)
        if missing:
            findings.append(
                Finding(
                    solution_path,
                    None,
                    "error",
                    f"solutions omit problem(s) {', '.join(missing)} posed in "
                    f"{exam_path.name}",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def check(root: Path = ROOT, module: str | None = None) -> list[Finding]:
    findings: list[Finding] = []

    quizzes_dir = root / "assessment" / "quizzes"
    quiz_paths = sorted(quizzes_dir.glob("*.yml")) if quizzes_dir.exists() else []

    misconception_entries, _ = load_misconceptions(root)
    misconception_ids = {entry.get("id") for entry in misconception_entries if entry.get("id")}

    all_quiz_banks: dict[Path, dict] = {
        path: yaml.safe_load(path.read_text(encoding="utf-8")) or {} for path in quiz_paths
    }
    quiz_banks = {
        path: bank
        for path, bank in all_quiz_banks.items()
        if not module or path.name.startswith(f"{module}.")
    }
    for path, bank in quiz_banks.items():
        findings.extend(check_quiz_schema(path, bank, misconception_ids))

    findings.extend(check_answer_key_safety(root))
    findings.extend(check_solution_coverage(root, module))

    # Every bank, not the scoped subset — see check_misconceptions.
    known_modules = collect_known_modules(root, all_quiz_banks)
    findings.extend(check_misconceptions(root, all_quiz_banks, known_modules, module))

    for lang in LANGS:
        findings.extend(check_objective_coverage(root, lang, module, quiz_banks))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="scope quiz/objective checks to one module slug")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    findings = check(module=args.module)
    return report(findings, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
