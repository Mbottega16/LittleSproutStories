"""
Extracts a per-book JSON spec from a published books/*.html file.

Exists to bring build_pipeline/specs/*.json back in step with the REAL,
already-published books (not guessed content). Every field below is pulled
out of the live HTML by pattern. It is strict on purpose: if a book has a
shape this script does not know, it stops with an error instead of
guessing.

Rewritten 2026-11-22 for the current "watercolor" template (one illustration
per page, `.art`), after the old extractor and the old specs fell behind
the published books (the specs had 8 pages per book; the live books have 12).

Usage:
    python build_pipeline/extract_spec.py books/Book1_Maya_Marcus_FireStation.html
    python build_pipeline/extract_spec.py --all

Warning: this overwrites specs/<book>.json. It keeps the analyzer fields
`reading_level` and `practice_words` if the old spec had them.
"""

import html as htmllib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import amp  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = REPO_ROOT / "books"
SPECS_DIR = Path(__file__).resolve().parent / "specs"

KEEP_FROM_OLD_SPEC = ("reading_level", "practice_words")


def _one(pattern: str, text: str, what: str, flags: int = 0) -> re.Match:
    m = re.search(pattern, text, flags)
    if not m:
        raise ValueError(f"Could not find {what}")
    return m


def _js_const(tail: str, name: str) -> str:
    return _one(r'const %s = "(.*?)";' % name, tail, f"JS const {name}").group(1)


def extract_quiz(page_html: str) -> dict | None:
    m = re.search(
        r'<div class="quiz" data-answer="(\d+)" role="group" aria-label="Question">\s*'
        r'<p class="quiz-q">(.*?)</p>\s*<div class="quiz-opts">(.*?)</div>\s*'
        r'<p class="quiz-feedback" role="status" aria-live="polite"></p>\s*</div>',
        page_html,
        re.DOTALL,
    )
    if not m:
        if 'class="quiz"' in page_html:
            raise ValueError("A quiz is present but did not match the known shape")
        return None
    options = re.findall(
        r'<button type="button" onclick="checkAnswer\(this,(\d+)\)">(.*?)</button>',
        m.group(3),
    )
    ordered = [text for _, text in sorted(options, key=lambda p: int(p[0]))]
    return {"question": m.group(2), "options": ordered, "answer": int(m.group(1))}


def _art(block: str, default_alt: str, extra_attr: str) -> dict:
    m = _one(
        r'<div class="art"><img src="\.\./assets/([^"]+)" alt="([^"]*)" %s></div>' % extra_attr,
        block,
        "the page illustration",
    )
    out = {"image": m.group(1)}
    if m.group(2) != default_alt:
        out["alt"] = m.group(2)  # only stored when it is not the default pattern
    return out


def extract_book(html: str) -> dict:
    head, rest = html.split('<main id="bookMain">', 1)
    main, tail = rest.split("</main>", 1)

    title = htmllib.unescape(
        _one(r"<title>(.*?) \| Little Sprout Stories</title>", head, "<title>").group(1)
    )
    book_id = _js_const(tail, "BOOK_ID")
    spec = {
        "book_id": book_id,
        "title": title,
        "book_title": _js_const(tail, "BOOK_TITLE"),
        "book_badge": _js_const(tail, "BOOK_BADGE"),
    }

    blocks = re.split(r'(?=<div class="page-wrap" id="p\d+")', main)
    blocks = [b for b in blocks if b.strip()]
    cover_block, page_blocks, end_block = blocks[0], blocks[1:-1], blocks[-1]

    # --- cover
    cover = {
        "h1_html": _one(r"<h1>(.*?)</h1>", cover_block, "cover <h1>").group(1),
        "subtitle": _one(r'<p class="subtitle">(.*?)</p>', cover_block, "cover subtitle").group(1),
    }
    cover.update(_art(cover_block, f"{amp(title)} — cover art", 'fetchpriority="high"'))
    spec["cover"] = cover

    # --- interior pages
    pages = []
    for block in page_blocks:
        idx = int(_one(r'id="p(\d+)"', block, "page id").group(1))
        page = {"index": idx}
        page.update(_art(block, f"Illustration for page {idx} of {amp(title)}", 'loading="lazy"'))
        page["text_a"] = _one(r'<div class="text-a">(.*?)</div>', block, f"text_a p{idx}", re.S).group(1)
        page["text_b"] = _one(r'<div class="text-b">(.*?)</div>', block, f"text_b p{idx}", re.S).group(1)
        page["quiz"] = extract_quiz(block)
        pages.append(page)
    spec["pages"] = pages

    # --- end screen ("For Grown-Ups")
    def guide(label: str) -> str:
        return _one(r"<p><b>%s:</b> (.*?)</p>" % re.escape(label), end_block, f"guide '{label}'", re.S).group(1)

    badge = _one(
        r'<div class="badge"><span aria-hidden="true">(.*?)</span><div>(.*?)</div></div>',
        end_block,
        "end-screen badge",
    )
    spec["end_screen"] = {
        "badge_emoji": badge.group(1),
        "badge_label_html": badge.group(2),
        "feeling": guide("Feeling/skill"),
        "ask": guide("Ask your child"),
        "try_this": guide("Try this"),
        "words_to_grow": guide("Words to grow on"),
        "bigger_picture": guide("The bigger picture"),
        "standards": _one(r'<p class="standards">Standards: (.*?)</p>', end_block, "standards").group(1),
    }
    return spec


def extract_file(book_path: Path) -> Path:
    # newline="" keeps the file's own line endings untouched
    html = book_path.read_text(encoding="utf-8", newline="")
    spec = extract_book(html)
    out_path = SPECS_DIR / (book_path.stem + ".json")
    if out_path.exists():
        old = json.loads(out_path.read_text(encoding="utf-8"))
        for key in KEEP_FROM_OLD_SPEC:
            if key in old:
                spec[key] = old[key]
    out_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return out_path


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--all":
        targets = sorted(BOOKS_DIR.glob("Book*.html"))
    elif len(sys.argv) == 2:
        targets = [Path(sys.argv[1])]
    else:
        print("Usage: python extract_spec.py <books/BookN_....html> | --all")
        return 1
    for path in targets:
        out = extract_file(path)
        print(f"{path.name} -> {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
