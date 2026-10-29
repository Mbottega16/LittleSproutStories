# Little Sprout Stories — rules & map (read this first)

Interactive phonics storybooks (ages 4–7) and educational mini-games (ages 3–12) for early readers, plus a Maryland family resources hub and COPPA-compliant physical rewards/merch backend.

**History:** [`HISTORY.md`](HISTORY.md), newest first — read it when a task touches past work.
**Business side:** the owner's my-brain vault, `projects/little-sprout-stories/context.md`.
- **Repo:** PC `~/OneDrive/Desktop/LittleSprouts`, Mac `projects/little-sprout-stories/app` in the vault (`Mbottega16/LittleSproutStories`, **public**)
- **Live Site:** https://mbottega16.github.io/LittleSproutStories/ (GitHub Pages deploys straight from `main`)

## What this is
- **What:** fourteen-plus phonics storybooks starring four recurring kids (Maya, Marcus,
  Sophie, James) and six games, built on a **"Double Engine"** model: every page pairs
  decodable phonics text with a social-emotional-learning beat. Read-aloud with word
  highlighting, badges and progress, offline support, installable as a PWA.
- **For:** early readers ages 4–7 (games up to 12), handed a home or classroom tablet by a
  parent or teacher — which is why progress stays on the device and nothing is transmitted.
- **Platform:** a static site — plain HTML/CSS/JS, no build step for the site, no server, no
  dependencies. The separate `rewards-api/` backend (reward box, shop, cork board) is
  code-complete but not deployed.
- **What "done" looks like:** books and games a young child can use alone, safely, with the
  family pages around them; the rewards backend live only after the owner signs off.

## Settled decisions (don't re-argue)

1. **"If it's on `main`, it's live."** GitHub Pages deploys directly from `main`. Non-trivial feature work goes on a feature branch + PR unless the user asks to land on `main`.
2. **Never hand-edit `books/*.html`.** Always edit the JSON spec in `build_pipeline/specs/` or the template in `build_pipeline/render.py`, then run `python build_pipeline/build.py`.
3. **COPPA & Zero Passive Tracking.** All child reading progress, stars, and badges stay strictly in browser `localStorage`. No third-party analytics or tracking pixels on kid-facing pages. Physical mailing addresses in `rewards-api` are collected only via Stripe Checkout (payment-as-parental-consent) and auto-purged after 90 days.
4. **Double Engine Pedagogy.** Every book pairs decodable phonics text with a social-emotional learning (SEL) beat and a book-specific "For Grown-Ups" panel at the end. Keep SEL fields (`feeling`, `ask`, `try_this`) separate from factual comprehension games.
5. **No failure states for kids:** games use non-punitive streaks, not timers or losses.
6. **Plain HTML/CSS/JS only** — any new feature (flashcards, an OER library) follows the
   site's no-build-step, no-dependency convention, not React.
7. **Book 13 was scrapped intentionally — never renumber the books.**
8. **The rewards backend lives here** (`rewards-api/`, consolidated 2026-09-03); the old
   `LittleSprout-Rewards` repo is archived. No secrets were ever committed.

## How it's built

The frontend is **zero-dependency vanilla HTML5/CSS3/ES6 JS** (no bundler, no `package.json`, no npm runtime) with a PWA service worker (`sw.js` + `manifest.json`).

| Path | Role |
|---|---|
| `build_pipeline/` | **Authoritative book generator.** Edit `build_pipeline/specs/<Book>.json` or `build_pipeline/render.py`, then run `python build_pipeline/build.py` to regenerate `books/*.html`. `extract_spec.py` recovers JSON from HTML; `generate_story.py` generates stories + Piper TTS audio. |
| `books/` | 18 generated storybooks (`Book1`–`Book12`, `Book14`–`Book19`; Book 13 was scrapped intentionally — never renumber). |
| `games/` | Standalone HTML5/JS mini-games (`feelings_faces.html`, `pose_parade.html`, `rhyme_time.html`, `sentence_builder.html`, `sound_it_out.html`, `whos_missing.html`) sharing sprites and `localStorage` star progress. |
| `rewards-api/` | Standalone FastAPI + SQLAlchemy + Stripe + Printify backend for the $10 physical reward box, merch shop, and community cork-board moderation. Deployed separately on Render (`render.yaml`, `rootDir: rewards-api`). |
| `scripts/` | Verification, art import, and build guards (`link_check.py`, `cache_bump_guard.py`, `placeholder_audit.py`, `generate_sitemap.py`, `import_character_art.py`, `import_background_art.py`). |

**Root HTML pages (13 active entry points — not loose scratch files)**
- **Reader & Family Pages:** `index.html` (main catalog, badge shelf, 5-stage reading plan), `characters.html` ("Meet the Friends": Maya, Marcus, Sophie, James), `reading-passport.html` (printable 14-location passport), `book-nook.html` & `book-nook-bookplate.html` (book donation hub & printable bookplates).
- **Maryland & Educator Pages:** `resources.html` (Maryland Family Resources Hub — 24 vetted orgs across 7 domains), `grants.html` (Maryland ECE grants & scholarships), `stats.html` (Common Core RL/SL crosswalk, 4-tier phonics levels), `board.html` (moderated community cork board).
- **Commerce, Legal & Admin:** `rewards.html` ($10 Stripe Checkout reward box), `shop.html` (Printify merch shop), `privacy.html` (COPPA-compliant policy: client-side `localStorage` only, 90-day address auto-purge), `admin.html` (cookie-gated moderation & order fulfillment dashboard).

## Commands & Verification

```powershell
# Local static preview
python -m http.server 8000

# Rebuild all books (or pass a single spec name)
python build_pipeline/build.py

# Pre-push verification checks (run before committing/pushing)
python scripts/link_check.py
python scripts/cache_bump_guard.py
python scripts/placeholder_audit.py

# Backend (rewards-api) test suite
rewards-api\.venv\Scripts\pytest rewards-api/tests -q
```

On the Mac use `python3`, and `rewards-api/.venv/bin/pytest` if that venv exists.

## Never Read / Noise Zones (Do Not Scan)

To keep context clean and avoid scanning thousands of vendor/binary files, **never read or grep inside**:
- `rewards-api/.venv/` — 7,580+ Python virtual environment files.
- `raw_art/` — 389 MB of unprocessed character/background source zips and PSD/PNG sheets.
- `assets/audio/`, `assets/sprites/`, `assets/backgrounds/`, `assets/resource-photos/` — binary media assets (use `scripts/` to inspect or import art).
- `books/*.html` — **generated output** from `build_pipeline/specs/*.json`. Do not hand-edit or read all 18 generated HTML books to understand template structure; read `build_pipeline/render.py` and one spec in `build_pipeline/specs/` instead.
- `data/*.db` — local SQLite working database.

## Rules & Gotchas

- **Bump `CACHE_VERSION` in `sw.js` when changing site assets.** `.git/hooks/pre-push` (on the PC) runs `scripts/cache_bump_guard.py` and `scripts/link_check.py` and will block pushes if cached files changed without bumping `CACHE_VERSION`. The agent docs (`CLAUDE.md`, `AGENTS.md`, `HISTORY.md`, `.claudeignore`) are not cached and don't need a bump.
- **Several open PRs branch independently off `main`** and overlap in `index.html` and
  `sw.js` `CACHE_VERSION` — expect to resolve those on each merge.
- **Games for older kids use only the factual helper layer** from the specs, never the
  `feeling`/SEL fields.
- **Nothing that costs money or goes live** (Render deploy, live Stripe keys) without the
  owner's explicit sign-off.
- **This repo is public:** keep private business notes in the owner's vault, not here.

## Session Handoff (Last Worked On · Current State · Next Up)

*Overwrite this at the end of every session; move the previous handoff into `HISTORY.md` first.*

- **Last Worked On (2026-10-29):** imported community center background pack (`raw_art/LittleSprout_community-center_Backgrounds.zip`) into `assets/backgrounds/` (`center_1.jpg` .. `center_5.jpg` and `center.jpg`), completing full 5-variant coverage across all 13 locations (78 images total). Upgraded `scripts/import_background_art.py` with single-target zip/slug argument and `--skip-existing` support. Bumped `sw.js` `CACHE_VERSION` to `littlesprout-v36`.
- **Current State (2026-10-29):** `main` is live with 18 books, 6 games, all 13 background locations with 5 variants each, zero placeholder assets, and 0 broken links across 712 verified local links. Open PRs: #9, #10, #11, #12, #13.
- **Next Up:**
  1. Review and merge the open feature PRs (#9–#13) one at a time, resolving shared `index.html` / `sw.js` `CACHE_VERSION` conflicts on each merge.
  2. Deploy `rewards-api/` to Render + connect live Stripe keys only when the owner gives explicit spend/publish sign-off.
