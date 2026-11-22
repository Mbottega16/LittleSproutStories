# build_pipeline

How `books/*.html` gets edited. The rule: **never hand-edit files in
`books/`**. They are generated output. Edit a page spec (or a template), then
rebuild.

## What is in here

| Path | Role |
|---|---|
| `specs/<Book>.json` | The content of one book: cover, 12 pages, quizzes, the "For Grown-Ups" panel. |
| `templates/book_head.html` | Everything before `<main>`: meta tags, all the CSS, the header. Shared by all 18 books. |
| `templates/book_tail.html` | Everything after `</main>`: the nav row and all the JavaScript. Shared by all 18 books. |
| `render.py` | Builds one book from its spec and the two templates. |
| `build.py` | The command you run. It calls `render.py`. |
| `extract_spec.py` | Goes the other way: copies a published book back into its spec. |
| `generate_story.py` | Drafts a new story spec (old sprite-scene format; see the note at the end). |

`scripts/pipeline_roundtrip.py` checks that `books/` equals what the specs
render. CI runs it on every push and pull request.

## History

- 2026-08-23: the pipeline was first built from the 14 books that existed.
- Later, the "watercolor" rebuild (one illustration per page, 12 pages, new
  text, SEO tags) was written straight into `books/*.html`. The specs and
  `render.py` were not updated.
  Running `build.py` would have replaced the live books with an old version.
- 2026-11-22: `extract_spec.py` and `render.py` were rewritten for the
  current template. All 18 specs were rebuilt from the live books. Output is
  byte-identical to `books/` again, and the round-trip check guards it.

## How a book is structured

Every book has a cover, 12 interior pages and an end screen.

- **Cover:** `h1_html` (raw HTML, may hold `<br>` and `&amp;`), `subtitle`,
  and `image` (a file in `assets/`, for example `book1-cover.webp`).
- **Each page:** `index`, `image` (for example `book1-page3.webp`), `text_a`,
  `text_b`, and an optional `quiz`.
  - `text_a` is the full story text. An adult or the read-aloud voice reads it.
  - `text_b` is the short practice line for the child to sound out. It must
    follow the rules in `10_Decodable_Word_List.md` and
    `GUIDANCE_DECODABILITY_VS_STORY_FLOW.md`.
  - `quiz` has a `question`, an `options` list and the `answer` index.
  - `alt` is optional. The default is "Illustration for page N of <title>".
- **End screen:** the badge, and the "For Grown-Ups" fields: `feeling`, `ask`,
  `try_this`, `words_to_grow`, `bigger_picture`, `standards`.
- **Written by the analyzer:** `reading_level` (1 to 4) and
  `end_screen.practice_words`. Run `python scripts/analyze_decodability.py --write`.
  The renderer shows them as the level tag on the cover and the "Practice these
  words" line on the end screen.

Titles are stored as plain text (`Maya & Marcus ...`). The renderer escapes
the `&` where HTML needs it.

See any file in `specs/` for the exact shape. They are real, not samples.

## Commands

```bash
# Rebuild every book from its spec
python build_pipeline/build.py

# Rebuild one book
python build_pipeline/build.py Book1_Maya_Marcus_FireStation

# Render into another folder and leave books/ alone
python build_pipeline/render.py --all --out /tmp/scratch_books

# Check that books/ equals what the specs render (never writes)
python scripts/pipeline_roundtrip.py

# Copy the published books back into the specs
python build_pipeline/extract_spec.py --all
```

Use `extract_spec.py --all` only when a book was edited by hand and the specs
must catch up. It copies the hand edit into the spec as it is.

## Editing a book

1. Open `build_pipeline/specs/<BookName>.json`.
2. Change the field you need: a `text_a` line, a quiz answer, an `image`.
3. If you changed a `text_b` line, run `python scripts/analyze_decodability.py`.
   It lists words that are not in the approved word list.
   Run it with `--write` to refresh the reading level and practice words.
4. Run `python build_pipeline/build.py <BookName>`.
5. Bump `CACHE_VERSION` in `sw.js`. `scripts/cache_bump_guard.py` blocks the
   push if you forget.
6. Commit the spec and the rebuilt `books/*.html` together.

To change the look or the behaviour of all books at once, edit the two files
in `templates/`, then rebuild.

## Adding a new book

There is no scaffold command. Copy an existing spec, write the new content,
add the book's illustration files to `assets/`, add a card to `index.html`
(this pipeline does not do that), then run `build.py <NewBookName>`.

## What this pipeline does not do

- It does not make the illustrations. The `image` files must already exist in
  `assets/`. A wrong name renders a broken image until someone looks at the page.
- It does not make the printable PDFs (`books/*.pdf`).
- It does not touch `games/`, `index.html`, `stats.html`, `manifest.json` or
  `sw.js`.
- `generate_story.py` still writes the old sprite-scene spec format (a `stage`
  with sprites for each page). That format no longer renders. Use it for
  story drafting only, and move the text into a current-format spec by hand.
