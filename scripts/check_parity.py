"""EN/HE parity checks: tree completeness, hash staleness, equation identity,
notebook code-cell identity, quiz-bank identity, figure targets, and media-tree agreement.

English is the source of truth (`.claude/CLAUDE.md`); every HE artifact either
mirrors its EN source exactly (equations, notebook code) or carries a hash proving
it was translated against the current EN text. `translation-pending.txt` lists the
repo-relative EN paths intentionally not yet translated.

Run standalone (`python scripts/check_parity.py`) or import `check()`. `--json`
groups findings the way the translate-sync skill wants them: missing / stale /
mismatch (see `CATEGORY_PREFIXES`) — every message from this script starts with one
of those words followed by a colon.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import nbformat
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _content import (  # noqa: E402
    LANGS,
    content_root,
    extract_equations,
    iter_content_pages,
    iter_markdown,
    normalize_equation,
    parse_frontmatter,
    sha256_normalized,
)
from _findings import Finding, ensure_stdout_can_print_unicode, report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_PREFIXES = ("missing", "stale", "mismatch")


# ---------------------------------------------------------------------------
# translation-pending.txt
# ---------------------------------------------------------------------------


def load_pending(root: Path) -> set[str]:
    path = root / "translation-pending.txt"
    if not path.exists():
        return set()
    pending: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            pending.add(line.replace("\\", "/"))
    return pending


def en_to_he(en_relpath: str) -> str:
    """Swap the first "en" path segment for "he" (works for content/ and notebooks/)."""
    parts = en_relpath.split("/")
    for i, part in enumerate(parts):
        if part == "en":
            parts[i] = "he"
            return "/".join(parts)
    raise ValueError(f"path has no 'en' segment to swap: {en_relpath}")


# ---------------------------------------------------------------------------
# Hash staleness (shared by pages and notebooks)
# ---------------------------------------------------------------------------


def check_hash(he_path: Path, stored: object, en_path: Path, pending: bool) -> list[Finding]:
    if not stored:
        return [Finding(he_path, None, "error", "stale: missing en_source_hash")]
    if not isinstance(stored, str):
        return [
            Finding(he_path, None, "error", f"stale: en_source_hash is not a string: {stored!r}")
        ]
    if stored == "PENDING":
        if pending:
            return [
                Finding(
                    he_path,
                    None,
                    "warning",
                    "stale: en_source_hash is PENDING (listed in translation-pending.txt)",
                )
            ]
        return [
            Finding(
                he_path,
                None,
                "error",
                "stale: en_source_hash is PENDING but file is not listed in "
                "translation-pending.txt",
            )
        ]
    expected = sha256_normalized(en_path.read_bytes())
    if stored != expected:
        return [
            Finding(
                he_path,
                None,
                "error",
                f"stale: en_source_hash mismatch "
                f"(stored {stored[:12]}.., expected {expected[:12]}..)",
            )
        ]
    return []


# ---------------------------------------------------------------------------
# Page tree parity + staleness + equation identity
# ---------------------------------------------------------------------------


def check_page_tree(root: Path, pending: set[str]) -> tuple[list[Finding], set[str]]:
    en_dir = content_root(root, "en")
    he_dir = content_root(root, "he")
    en_tails = {p.relative_to(en_dir).as_posix() for p in iter_markdown(en_dir)}
    he_tails = {p.relative_to(he_dir).as_posix() for p in iter_markdown(he_dir)}

    pending_tails = {p[len("content/en/") :] for p in pending if p.startswith("content/en/")}

    findings: list[Finding] = []
    required = en_tails - pending_tails
    for tail in sorted(required - he_tails):
        findings.append(
            Finding(
                en_dir / tail,
                None,
                "error",
                f"missing: HE translation missing for content/en/{tail}",
            )
        )
    for tail in sorted(he_tails - en_tails):
        findings.append(
            Finding(
                he_dir / tail,
                None,
                "error",
                f"mismatch: HE file has no EN source (content/he/{tail})",
            )
        )

    return findings, en_tails & he_tails


def check_page_pair(root: Path, tail: str, pending_tail: bool) -> list[Finding]:
    en_path = content_root(root, "en") / tail
    he_path = content_root(root, "he") / tail
    findings: list[Finding] = []

    he_frontmatter = parse_frontmatter(he_path.read_text(encoding="utf-8"))
    findings.extend(
        check_hash(he_path, he_frontmatter.get("en_source_hash"), en_path, pending=pending_tail)
    )

    en_equations = Counter(
        normalize_equation(e) for e in extract_equations(en_path.read_text(encoding="utf-8"))
    )
    he_equations = Counter(
        normalize_equation(e) for e in extract_equations(he_path.read_text(encoding="utf-8"))
    )
    for eq in sorted(set(en_equations) | set(he_equations)):
        en_n, he_n = en_equations.get(eq, 0), he_equations.get(eq, 0)
        if en_n != he_n:
            findings.append(
                Finding(
                    he_path,
                    None,
                    "error",
                    f"mismatch: equation count differs for '{eq}': EN={en_n} HE={he_n}",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Notebook tree parity + code-cell identity + metadata hash
# ---------------------------------------------------------------------------


def _cell_source(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def check_notebook_tree(root: Path, pending: set[str]) -> tuple[list[Finding], set[str]]:
    en_dir = root / "notebooks" / "en"
    he_dir = root / "notebooks" / "he"
    en_tails = (
        {p.relative_to(en_dir).as_posix() for p in en_dir.rglob("*.ipynb")}
        if en_dir.exists()
        else set()
    )
    he_tails = (
        {p.relative_to(he_dir).as_posix() for p in he_dir.rglob("*.ipynb")}
        if he_dir.exists()
        else set()
    )

    pending_tails = {p[len("notebooks/en/") :] for p in pending if p.startswith("notebooks/en/")}

    findings: list[Finding] = []
    required = en_tails - pending_tails
    for tail in sorted(required - he_tails):
        findings.append(
            Finding(
                en_dir / tail,
                None,
                "error",
                f"missing: HE notebook missing for notebooks/en/{tail}",
            )
        )
    for tail in sorted(he_tails - en_tails):
        findings.append(
            Finding(
                he_dir / tail,
                None,
                "error",
                f"mismatch: HE notebook has no EN source (notebooks/he/{tail})",
            )
        )
    return findings, en_tails & he_tails


def check_notebook_pair(root: Path, tail: str, pending_tail: bool) -> list[Finding]:
    en_path = root / "notebooks" / "en" / tail
    he_path = root / "notebooks" / "he" / tail
    findings: list[Finding] = []

    en_nb = nbformat.read(en_path, as_version=4)
    he_nb = nbformat.read(he_path, as_version=4)
    en_code = [_cell_source(c) for c in en_nb.cells if c.get("cell_type") == "code"]
    he_code = [_cell_source(c) for c in he_nb.cells if c.get("cell_type") == "code"]
    if len(en_code) != len(he_code):
        findings.append(
            Finding(
                he_path,
                None,
                "error",
                f"mismatch: code-cell count differs: EN={len(en_code)} HE={len(he_code)}",
            )
        )
    else:
        for i, (en_src, he_src) in enumerate(zip(en_code, he_code, strict=True)):
            if en_src != he_src:
                findings.append(
                    Finding(
                        he_path, None, "error", f"mismatch: code cell {i} differs between EN and HE"
                    )
                )

    stored = ((he_nb.get("metadata") or {}).get("thermolab") or {}).get("en_source_hash")
    findings.extend(check_hash(he_path, stored, en_path, pending=pending_tail))
    return findings


# ---------------------------------------------------------------------------
# Quiz bank parity
# ---------------------------------------------------------------------------


def check_quiz_pair(en_path: Path, he_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    en_data = yaml.safe_load(en_path.read_text(encoding="utf-8")) or {}
    he_data = yaml.safe_load(he_path.read_text(encoding="utf-8")) or {}
    en_qs = {q.get("id"): q for q in en_data.get("questions") or []}
    he_qs = {q.get("id"): q for q in he_data.get("questions") or []}

    for qid in sorted(en_qs.keys() - he_qs.keys()):
        findings.append(
            Finding(
                he_path,
                None,
                "error",
                f"mismatch: question '{qid}' present in EN bank but missing in HE",
            )
        )
    for qid in sorted(he_qs.keys() - en_qs.keys()):
        findings.append(
            Finding(
                he_path,
                None,
                "error",
                f"mismatch: question '{qid}' present in HE bank but missing in EN",
            )
        )

    for qid in sorted(en_qs.keys() & he_qs.keys()):
        en_q, he_q = en_qs[qid], he_qs[qid]
        if en_q.get("type") != he_q.get("type"):
            findings.append(
                Finding(
                    he_path,
                    None,
                    "error",
                    f"mismatch: question '{qid}' type differs: EN={en_q.get('type')!r} "
                    f"HE={he_q.get('type')!r}",
                )
            )
            continue
        qtype = en_q.get("type")
        if qtype == "multiple-choice":
            en_correct = [i for i, c in enumerate(en_q.get("choices") or []) if c.get("correct")]
            he_correct = [i for i, c in enumerate(he_q.get("choices") or []) if c.get("correct")]
            if en_correct != he_correct:
                findings.append(
                    Finding(
                        he_path,
                        None,
                        "error",
                        f"mismatch: question '{qid}' correct-choice index differs: "
                        f"EN={en_correct} HE={he_correct}",
                    )
                )
        elif qtype == "numeric":
            if en_q.get("answer") != he_q.get("answer") or en_q.get("tolerance") != he_q.get(
                "tolerance"
            ):
                findings.append(
                    Finding(
                        he_path,
                        None,
                        "error",
                        f"mismatch: question '{qid}' numeric answer/tolerance differs: "
                        f"EN=({en_q.get('answer')!r}, {en_q.get('tolerance')!r}) "
                        f"HE=({he_q.get('answer')!r}, {he_q.get('tolerance')!r})",
                    )
                )
    return findings


def check_quiz_parity(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    quiz_dir = root / "assessment" / "quizzes"
    if not quiz_dir.exists():
        return findings

    for en_path in sorted(quiz_dir.glob("*.en.yml")):
        module = en_path.name[: -len(".en.yml")]
        he_path = quiz_dir / f"{module}.he.yml"
        if not he_path.exists():
            findings.append(
                Finding(en_path, None, "error", f"missing: HE quiz bank missing: {he_path.name}")
            )
            continue
        findings.extend(check_quiz_pair(en_path, he_path))

    for he_path in sorted(quiz_dir.glob("*.he.yml")):
        module = he_path.name[: -len(".he.yml")]
        if not (quiz_dir / f"{module}.en.yml").exists():
            findings.append(
                Finding(
                    he_path,
                    None,
                    "error",
                    f"mismatch: HE quiz bank has no EN source ({module}.en.yml)",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Media: figure targets resolve, and both language trees hold the same files
# ---------------------------------------------------------------------------

FIGURE_TARGET_RE = re.compile(r"^:{3,}\{(?:figure|image)\}\s*(\S+)\s*$", re.MULTILINE)
MEDIA_SUFFIXES = frozenset({".gif", ".mp4", ".png", ".jpg", ".jpeg", ".svg", ".webp"})


def check_figure_targets(root: Path) -> list[Finding]:
    """Every {figure}/{image} target must exist on disk.

    Without this a renamed or re-encoded animation leaves the page pointing at a file that is
    no longer there: mystmd emits the broken URL without complaint, the reader sees an empty
    box, and every other validator stays green. Renaming media is exactly what this project
    does whenever a render script changes format, so the gap was worth closing.
    """
    findings: list[Finding] = []
    for page in iter_content_pages(root):
        for match in FIGURE_TARGET_RE.finditer(page.text):
            target = match.group(1)
            if "://" in target or target.startswith("#"):
                continue
            resolved = (page.path.parent / target).resolve()
            if not resolved.exists():
                line = page.text[: match.start()].count("\n") + 1
                findings.append(
                    Finding(page.path, line, "error", f"missing: figure target {target}")
                )
    return findings


def check_media_trees(root: Path) -> list[Finding]:
    """The two language media trees must hold the same filenames.

    The render scripts encode once and copy the bytes into each tree, so they agree only as
    long as that copy completes. An interrupted render would leave English with an animation
    Hebrew lacks, and nothing else would notice.
    """
    names = {}
    for lang in LANGS:
        media_dir = root / "content" / lang / "media"
        names[lang] = {
            p.name for p in media_dir.glob("*") if p.suffix.lower() in MEDIA_SUFFIXES
        } if media_dir.exists() else set()

    findings: list[Finding] = []
    for lang, other in (("en", "he"), ("he", "en")):
        for name in sorted(names[lang] - names[other]):
            findings.append(
                Finding(
                    root / "content" / lang / "media" / name,
                    None,
                    "error",
                    f"mismatch: {name} exists in {lang} but not in {other}",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def check(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    pending = load_pending(root)

    tree_findings, common_pages = check_page_tree(root, pending)
    findings.extend(tree_findings)
    pending_page_tails = {p[len("content/en/") :] for p in pending if p.startswith("content/en/")}
    for tail in sorted(common_pages):
        findings.extend(check_page_pair(root, tail, pending_tail=tail in pending_page_tails))

    nb_findings, common_notebooks = check_notebook_tree(root, pending)
    findings.extend(nb_findings)
    pending_nb_tails = {p[len("notebooks/en/") :] for p in pending if p.startswith("notebooks/en/")}
    for tail in sorted(common_notebooks):
        findings.extend(check_notebook_pair(root, tail, pending_tail=tail in pending_nb_tails))

    findings.extend(check_quiz_parity(root))
    findings.extend(check_figure_targets(root))
    findings.extend(check_media_trees(root))
    return findings


def _category(finding: Finding) -> str:
    for prefix in CATEGORY_PREFIXES:
        if finding.message.startswith(prefix + ":"):
            return prefix
    return "other"


def parity_json(findings: list[Finding]) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = {c: [] for c in (*CATEGORY_PREFIXES, "other")}
    for finding in findings:
        grouped[_category(finding)].append(finding.to_json())
    return grouped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    findings = check()
    if args.json:
        ensure_stdout_can_print_unicode()
        print(json.dumps(parity_json(findings), indent=2, ensure_ascii=False))
        return 1 if any(f.severity == "error" for f in findings) else 0
    return report(findings, as_json=False)


if __name__ == "__main__":
    raise SystemExit(main())
