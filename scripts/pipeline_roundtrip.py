"""
Round-trip guard: is books/*.html exactly what the build pipeline renders
from build_pipeline/specs/*.json?

Why this exists: the pipeline fell out of step with the published books once
(2026-08 to 2026-11). The books were edited by hand, the specs and the
renderer were not, and a rebuild would have overwritten the live books with
an old version. This script catches that the day it happens.

Usage (from the repo root):
    python scripts/pipeline_roundtrip.py

Exit 0: every book matches its spec. Exit 1: something differs.
It never writes to books/.

If it fails because a book was edited by hand:
    python build_pipeline/extract_spec.py --all     # copy the book's text back into the specs
    python scripts/pipeline_roundtrip.py            # should pass now
If it fails because a spec or template was edited on purpose:
    python build_pipeline/build.py                  # rebuild the books
"""

import difflib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "build_pipeline"))

import render  # noqa: E402
from common import read_exact  # noqa: E402


def main() -> int:
    specs = {p.stem: p for p in sorted(render.SPECS_DIR.glob("Book*.json"))}
    books = {p.stem: p for p in sorted(render.BOOKS_DIR.glob("Book*.html"))}
    problems = []

    for stem in sorted(set(specs) | set(books)):
        if stem not in books:
            problems.append(f"{stem}: has a spec but no books/{stem}.html")
            continue
        if stem not in specs:
            problems.append(f"{stem}: has a book but no spec in build_pipeline/specs/")
            continue
        spec = json.loads(specs[stem].read_text(encoding="utf-8"))
        wanted = render.render_book(spec)
        actual = read_exact(books[stem])
        if wanted != actual:
            first = next(
                (line for line in difflib.unified_diff(
                    actual.splitlines(), wanted.splitlines(), "books/" + stem, "rendered", n=0, lineterm="")
                 if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))),
                "(line endings or trailing text differ)",
            )
            problems.append(f"{stem}: books/ differs from what the specs render. First difference: {first[:160]}")

    if problems:
        print(f"{len(problems)} problem(s):")
        for line in problems:
            print("  " + line)
        print("\nFix: if a book was edited by hand, run  python build_pipeline/extract_spec.py --all"
              "\n     if a spec or template was edited, run  python build_pipeline/build.py")
        return 1
    print(f"OK: all {len(books)} books match what the pipeline renders from their specs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
