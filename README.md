# LittleSprout Stories

Interactive phonics storybooks for early readers ages 4–7, plus games spanning ages 3–12.

Eighteen storybooks and twelve games starring Maya, Marcus, Sophie, and James, built on a
"Double Engine" model: every page pairs decodable phonics text with a social-emotional
learning beat.

**Live site:** https://mbottega16.github.io/LittleSproutStories/

---

## Structure

```
index.html          Home — library, games, badge shelf, Maryland resources
characters.html     Meet the Friends — all four kids, all five expressions
privacy.html        Privacy policy (no data collected)
manifest.json       PWA manifest — lets the site install to a home screen
sw.js               Service worker — offline support
assets/sprites/     87 character PNGs, shared by every page
assets/icons/       App icons for installed/home-screen use
books/              14 storybooks (~23KB each, reference assets/sprites/)
games/              12 games (ages 3-12, all reference assets/sprites/)
rewards-api/        FastAPI backend — reward box, Shop, cork board. Deploys
                    separately to Render; GitHub Pages ignores this folder.
.nojekyll           Tells GitHub Pages to serve files as-is
```

Static site — no build step, no server code, no dependencies. Plain HTML/CSS/JS.

The one exception is [`rewards-api/`](rewards-api/README.md) — a small FastAPI
backend for paid orders (the reward box and the Shop) and the community cork
board. It is **not** part of the static site: Pages serves the repo root and
ignores that folder, while the backend runs as its own Render web service from
the subdirectory (`rootDir: rewards-api`, see `rewards-api/render.yaml`). It was
previously the separate repo `EduSystems-Code/LittleSprout-Rewards`, consolidated
here on 2026-09-03.

---

## Deploying to GitHub Pages

Once pushed, go to **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.
The site is live in about a minute at the URL above.

`index.html` must stay at the repo root. All internal links are relative, so nothing
needs to change between local preview and the live site.

**Local preview** — open `index.html` directly, or for a closer match to production:
```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

---

## Smoke test (Playwright)

`scripts/smoke_playwright.mjs` opens every page in `books/` and `games/` in headless
Chromium and fails on any HTTP error, console error, uncaught exception, or blank render.
Playwright is not a repo dependency. It must be resolvable by `import 'playwright'` from this
folder (for example, installed in a parent directory). Then install the browser once:

```bash
npx playwright install chromium                                # one-time browser download
node scripts/smoke_playwright.mjs                              # test files on disk
python3 -m http.server 8000 &                                  # or test a served copy:
node scripts/smoke_playwright.mjs http://localhost:8000/
```

Exit code is 0 only when every page passes. Each run prints one `PASS`/`FAIL` line per page
plus the errors for any failure.

---

## Editing

**Site copy, layout, resources** — edit `index.html` or `characters.html` directly.

**Storybook content** — do *not* edit files in `books/`. They are generated and get
overwritten. Edit the page specs in the build pipeline instead, then rebuild. See
`build_pipeline/README.md`.

**Character art** — add processed sprites to `assets/sprites/` using the naming
convention `character_expression_pose.png`. Expressions: `happy`, `neutral`, `sad`,
`surprised`, `frustrated`. Poses: `standing`, `sitting`, `walking`, `running`, `jumping`,
`waving`, `kneeling`, `pointing`, `looking`, `reaching`, `giving`, `hands`.

Don't crop/resize/rename by hand. Drop the Canva/Gemini-exported
character-sheet zip in `raw_art/` (gitignored) and run:
```bash
python scripts/import_character_art.py
```
It crops each image to its real content, resizes, and writes correctly-named
files straight into `assets/sprites/`. See its module docstring for details.

---

## Suggested workflow

Work on a branch, not directly on `main`:

```bash
git checkout -b add-backgrounds
# make changes
git add -A
git commit -m "Add fire station background art"
git push -u origin add-backgrounds
```

Then open a Pull Request on GitHub. Pages keeps serving `main`, so the live site stays
working while you experiment. Merge when you're happy.

**Keep `main` deployable.** If it's on `main`, it's live.

---

## Features

- **Read-aloud.** Every story page has a "Read to me" button using the browser's built-in
  speech engine. Words highlight as they're spoken. No network calls, no cost, no API key.
  Hidden automatically on browsers without speech support.
- **Progress + badges.** Finishing a book saves a badge to `localStorage`. The home page
  shows a badge shelf and ticks finished books. Device-local only; nothing is transmitted.
  A "Clear saved progress" button wipes it.
- **Offline.** A service worker caches the shell on install and caches books, games, and
  sprites as they're opened, so anything read once opens again with no connection.
- **Installable.** `manifest.json` lets a parent add LittleSprout to a tablet home screen.
- **Accessibility.** Keyboard paging (arrow keys), Escape stops narration, visible focus
  rings, skip link, ARIA live regions on quiz feedback, `prefers-reduced-motion` respected,
  and an "Aa Easier to read" toggle that increases letter/word/line spacing.

### Bumping the cache after an update
`sw.js` has `CACHE_VERSION` near the top. **Change it whenever you change site files**
(e.g. `littlesprout-v1` → `littlesprout-v2`), otherwise returning visitors keep getting the
old cached copy. This is the single most common cause of "I pushed a fix but it looks the same."

## Known placeholders

These are real gaps, documented so nobody mistakes them for finished work:

- ~~Backgrounds~~ — done, refreshed 2026-09-11. Real illustrated art
  (`assets/backgrounds/`) via `scripts/import_background_art.py`. 12 of
  the 13 `backdrop-*` locations got a full 5-variant overhaul (var1 is
  what every book still points at via `<class>.jpg`; `<class>_1..5.jpg`
  are all kept, and the 6 games now each use one as a page background).
  `backdrop-center` (community center) never got a batch in this round —
  still the original single-variant art from 2026-08-24, in
  `raw_art/backgrounds/archive_v1_single-variant/`. Mr. Rodriguez's
  specific classroom (`backdrop-classroom`) stays wired to Book5's one
  page that actually features him as the on-page helper; every other
  School-related page (including Book5's other rooms and Book15's
  classroom-flavored recap) stays on `backdrop-school`'s general room.
- **Helper characters.** The eleven community helpers — Alex, Jasmine, Ms. Chen,
  Dr. Patel, Mr. Rodriguez, Mr. Smith, Keisha, Tom, Rose, David, Nurse Aisha — render as
  an emoji plus a name label in a `.helper-slot` div. The series is named after these
  characters and none of them are drawn yet.
- ~~Games still embed their art~~ — done. All six games (`games/*.html`)
  reference `assets/sprites/` directly, not embedded base64. The original
  three use the `happy` expression exclusively (they're not narrative
  scenes). Added 2026-09-11: **Feelings Faces** (ages 3–5, name-the-
  feeling, uses all five expressions), **Rhyme Time** (ages 5–7, rhyme
  awareness), and **Sentence Builder** (ages 6–9, word-order practice) —
  all three use only existing `assets/sprites/` art, no new art needed.

---

## Series note

Book 13 was scrapped during development. The series runs 1–12 and 14–19 — eighteen books (16–19 are the classic-story adaptations).
Numbering was left as-is rather than resequencing.
