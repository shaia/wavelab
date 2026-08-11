"""Stamp `en_source_hash` into Hebrew pages once their translation is finished.

A Hebrew page records the hash of the English source it was translated from, so
`check_parity.py` can tell "translated and current" from "translated, then the English
changed underneath it". Running this is the deliberate act of saying "this translation is
up to date" — which is why it is a separate step from writing the translation, and why it
refuses to touch a page still marked PENDING unless you ask for it explicitly.

Run:  uv run python scripts/stamp_hashes.py [--pending] [path ...]
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "content" / "en"
HE_ROOT = ROOT / "content" / "he"

_YAML_HASH_RE = re.compile(r"^en_source_hash:\s*(.*)$", re.MULTILINE)
_COMMENT_HASH_RE = re.compile(r"^%\s*en_source_hash:\s*(.*)$", re.MULTILINE)


def source_hash(path: Path) -> str:
    """sha256 with line endings normalised, matching scripts/_content.py."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def stamp(he_path: Path, include_pending: bool) -> str | None:
    en_path = EN_ROOT / he_path.relative_to(HE_ROOT)
    if not en_path.exists():
        return f"{he_path.relative_to(ROOT)}: no English source — skipped"

    text = he_path.read_text(encoding="utf-8")
    pattern = _YAML_HASH_RE if _YAML_HASH_RE.search(text) else _COMMENT_HASH_RE
    match = pattern.search(text)
    if not match:
        return f"{he_path.relative_to(ROOT)}: no en_source_hash field — skipped"

    current = match.group(1).strip()
    expected = source_hash(en_path)
    if current == expected:
        return None
    if current == "PENDING" and not include_pending:
        return f"{he_path.relative_to(ROOT)}: still PENDING (pass --pending to stamp it)"

    he_path.write_text(pattern.sub(match.group(0).split(":")[0] + f": {expected}", text, count=1),
                       encoding="utf-8")
    return f"{he_path.relative_to(ROOT)}: stamped {expected[:12]}…"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pending",
        action="store_true",
        help="also stamp pages whose hash is still PENDING (i.e. declare them translated)",
    )
    parser.add_argument("paths", nargs="*", help="specific Hebrew pages; default is all of them")
    args = parser.parse_args(argv)

    # `_build` holds the downloaded MyST theme, whose node_modules carry thousands of READMEs.
    # Walking them buried the real output in "no en_source_hash field" lines.
    targets = [Path(p).resolve() for p in args.paths] or sorted(
        p for p in HE_ROOT.rglob("*.md") if "_build" not in p.parts
    )
    messages = [m for p in targets if (m := stamp(p, args.pending))]
    for message in messages:
        print(message)
    if not messages:
        print("all Hebrew pages already carry the current hash")
    return 0


if __name__ == "__main__":
    sys.exit(main())
