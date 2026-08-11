"""Shared MyST content-parsing helpers used by the check_*.py validators.

Kept separate from `_findings.py` (which is purely about output formatting) because
several validators need the *same* parsing — front matter, section labels, admonition
blocks, math spans, hashing — and re-deriving it per script would let the parsers
drift out of sync with each other, which is exactly the kind of bug a lint suite is
supposed to catch, not cause.

Front matter is read from a YAML `---` block when present, and/or from leading
`% key: value` MyST comment lines (the convention already used for `en_source_hash`
on Hebrew pages before any module scaffolding existed). YAML wins if a key appears
in both places.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import yaml

LANGS = ("en", "he")

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---[ \t]*\r?\n?", re.DOTALL)
_PERCENT_COMMENT_RE = re.compile(r"^%\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
_LABEL_RE = re.compile(r"^\(([\w-]+)\)=\s*$")
_FENCE_OPEN_RE = re.compile(r"^(:{3,})\{([\w-]+)\}\s*(.*)$")
_CLASS_OPTION_RE = re.compile(r"^:class:\s*(.+)$")
_TOP_BULLET_RE = re.compile(r"^[-*]\s+(.*)$")
_CODE_FENCE_RE = re.compile(r"^([`~]{3,}).*?\n.*?^\1[`~]*[ \t]*$", re.DOTALL | re.MULTILINE)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_DISPLAY_MATH_RE = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)
_INLINE_MATH_RE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", re.DOTALL)
_DIRECTIVE_NAME_RE = re.compile(r"\{[\w-]+\}")
# Slugs, ids and file paths: two or more ASCII word-runs joined by -, _, . or /.
_IDENTIFIER_RE = re.compile(r"[A-Za-z0-9]+(?:[-_./][A-Za-z0-9]+)+")


def is_content_path(path: Path) -> bool:
    """True unless `path` sits inside a generated `_build` directory."""
    return "_build" not in path.parts


def iter_markdown(root: Path) -> Iterator[Path]:
    """Yield every `*.md` file under `root`, skipping generated `_build` output."""
    if not root.exists():
        return
    for path in sorted(root.rglob("*.md")):
        if is_content_path(path):
            yield path


# ---------------------------------------------------------------------------
# Front matter
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    match = _FRONTMATTER_RE.match(text)
    rest = text
    if match:
        try:
            loaded = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            loaded = None
        if isinstance(loaded, dict):
            data.update(loaded)
        rest = text[match.end() :]
    for line in rest.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        comment_match = _PERCENT_COMMENT_RE.match(stripped)
        if comment_match:
            data.setdefault(comment_match.group(1), comment_match.group(2).strip())
            continue
        break  # first real content line ends the leading-comment scan
    return data


# ---------------------------------------------------------------------------
# Section labels: "(slug-suffix)=" on its own line
# ---------------------------------------------------------------------------


def extract_labels(text: str) -> list[tuple[str, int]]:
    """Return (label_name, line_number) for every MyST label in `text`, in order."""
    labels = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = _LABEL_RE.match(line.strip())
        if match:
            labels.append((match.group(1), lineno))
    return labels


# ---------------------------------------------------------------------------
# Admonitions: ":::{directive} title" ... ":class: a b" ... "- bullet" ... ":::"
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Admonition:
    directive: str
    classes: frozenset[str]
    line: int
    bullets: tuple[str, ...]


def extract_admonitions(text: str) -> list[Admonition]:
    """Parse MyST colon-fenced directives, tracking `:class:` options and top-level
    bullets (lines starting with "- "/"* " with no leading indentation).

    Nesting is supported via a stack keyed on the exact fence marker (e.g. `:::` vs
    `::::`), which is how MyST itself disambiguates nested fences.
    """
    admonitions: list[Admonition] = []
    stack: list[dict[str, object]] = []
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        open_match = _FENCE_OPEN_RE.match(stripped)
        if open_match:
            stack.append(
                {
                    "fence": open_match.group(1),
                    "directive": open_match.group(2),
                    "line": lineno,
                    "classes": set(),
                    "bullets": [],
                }
            )
            continue
        if stack and stripped == stack[-1]["fence"]:
            block = stack.pop()
            admonitions.append(
                Admonition(
                    directive=str(block["directive"]),
                    classes=frozenset(block["classes"]),  # type: ignore[arg-type]
                    line=int(block["line"]),  # type: ignore[arg-type]
                    bullets=tuple(block["bullets"]),  # type: ignore[arg-type]
                )
            )
            continue
        if not stack:
            continue
        top = stack[-1]
        class_match = _CLASS_OPTION_RE.match(stripped)
        if class_match:
            top["classes"].update(class_match.group(1).split())  # type: ignore[union-attr]
            continue
        bullet_match = _TOP_BULLET_RE.match(raw_line)
        if bullet_match:
            top["bullets"].append(bullet_match.group(1).strip())  # type: ignore[union-attr]
    return admonitions


# ---------------------------------------------------------------------------
# Code / math / label spans, used both to mask prose and to extract equations
# ---------------------------------------------------------------------------


def _overlaps_any(span: tuple[int, int], others: list[tuple[int, int]]) -> bool:
    start, end = span
    return any(start < e and s < end for s, e in others)


def _code_spans(text: str) -> list[tuple[int, int]]:
    spans = [m.span() for m in _CODE_FENCE_RE.finditer(text)]
    spans += [
        m.span() for m in _INLINE_CODE_RE.finditer(text) if not _overlaps_any(m.span(), spans)
    ]
    return spans


def iter_math_spans(text: str) -> list[tuple[int, int, str, bool]]:
    """Return (start, end, raw_content, is_display) for every math span in `text`,
    skipping any `$` that falls inside a fenced or inline code span.
    """
    code_spans = _code_spans(text)
    spans: list[tuple[int, int, str, bool]] = []
    consumed: list[tuple[int, int]] = []
    for m in _DISPLAY_MATH_RE.finditer(text):
        if _overlaps_any(m.span(), code_spans):
            continue
        spans.append((*m.span(), m.group(1), True))
        consumed.append(m.span())
    for m in _INLINE_MATH_RE.finditer(text):
        if _overlaps_any(m.span(), code_spans) or _overlaps_any(m.span(), consumed):
            continue
        spans.append((*m.span(), m.group(1), False))
    return spans


def extract_equations(text: str) -> list[str]:
    """Raw LaTeX content of every `$...$`/`$$...$$` span in `text`, in document order."""
    return [content for _, _, content, _ in iter_math_spans(text)]


def normalize_equation(raw: str) -> str:
    """Collapse all internal whitespace to single spaces for equation-identity comparison."""
    return " ".join(raw.split())


def mask_non_prose(text: str) -> str:
    """Blank out everything that is not prose, replacing each masked character with a
    space (newlines are preserved) so glossary matching sees only prose while line
    numbers stay accurate.

    Masked: fenced and inline code, math, MyST labels, directive names, and
    identifier-like tokens — slugs, ids and file paths such as `04-pressure`,
    `heat-temperature-same` or `../media/pressure-impacts.gif`. Those legitimately
    contain English words in every language's copy of a page, so flagging them would
    make the glossary check cry wolf on every file and train authors to ignore it.
    """
    code_spans = _code_spans(text)
    math_spans = [(s, e) for s, e, _, _ in iter_math_spans(text)]
    label_spans = [m.span() for m in re.finditer(_LABEL_RE.pattern, text, re.MULTILINE)]
    directive_spans = [m.span() for m in _DIRECTIVE_NAME_RE.finditer(text)]
    identifier_spans = [m.span() for m in _IDENTIFIER_RE.finditer(text)]

    chars = list(text)
    for start, end in (
        *code_spans,
        *math_spans,
        *label_spans,
        *directive_spans,
        *identifier_spans,
    ):
        for idx in range(start, end):
            if chars[idx] != "\n":
                chars[idx] = " "
    return "".join(chars)


# ---------------------------------------------------------------------------
# Hashing (CRLF-normalised, since the repo's checkout converts line endings on Windows)
# ---------------------------------------------------------------------------


def sha256_normalized(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


# ---------------------------------------------------------------------------
# Content pages: content/<lang>/**/*.md, front matter + labels + admonitions parsed once
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContentPage:
    path: Path
    lang: str
    rel_path: str  # POSIX path relative to the repo root
    text: str
    frontmatter: dict[str, object]
    labels: list[tuple[str, int]]
    admonitions: list[Admonition]


def content_root(root: Path, lang: str) -> Path:
    return root / "content" / lang


def iter_content_pages(root: Path) -> Iterator[ContentPage]:
    """Yield every content/<lang>/**/*.md page (both languages), parsed once."""
    for lang in LANGS:
        for path in iter_markdown(content_root(root, lang)):
            text = path.read_text(encoding="utf-8")
            yield ContentPage(
                path=path,
                lang=lang,
                rel_path=path.relative_to(root).as_posix(),
                text=text,
                frontmatter=parse_frontmatter(text),
                labels=extract_labels(text),
                admonitions=extract_admonitions(text),
            )
