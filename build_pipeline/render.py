"""
Renders a books/BookN_*.html file from a build_pipeline/specs/BookN_*.json
spec plus the two shared templates in build_pipeline/templates/.

    templates/book_head.html   everything before <main> (meta tags, CSS, header)
    templates/book_tail.html   everything after </main> (nav row, all the JS)
    specs/<book>.json          the cover, the 12 pages, the quizzes, the
                               "For Grown-Ups" panel

Rewritten 2026-11-22 so the output matches the published "watercolor" books
byte for byte (see build.py). The old version rendered the pre-watercolor
sprite-stage layout and no longer matched the live site.

Usage:
    python render.py <specs/BookN_....json> | --all
    python render.py --all --out <folder>      # write somewhere other than books/
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import amp  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = REPO_ROOT / "books"
SPECS_DIR = Path(__file__).resolve().parent / "specs"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def _template(name: str) -> str:
    # newline="" keeps the template's own line endings untouched
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8", newline="")


def _fill(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace(f"@@{key}@@", value)
    return template


def _art_html(spec: dict, item: dict, default_alt: str, attr: str) -> str:
    alt = item.get("alt", default_alt)
    return f'<div class="art"><img src="../assets/{item["image"]}" alt="{alt}" {attr}></div>'


def render_quiz(quiz: dict | None) -> str:
    if not quiz:
        return ""
    opts = "\n".join(
        f'      <button type="button" onclick="checkAnswer(this,{i})">{text}</button>'
        for i, text in enumerate(quiz["options"])
    )
    return (
        f'<div class="quiz" data-answer="{quiz["answer"]}" role="group" aria-label="Question">\n'
        f'    <p class="quiz-q">{quiz["question"]}</p>\n'
        f'    <div class="quiz-opts">\n'
        f'{opts}\n'
        f'    </div>\n'
        f'    <p class="quiz-feedback" role="status" aria-live="polite"></p>\n'
        f'  </div>'
    )


def render_cover(spec: dict) -> str:
    cover = spec["cover"]
    art = _art_html(spec, cover, f"{amp(spec['title'])} — cover art", 'fetchpriority="high"')
    return (
        f'<div class="page-wrap" id="p0" style="display:block">\n'
        f'<section class="page cover">\n'
        f'  <div class="banner">Little Sprout Stories</div>\n'
        f'  <h1>{cover["h1_html"]}</h1>\n'
        f'  <p class="subtitle">{cover["subtitle"]}</p>\n'
        f'  {art}\n'
        f'  <button class="start-btn" type="button" onclick="nextPage()">Start Reading &#9654;</button>\n'
        f'</section></div>\n'
    )


def render_page(spec: dict, page: dict) -> str:
    n = page["index"]
    art = _art_html(spec, page, f"Illustration for page {n} of {amp(spec['title'])}", 'loading="lazy"')
    quiz_html = render_quiz(page.get("quiz"))
    quiz_block = f"\n  {quiz_html}" if quiz_html else ""
    return (
        f'<div class="page-wrap" id="p{n}" style="display:none">\n'
        f'<section class="page">\n'
        f'  {art}\n'
        f'  <button class="readaloud" type="button" onclick="readPage(this)" aria-label="Read this page out loud">\n'
        f'    <span class="ra-icon" aria-hidden="true">&#128266;</span><span class="ra-label">Read to me</span>\n'
        f'  </button>\n'
        f'  <div class="text-a">{page["text_a"]}</div>\n'
        f'  <div class="text-b">{page["text_b"]}</div>{quiz_block}\n'
        f'</section></div>\n'
    )


def render_end(spec: dict, end_index: int) -> str:
    e = spec["end_screen"]
    return (
        f'<div class="page-wrap" id="p{end_index}" style="display:none">\n'
        f'<section class="page end-screen">\n'
        f'  <div class="badge"><span aria-hidden="true">{e["badge_emoji"]}</span><div>{e["badge_label_html"]}</div></div>\n'
        f'  <h2>Great reading!</h2>\n'
        f'  <p class="saved-note" id="savedNote"></p>\n'
        f'  <details class="guide">\n'
        f'    <summary>For Grown-Ups</summary>\n'
        f'    <p><b>Feeling/skill:</b> {e["feeling"]}</p>\n'
        f'    <p><b>Ask your child:</b> {e["ask"]}</p>\n'
        f'    <p><b>Try this:</b> {e["try_this"]}</p>\n'
        f'    <p><b>Words to grow on:</b> {e["words_to_grow"]}</p>\n'
        f'    <p><b>The bigger picture:</b> {e["bigger_picture"]}</p>\n'
        f'    <p class="standards">Standards: {e["standards"]}</p>\n'
        f'  </details>\n'
        f'  <div class="end-btns">\n'
        f'    <button class="start-btn" type="button" onclick="restart()">Read Again &#9654;</button>\n'
        f'    <a class="start-btn ghost" href="{spec["book_id"]}.pdf" download>&#128196; Download the printable PDF</a>\n'
        f'    <a class="start-btn ghost" href="../index.html">&#8592; More books</a>\n'
        f'  </div>\n'
        f'</section></div>\n'
    )


def render_book(spec: dict) -> str:
    total = len(spec["pages"]) + 2  # cover + interior pages + end screen
    head = _fill(_template("book_head.html"), ID=spec["book_id"], TITLE=amp(spec["title"]))
    tail = _fill(
        _template("book_tail.html"),
        ID=spec["book_id"],
        BOOK_TITLE=spec["book_title"],
        BADGE=spec["book_badge"],
        TOTAL=str(total),
    )
    parts = [head, '<main id="bookMain">\n', render_cover(spec)]
    parts += [render_page(spec, page) for page in spec["pages"]]
    parts.append(render_end(spec, total - 1))
    parts.append(tail)
    return "".join(parts)


def main() -> int:
    args = sys.argv[1:]
    out_dir = BOOKS_DIR
    if "--out" in args:
        i = args.index("--out")
        out_dir = Path(args[i + 1])
        del args[i : i + 2]
    out_dir.mkdir(parents=True, exist_ok=True)

    if args == ["--all"]:
        targets = sorted(SPECS_DIR.glob("*.json"))
    elif len(args) == 1:
        targets = [Path(args[0])]
    else:
        print("Usage: python render.py <specs/BookN_....json> | --all [--out <folder>]")
        return 1

    for path in targets:
        spec = json.loads(path.read_text(encoding="utf-8"))
        html = render_book(spec)
        out_path = out_dir / (path.stem + ".html")
        out_path.write_text(html, encoding="utf-8", newline="\n")
        shown = out_path.relative_to(REPO_ROOT) if out_path.is_relative_to(REPO_ROOT) else out_path
        print(f"{path.name} -> {shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
