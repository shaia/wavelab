"""Tests for the content-validation scripts under `scripts/`.

Every validator here is exercised both ways: a deliberately broken fixture must
produce an "error" Finding, and a clean fixture must produce none. A validator that
can only ever pass is worse than no validator at all, so each `test_fails_on_*` is
the load-bearing half of its pair.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_assessment  # noqa: E402
import check_glossary  # noqa: E402
import check_modelspec  # noqa: E402
import check_notebooks  # noqa: E402
import check_parity  # noqa: E402

from _content import sha256_normalized  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def write_notebook(path: Path, code_sources: list[str], en_source_hash: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbformat.v4.new_notebook()
    for source in code_sources:
        nb.cells.append(nbformat.v4.new_code_cell(source))
    if en_source_hash is not None:
        nb.metadata["thermolab"] = {"en_source_hash": en_source_hash}
    nbformat.write(nb, path)


def has_error(findings, snippet: str) -> bool:
    return any(f.severity == "error" and snippet in f.message for f in findings)


def has_warning(findings, snippet: str) -> bool:
    return any(f.severity == "warning" and snippet in f.message for f in findings)


MODULE_LABEL_SUFFIXES = (
    "puzzle",
    "predict",
    "explore",
    "derive",
    "verify",
    "transfer",
    "quiz",
    "explain",
)


def good_module_page(
    slug: str,
    *,
    objectives: tuple[str, ...] = ("OBJ-1", "OBJ-2"),
    skip_suffixes: tuple[str, ...] = (),
    include_epistemic: bool = True,
    extra_body: str = "",
) -> str:
    """A minimal but fully compliant module page: front matter with objectives:,
    every required section label in order, one 7-bullet model-spec block, and one
    epistemic admonition — the baseline that check_modelspec.py must accept.
    """
    if objectives:
        objectives_yaml = "\n".join(
            f'  - id: {oid}\n    text: "objective {oid}"' for oid in objectives
        )
        objectives_block = f"objectives:\n{objectives_yaml}"
    else:
        objectives_block = "objectives: []"

    sections = "\n\n".join(
        f"({slug}-{suffix})=\n## {suffix.title()}\n\nBody text."
        for suffix in MODULE_LABEL_SUFFIXES
        if suffix not in skip_suffixes
    )

    epistemic_block = (
        ":::{admonition} A definition\n:class: definition\nSome defined term.\n:::\n"
        if include_epistemic
        else ""
    )

    return f"""---
title: "{slug}"
module: {slug}
{objectives_block}
---

# {slug}

{sections}

:::{{admonition}} Model specification
:class: model-spec
- **System:** a.
- **Dynamics:** b.
- **Boundary:** c.
- **Ensemble:** d.
- **Ignored:** e.
- **Valid when:** f.
- **Failure modes:** g.
:::

{epistemic_block}{extra_body}
"""


# ---------------------------------------------------------------------------
# check_modelspec.py
# ---------------------------------------------------------------------------


class TestCheckModelspec:
    def test_empty_repo_returns_no_findings(self, tmp_path):
        assert check_modelspec.check(tmp_path) == []

    def test_passes_on_complete_page(self, tmp_path):
        write(tmp_path / "content" / "en" / "04-demo.md", good_module_page("04-demo"))
        assert check_modelspec.check(tmp_path) == []

    def test_fails_on_missing_label(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "04-demo.md",
            good_module_page("04-demo", skip_suffixes=("derive",)),
        )
        findings = check_modelspec.check(tmp_path)
        assert has_error(findings, "missing required label (04-demo-derive)=")

    def test_fails_on_wrong_model_spec_bullet_count(self, tmp_path):
        text = good_module_page("04-demo").replace("- **Failure modes:** g.\n", "")
        write(tmp_path / "content" / "en" / "04-demo.md", text)
        findings = check_modelspec.check(tmp_path)
        assert has_error(findings, "model-spec block has 6 top-level bullets, expected exactly 7")

    def test_fails_on_sign_convention_violation(self, tmp_path):
        text = good_module_page("04-demo", extra_body="The engine does $W_{by}$ work.\n")
        write(tmp_path / "content" / "en" / "04-demo.md", text)
        findings = check_modelspec.check(tmp_path)
        assert has_error(findings, "W_{by}")

    def test_sign_convention_exempt_with_marker_comment(self, tmp_path):
        text = good_module_page(
            "04-demo",
            extra_body="<!-- sign-convention-exception -->\nThe engine does $W_{by}$ work.\n",
        )
        write(tmp_path / "content" / "en" / "04-demo.md", text)
        findings = check_modelspec.check(tmp_path)
        assert not has_error(findings, "W_{by}")

    def test_sign_convention_exempt_in_conventions_file(self, tmp_path):
        write(tmp_path / "content" / "en" / "conventions.md", "The engine does $W_{by}$ work.\n")
        findings = check_modelspec.check(tmp_path)
        assert not has_error(findings, "W_{by}")

    def test_warns_when_no_epistemic_admonition(self, tmp_path):
        text = good_module_page("04-demo", include_epistemic=False)
        write(tmp_path / "content" / "en" / "04-demo.md", text)
        findings = check_modelspec.check(tmp_path)
        assert has_warning(findings, "no epistemic admonition")

    def test_fails_on_empty_objectives(self, tmp_path):
        text = good_module_page("04-demo", objectives=())
        write(tmp_path / "content" / "en" / "04-demo.md", text)
        findings = check_modelspec.check(tmp_path)
        assert has_error(findings, "objectives")

    def test_module_flag_scopes_to_one_module(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "04-demo.md",
            good_module_page("04-demo", skip_suffixes=("derive",)),
        )
        write(tmp_path / "content" / "en" / "05-other.md", good_module_page("05-other"))
        findings = check_modelspec.check(tmp_path, module="05-other")
        assert findings == []


# ---------------------------------------------------------------------------
# check_glossary.py
# ---------------------------------------------------------------------------

GLOSSARY_YAML = """
terms:
  - key: entropy
    en: entropy
    he: אנטרופיה
    he_reject: [אנתרופיה]
  - key: pressure
    en: pressure
    he: לחץ
"""


class TestCheckGlossary:
    def test_empty_repo_returns_no_findings(self, tmp_path):
        assert check_glossary.check(tmp_path) == []

    def test_passes_on_clean_hebrew(self, tmp_path):
        write(tmp_path / "glossary" / "terms.yml", GLOSSARY_YAML)
        write(tmp_path / "content" / "he" / "page.md", "# כותרת\n\nהאנטרופיה של הגז גדלה.\n")
        assert check_glossary.check(tmp_path) == []

    def test_fails_on_he_reject_spelling(self, tmp_path):
        write(tmp_path / "glossary" / "terms.yml", GLOSSARY_YAML)
        write(tmp_path / "content" / "he" / "page.md", "# כותרת\n\nהמושג אנתרופיה חשוב כאן.\n")
        findings = check_glossary.check(tmp_path)
        assert has_error(findings, "rejected spelling")

    def test_warns_on_untranslated_english_term(self, tmp_path):
        write(tmp_path / "glossary" / "terms.yml", GLOSSARY_YAML)
        write(tmp_path / "content" / "he" / "page.md", "# כותרת\n\nה-pressure כאן גבוה.\n")
        findings = check_glossary.check(tmp_path)
        assert has_warning(findings, "English term 'pressure'")

    def test_ignores_english_term_inside_math_and_code(self, tmp_path):
        write(tmp_path / "glossary" / "terms.yml", GLOSSARY_YAML)
        write(
            tmp_path / "content" / "he" / "page.md",
            "# כותרת\n\nנוסחה $pressure = F/A$ וגם `pressure` בקוד.\n",
        )
        findings = check_glossary.check(tmp_path)
        assert not has_warning(findings, "pressure")

    def test_fails_on_duplicate_glossary_key(self, tmp_path):
        write(
            tmp_path / "glossary" / "terms.yml",
            "terms:\n  - key: entropy\n    en: entropy\n    he: א\n"
            "  - key: entropy\n    en: entropy\n    he: ב\n",
        )
        findings = check_glossary.check(tmp_path)
        assert has_error(findings, "duplicate glossary key")

    def test_fails_on_missing_he_value(self, tmp_path):
        write(tmp_path / "glossary" / "terms.yml", "terms:\n  - key: entropy\n    en: entropy\n")
        findings = check_glossary.check(tmp_path)
        assert has_error(findings, "missing a Hebrew")


# ---------------------------------------------------------------------------
# check_parity.py
# ---------------------------------------------------------------------------


class TestCheckParity:
    def test_empty_repo_returns_no_findings(self, tmp_path):
        assert check_parity.check(tmp_path) == []

    def test_fails_on_missing_he_page(self, tmp_path):
        write(tmp_path / "content" / "en" / "page.md", "# Page\n\nSome text.\n")
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "missing: HE translation missing for content/en/page.md")

    def test_fails_on_stale_hash(self, tmp_path):
        write(tmp_path / "content" / "en" / "page.md", "# Page\n\nSome text with $E = m c^2$.\n")
        write(
            tmp_path / "content" / "he" / "page.md",
            '---\nen_source_hash: "deadbeef"\n---\n\n# עמוד\n\nטקסט עם $E = m c^2$.\n',
        )
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "stale: en_source_hash mismatch")

    def test_passes_on_matching_hash_and_equations(self, tmp_path):
        en_path = tmp_path / "content" / "en" / "page.md"
        write(en_path, "# Page\n\nSome text with $E = m c^2$.\n")
        expected_hash = sha256_normalized(en_path.read_bytes())
        write(
            tmp_path / "content" / "he" / "page.md",
            f'---\nen_source_hash: "{expected_hash}"\n---\n\n# עמוד\n\nטקסט עם $E = m c^2$.\n',
        )
        assert check_parity.check(tmp_path) == []

    def test_pending_hash_warns_when_listed(self, tmp_path):
        write(tmp_path / "content" / "en" / "page.md", "# Page\n\nText.\n")
        write(
            tmp_path / "content" / "he" / "page.md",
            "% en_source_hash: PENDING\n\n# עמוד\n\nטקסט.\n",
        )
        write(tmp_path / "translation-pending.txt", "content/en/page.md\n")
        findings = check_parity.check(tmp_path)
        assert has_warning(findings, "PENDING")
        assert not has_error(findings, "PENDING")

    def test_pending_hash_errors_when_not_listed(self, tmp_path):
        write(tmp_path / "content" / "en" / "page.md", "# Page\n\nText.\n")
        write(
            tmp_path / "content" / "he" / "page.md",
            "% en_source_hash: PENDING\n\n# עמוד\n\nטקסט.\n",
        )
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "PENDING")

    def test_fails_on_mutated_equation(self, tmp_path):
        en_path = tmp_path / "content" / "en" / "page.md"
        write(en_path, "# Page\n\n$$P V = N k_B T$$\n")
        expected_hash = sha256_normalized(en_path.read_bytes())
        write(
            tmp_path / "content" / "he" / "page.md",
            f'---\nen_source_hash: "{expected_hash}"\n---\n\n# עמוד\n\n$$P V = N k_B T + 1$$\n',
        )
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "equation count differs")

    def test_fails_on_missing_he_notebook(self, tmp_path):
        write_notebook(tmp_path / "notebooks" / "en" / "lab.ipynb", ["x = 1"])
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "missing: HE notebook missing for notebooks/en/lab.ipynb")

    def test_fails_on_notebook_code_cell_mismatch(self, tmp_path):
        en_nb_path = tmp_path / "notebooks" / "en" / "lab.ipynb"
        write_notebook(en_nb_path, ["x = 1"])
        expected_hash = sha256_normalized(en_nb_path.read_bytes())
        write_notebook(
            tmp_path / "notebooks" / "he" / "lab.ipynb", ["x = 2"], en_source_hash=expected_hash
        )
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "code cell 0 differs")

    def test_passes_on_matching_notebook_pair(self, tmp_path):
        en_nb_path = tmp_path / "notebooks" / "en" / "lab.ipynb"
        write_notebook(en_nb_path, ["x = 1"])
        expected_hash = sha256_normalized(en_nb_path.read_bytes())
        write_notebook(
            tmp_path / "notebooks" / "he" / "lab.ipynb", ["x = 1"], en_source_hash=expected_hash
        )
        assert check_parity.check(tmp_path) == []

    def test_fails_on_mismatched_quiz_ids(self, tmp_path):
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    objectives: [OBJ-1]\n"
            "    answer: 1\n    tolerance: 0.1\n",
        )
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.he.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q2\n    type: numeric\n    objectives: [OBJ-1]\n"
            "    answer: 1\n    tolerance: 0.1\n",
        )
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "present in EN bank but missing in HE")
        assert has_error(findings, "present in HE bank but missing in EN")

    def test_fails_on_figure_pointing_at_a_missing_file(self, tmp_path):
        # The failure mode of any media rename: mystmd emits the dead URL silently and the
        # reader gets an empty box, so nothing but this check would catch it.
        write(
            tmp_path / "content" / "en" / "page.md",
            "# Page\n\n:::{figure} ../media/gone.mp4\n:alt: a\n:::\n",
        )
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "missing: figure target ../media/gone.mp4")

    def test_passes_when_figure_target_exists(self, tmp_path):
        media = tmp_path / "content" / "media"
        media.mkdir(parents=True)
        (media / "there.mp4").write_bytes(b"\x00")
        write(
            tmp_path / "content" / "en" / "page.md",
            "# Page\n\n:::{figure} ../media/there.mp4\n:alt: a\n:::\n",
        )
        assert not has_error(check_parity.check(tmp_path), "figure target")

    def test_ignores_remote_figure_urls(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "page.md",
            "# Page\n\n:::{figure} https://example.org/x.png\n:alt: a\n:::\n",
        )
        assert not has_error(check_parity.check(tmp_path), "figure target")

    def test_fails_when_media_trees_disagree(self, tmp_path):
        (tmp_path / "content" / "en" / "media").mkdir(parents=True)
        (tmp_path / "content" / "he" / "media").mkdir(parents=True)
        (tmp_path / "content" / "en" / "media" / "solo.mp4").write_bytes(b"\x00")
        findings = check_parity.check(tmp_path)
        assert has_error(findings, "mismatch: solo.mp4 exists in en but not in he")

    def test_passes_when_media_trees_agree(self, tmp_path):
        for lang in ("en", "he"):
            media = tmp_path / "content" / lang / "media"
            media.mkdir(parents=True)
            (media / "both.mp4").write_bytes(b"\x00")
        assert not has_error(check_parity.check(tmp_path), "exists in")


# ---------------------------------------------------------------------------
# check_assessment.py
# ---------------------------------------------------------------------------


class TestCheckAssessment:
    def test_empty_repo_returns_no_findings(self, tmp_path):
        assert check_assessment.check(tmp_path) == []

    def test_fails_on_missing_feedback_on_distractor(self, tmp_path):
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: multiple-choice\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    choices:\n"
            "      - text: Right\n        correct: true\n        feedback: Yes.\n"
            "      - text: Wrong\n        correct: false\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "choice 1 missing feedback")

    def test_fails_on_more_than_one_correct_choice(self, tmp_path):
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: multiple-choice\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    choices:\n"
            "      - text: A\n        correct: true\n        feedback: f\n"
            "      - text: B\n        correct: true\n        feedback: f\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "has 2 correct choices")

    def test_fails_on_numeric_missing_tolerance(self, tmp_path):
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    answer: 1\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "needs answer and tolerance")

    def test_fails_on_prediction_missing_discussion(self, tmp_path):
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: prediction\n    prompt: p\n    objectives: [OBJ-1]\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "needs discussion")

    def test_passes_on_well_formed_bank(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "04-demo.md",
            good_module_page("04-demo", objectives=("OBJ-1",)),
        )
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: multiple-choice\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    choices:\n"
            "      - text: A\n        correct: true\n        feedback: f\n"
            "      - text: B\n        correct: false\n        feedback: f\n"
            "  - id: Q2\n    type: numeric\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    answer: 1.0\n    tolerance: 0.1\n"
            "  - id: Q3\n    type: prediction\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    discussion: d\n"
            "  - id: Q4\n    type: short-answer\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    discussion: d\n",
        )
        assert check_assessment.check(tmp_path, module="04-demo") == []

    def test_fails_on_objective_not_covered_by_any_quiz_or_exam(self, tmp_path):
        write(tmp_path / "content" / "en" / "04-demo.md", good_module_page("04-demo"))
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "not covered by any quiz or exam question")

    def test_fails_on_reference_to_unknown_objective(self, tmp_path):
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: p\n    objectives: [OBJ-999]\n"
            "    answer: 1\n    tolerance: 0.1\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "unknown objective id 'OBJ-999'")

    def test_hebrew_coverage_fails_independently_of_english(self, tmp_path):
        # EN has the page + a quiz covering OBJ-1; HE has the page but no quiz/exam
        # yet, so HE coverage must fail even though EN passes.
        write(
            tmp_path / "content" / "en" / "04-demo.md",
            good_module_page("04-demo", objectives=("OBJ-1",)),
        )
        write(
            tmp_path / "content" / "he" / "04-demo.md",
            good_module_page("04-demo", objectives=("OBJ-1",)),
        )
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    answer: 1\n    tolerance: 0.1\n",
        )
        findings = check_assessment.check(tmp_path)
        assert not has_error(findings, "'OBJ-1' (en, module 04-demo) is not covered")
        assert has_error(findings, "'OBJ-1' (he, module 04-demo) is not covered")

    def test_scoped_run_does_not_blame_other_modules_misconceptions(self, tmp_path):
        """A --module run must still read every bank when checking misconception coverage.

        Otherwise every *other* module's addressed misconception looks unreferenced, and an
        author scoping the lint to their own module learns to skim past real errors.
        """
        write(
            tmp_path / "assessment" / "misconceptions.yml",
            "misconceptions:\n"
            "  - id: mine\n    statement: s\n    assigned_module: 04-demo\n    status: addressed\n"
            "  - id: theirs\n    statement: s\n    assigned_module: 05-other\n"
            "    status: addressed\n",
        )
        for slug, mid in (("04-demo", "mine"), ("05-other", "theirs")):
            write(
                tmp_path / "content" / "en" / f"{slug}.md",
                good_module_page(slug, objectives=("OBJ-1",)),
            )
            write(
                tmp_path / "assessment" / "quizzes" / f"{slug}.en.yml",
                f"module: {slug}\nquestions:\n"
                f"  - id: Q1\n    type: numeric\n    prompt: p\n    objectives: [OBJ-1]\n"
                f"    misconception: {mid}\n    answer: 1\n    tolerance: 0.1\n",
            )

        findings = check_assessment.check(tmp_path, module="04-demo")

        assert not has_error(findings, "'theirs' is addressed but no quiz question")
        assert not has_error(findings, "'mine' is addressed but no quiz question")

    def test_scoped_run_still_reports_its_own_uncovered_misconception(self, tmp_path):
        """The narrowing must not become a way to hide the scoped module's own gap."""
        write(
            tmp_path / "assessment" / "misconceptions.yml",
            "misconceptions:\n"
            "  - id: mine\n    statement: s\n    assigned_module: 04-demo\n    status: addressed\n",
        )
        write(
            tmp_path / "content" / "en" / "04-demo.md",
            good_module_page("04-demo", objectives=("OBJ-1",)),
        )
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    answer: 1\n    tolerance: 0.1\n",
        )

        findings = check_assessment.check(tmp_path, module="04-demo")

        assert has_error(findings, "'mine' is addressed but no quiz question references it")

    def test_fails_on_answer_key_string_in_content(self, tmp_path):
        write(tmp_path / "content" / "en" / "page.md", "See the answer_key for solutions.\n")
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "answer_key")

    def test_fails_on_instructor_reference_in_content(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "page.md",
            "```{include} ../../instructor/solutions/04.md\n```\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "instructor/")

    def test_fails_on_problem_set_with_no_instructor_solutions(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "04-demo-problems.md",
            "# Problems\n\n## Problem 1 - one\n\nDo it.\n",
        )
        write(tmp_path / "instructor" / "solutions" / "05-other.md", "# Solutions\n")
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "instructor/solutions/04-demo.md")

    def test_stays_silent_when_there_is_no_instructor_tree_at_all(self, tmp_path):
        # instructor/ is gitignored because the repo is public, so a clone has no such
        # tree. Failing there would break validate_all.py for every non-instructor.
        write(
            tmp_path / "content" / "en" / "04-demo-problems.md",
            "# Problems\n\n## Problem 1 - one\n\nDo it.\n",
        )
        assert check_assessment.check(tmp_path) == []

    def test_fails_when_solutions_omit_a_posed_problem(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "04-demo-problems.md",
            "# Problems\n\n## Problem 1 - one\n\nDo it.\n\n## Problem 2 - two\n\nDo it too.\n",
        )
        write(
            tmp_path / "instructor" / "solutions" / "04-demo.md",
            "# Solutions\n\n## Problem 1 - one [10]\n\nHere it is.\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "solutions omit problem(s) 2")

    def test_passes_when_solutions_cover_every_problem(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "04-demo-problems.md",
            "# Problems\n\n## Problem 1 - one\n\nDo it.\n\n## Problem 2 - two\n\nDo it too.\n",
        )
        write(
            tmp_path / "instructor" / "solutions" / "04-demo.md",
            "# Solutions\n\n## Problem 1 - one [10]\n\nA.\n\n## Problem 2 - two [10]\n\nB.\n",
        )
        assert check_assessment.check(tmp_path) == []

    def test_warns_on_pending_misconception_not_yet_written(self, tmp_path):
        write(
            tmp_path / "assessment" / "misconceptions.yml",
            "misconceptions:\n  - id: mc-1\n    statement: s\n"
            "    assigned_module: 04-demo\n    status: pending\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_warning(findings, "module '04-demo' still owes a quiz question")

    def test_warns_on_pending_misconception_already_referenced(self, tmp_path):
        # The quiz already asks about it -- the warning should say so and point at
        # flipping status, distinguishing this from the "not written yet" case above.
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    misconception: mc-1\n    answer: 1\n    tolerance: 0.1\n",
        )
        write(
            tmp_path / "assessment" / "misconceptions.yml",
            "misconceptions:\n  - id: mc-1\n    statement: s\n"
            "    assigned_module: 04-demo\n    status: pending\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_warning(findings, "a quiz question already references it")
        assert has_warning(findings, "consider flipping status to addressed")

    def test_fails_on_addressed_misconception_without_quiz_reference(self, tmp_path):
        write(tmp_path / "content" / "en" / "04-demo.md", good_module_page("04-demo"))
        write(
            tmp_path / "assessment" / "misconceptions.yml",
            "misconceptions:\n  - id: mc-1\n    statement: s\n"
            "    assigned_module: 04-demo\n    status: addressed\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "no quiz question references it")

    def test_passes_on_addressed_misconception_referenced_by_quiz(self, tmp_path):
        write(
            tmp_path / "content" / "en" / "04-demo.md",
            good_module_page("04-demo", objectives=("OBJ-1",)),
        )
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    misconception: mc-1\n    answer: 1\n    tolerance: 0.1\n",
        )
        write(
            tmp_path / "assessment" / "misconceptions.yml",
            "misconceptions:\n  - id: mc-1\n    statement: s\n"
            "    assigned_module: 04-demo\n    status: addressed\n",
        )
        findings = check_assessment.check(tmp_path, module="04-demo")
        assert not has_error(findings, "mc-1")

    def test_fails_on_latex_math_in_quiz_prompt(self, tmp_path):
        """Banks are plain ASCII: a `$…$` here lands in a parity-checked generated page."""
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: 'estimate $N^{-1/2}$'\n"
            "    objectives: [OBJ-1]\n    answer: 1\n    tolerance: 0.1\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "prompt contains '$'")

    def test_fails_on_latex_math_in_choice_feedback(self, tmp_path):
        """The rule covers every authored string, not just the prompt."""
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: multiple-choice\n    prompt: p\n    objectives: [OBJ-1]\n"
            "    choices:\n"
            "      - text: A\n        correct: true\n        feedback: 'because $x$'\n"
            "      - text: B\n        correct: false\n        feedback: f\n",
        )
        findings = check_assessment.check(tmp_path)
        assert has_error(findings, "choices[0].feedback contains '$'")

    def test_passes_on_ascii_math(self, tmp_path):
        write(
            tmp_path / "assessment" / "quizzes" / "04-demo.en.yml",
            "module: 04-demo\nquestions:\n"
            "  - id: Q1\n    type: numeric\n    prompt: 'estimate N^(-1/2)'\n"
            "    objectives: [OBJ-1]\n    answer: 1\n    tolerance: 0.1\n",
        )
        findings = check_assessment.check(tmp_path)
        assert not has_error(findings, "contains '$'")


# ---------------------------------------------------------------------------
# check_notebooks.py
# ---------------------------------------------------------------------------

CANONICAL_BOOTSTRAP = (
    "try:\n"
    "    import piplite\n"
    "except ImportError:\n"
    "    pass\n"
    "else:\n"
    '    await piplite.install(["pint", "ipywidgets", "jupyterquiz"])\n'
    '    await piplite.install("thermolab", deps=False)\n'
)


class TestCheckNotebooks:
    def test_empty_repo_returns_no_findings(self, tmp_path):
        assert check_notebooks.check(tmp_path) == []

    def test_passes_on_canonical_bootstrap(self, tmp_path):
        write_notebook(
            tmp_path / "notebooks" / "en" / "labs" / "04-demo.ipynb",
            [CANONICAL_BOOTSTRAP, "import numpy as np"],
        )
        assert check_notebooks.check(tmp_path) == []

    def test_fails_when_bootstrap_is_missing_entirely(self, tmp_path):
        write_notebook(
            tmp_path / "notebooks" / "en" / "labs" / "04-demo.ipynb", ["import numpy as np"]
        )
        findings = check_notebooks.check(tmp_path)
        assert has_error(findings, "first code cell is not the JupyterLite bootstrap")

    def test_fails_when_thermolab_is_installed_with_its_dependency_graph(self, tmp_path):
        """The real defect: deps come from PyPI, which has no WebAssembly wheels."""
        write_notebook(
            tmp_path / "notebooks" / "en" / "labs" / "04-demo.ipynb",
            [
                "try:\n    import piplite\nexcept ImportError:\n    pass\n"
                'else:\n    await piplite.install("thermolab", keep_going=True)\n'
            ],
        )
        findings = check_notebooks.check(tmp_path)
        assert has_error(findings, "deps=False")
        assert has_error(findings, "pint, ipywidgets, jupyterquiz")

    def test_fails_when_a_pure_python_dependency_is_dropped(self, tmp_path):
        write_notebook(
            tmp_path / "notebooks" / "he" / "labs" / "04-demo.ipynb",
            [CANONICAL_BOOTSTRAP.replace('"jupyterquiz"', '"nothing"')],
        )
        findings = check_notebooks.check(tmp_path)
        assert has_error(findings, "does not install jupyterquiz")

    def test_checks_both_languages(self, tmp_path):
        write_notebook(
            tmp_path / "notebooks" / "en" / "labs" / "04-demo.ipynb", [CANONICAL_BOOTSTRAP]
        )
        write_notebook(tmp_path / "notebooks" / "he" / "labs" / "04-demo.ipynb", ["import numpy"])
        findings = check_notebooks.check(tmp_path)
        assert len(findings) == 1
        assert "he" in str(findings[0].path)
