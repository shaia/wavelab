"""Content-structure lint over `content/en/**/*.md` and `content/he/**/*.md`.

Enforces the module authoring contract from `.claude/CLAUDE.md`: every module page
carries its section labels in the mandated order, non-empty `objectives:` metadata,
a well-formed seven-bullet model-spec block, at least one epistemic admonition, and
the project's `dU = δQ + δW_on` sign convention everywhere except the one place that
is allowed to convert it.

Run standalone (`python scripts/check_modelspec.py`) or import `check()`.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _content import ContentPage, iter_content_pages  # noqa: E402
from _findings import Finding, report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SUFFIXES = (
    "puzzle",
    "predict",
    "explore",
    "derive",
    "verify",
    "transfer",
    "quiz",
    "explain",
)
OPTIONAL_LAST_SUFFIX = "advanced"

EPISTEMIC_CLASSES = frozenset(
    {
        "definition",
        "empirical-law",
        "theorem",
        "model-assumption",
        "approximation",
        "numerical-observation",
        "open-question",
    }
)

MODEL_SPEC_BULLET_COUNT = 7

# Each pattern flags a work-done-BY sign convention or a "dU = dQ - ..." spelling; the
# project convention is dU = delta Q + delta W_on everywhere except one marked block.
SIGN_CONVENTION_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"W_\{by\}"),
        "uses W_{by} (work-done-BY convention) — project convention is delta W_on",
    ),
    (
        re.compile(r"(?<![A-Za-z0-9_])W_by(?![A-Za-z0-9_])"),
        "uses W_by (work-done-BY convention) — project convention is delta W_on",
    ),
    (
        re.compile(r"\\delta\s*W_\\text\{by\}"),
        r"uses \delta W_\text{by} (work-done-BY convention) — project convention is delta W_on",
    ),
    (
        re.compile(r"dU\s*=\s*\\delta\s*Q\s*-\s*"),
        "uses dU = delta Q - ... — project convention is dU = delta Q + delta W_on",
    ),
)

ALLOWLIST_GLOBS = ("content/*/conventions.md",)
EXCEPTION_MARKER = "<!-- sign-convention-exception -->"


def is_sign_convention_exempt(rel_path: str, text: str) -> bool:
    if any(fnmatch.fnmatch(rel_path, pattern) for pattern in ALLOWLIST_GLOBS):
        return True
    return EXCEPTION_MARKER in text


def check_labels(page: ContentPage, slug: str) -> list[Finding]:
    findings: list[Finding] = []
    label_lines = dict(page.labels)
    required = [f"{slug}-{suffix}" for suffix in REQUIRED_SUFFIXES]

    for label in required:
        if label not in label_lines:
            findings.append(Finding(page.path, None, "error", f"missing required label ({label})="))

    present_required = [label for label in required if label in label_lines]
    in_document_order = sorted(present_required, key=lambda label: label_lines[label])
    if in_document_order != present_required:
        findings.append(
            Finding(
                page.path,
                None,
                "error",
                f"required labels out of order: found {in_document_order}, "
                f"expected {present_required}",
            )
        )

    advanced_label = f"{slug}-{OPTIONAL_LAST_SUFFIX}"
    if advanced_label in label_lines:
        module_labels = [*present_required, advanced_label]
        last_by_line = max(module_labels, key=lambda label: label_lines[label])
        if last_by_line != advanced_label:
            findings.append(
                Finding(
                    page.path,
                    label_lines[advanced_label],
                    "error",
                    f"({advanced_label})= must be the last section label",
                )
            )
    return findings


def check_objectives(page: ContentPage) -> list[Finding]:
    objectives = page.frontmatter.get("objectives")
    if not isinstance(objectives, list) or len(objectives) == 0:
        return [
            Finding(page.path, None, "error", "front matter objectives: must be a non-empty list")
        ]
    findings: list[Finding] = []
    for i, objective in enumerate(objectives):
        if not isinstance(objective, dict) or "id" not in objective or "text" not in objective:
            findings.append(
                Finding(
                    page.path, None, "error", f"objectives[{i}] must be a mapping with id and text"
                )
            )
    return findings


def check_model_spec_blocks(page: ContentPage) -> list[Finding]:
    findings: list[Finding] = []
    for admonition in page.admonitions:
        if "model-spec" not in admonition.classes and admonition.directive != "model-spec":
            continue
        n = len(admonition.bullets)
        if n != MODEL_SPEC_BULLET_COUNT:
            findings.append(
                Finding(
                    page.path,
                    admonition.line,
                    "error",
                    f"model-spec block has {n} top-level bullets, expected exactly "
                    f"{MODEL_SPEC_BULLET_COUNT}",
                )
            )
    return findings


def check_sign_convention(page: ContentPage) -> list[Finding]:
    if is_sign_convention_exempt(page.rel_path, page.text):
        return []
    findings: list[Finding] = []
    for lineno, line in enumerate(page.text.splitlines(), start=1):
        for pattern, message in SIGN_CONVENTION_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(page.path, lineno, "error", message))
    return findings


def check_epistemic_labeling(page: ContentPage) -> list[Finding]:
    if "module" not in page.frontmatter:
        return []
    classes: set[str] = set()
    for admonition in page.admonitions:
        classes |= admonition.classes
        classes.add(admonition.directive)
    if not classes & EPISTEMIC_CLASSES:
        return [
            Finding(
                page.path,
                None,
                "warning",
                "page has module: but no epistemic admonition "
                "(definition/empirical-law/theorem/model-assumption/approximation/"
                "numerical-observation/open-question) found",
            )
        ]
    return []


def check(root: Path = ROOT, module: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for page in iter_content_pages(root):
        if module and page.frontmatter.get("module") != module:
            continue
        findings.extend(check_model_spec_blocks(page))
        findings.extend(check_sign_convention(page))
        slug = page.frontmatter.get("module")
        if isinstance(slug, str) and slug:
            findings.extend(check_labels(page, slug))
            findings.extend(check_objectives(page))
            findings.extend(check_epistemic_labeling(page))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="scope the lint to one module slug")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    findings = check(module=args.module)
    return report(findings, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
