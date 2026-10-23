# Little Sprout Stories — Project Rules, Architecture & Session Handoff

Interactive phonics storybooks (ages 4–7) and educational mini-games (ages 3–12) for early readers, plus a Maryland family resources hub and COPPA-compliant physical rewards/merch backend.
- **Repo:** `~/OneDrive/Desktop/LittleSprouts` (`Mbottega16/LittleSproutStories`, public)
- **Live Site:** https://mbottega16.github.io/LittleSproutStories/ (GitHub Pages deploys straight from `main`)
- **Vault Context & History:** `~/OneDrive/Desktop/AI Projects/my-brain/projects/little-sprout-stories/context.md` (and `history.md` for older session logs)

---

## Never Read / Noise Zones (Do Not Scan)

To keep context clean and avoid scanning thousands of vendor/binary files, **never read or grep inside**:
- `rewards-api/.venv/` — 7,580+ Python virtual environment files.
- `raw_art/` — 389 MB of unprocessed character/background source zips and PSD/PNG sheets.
- `assets/audio/`, `assets/sprites/`, `assets/backgrounds/`, `assets/resource-photos/` — binary media assets (use `scripts/` to inspect or import art).
- `books/*.html` — **generated output** from `build_pipeline/specs/*.json`. Do not hand-edit or read all 18 generated HTML books to understand template structure; read `build_pipeline/render.py` and one spec in `build_pipeline/specs/` instead.
- `data/*.db` — local SQLite working database.

---

## Architecture & Root File Map

The frontend is **zero-dependency vanilla HTML5/CSS3/ES6 JS** (no bundler, no `package.json`, no npm runtime) with a PWA service worker (`sw.js` + `manifest.json`).

### Core Directories
| Path | Role |
|---|---|
| `build_pipeline/` | **Authoritative book generator.** Edit `build_pipeline/specs/<Book>.json` or `build_pipeline/render.py`, then run `python build_pipeline/build.py` to regenerate `books/*.html`. `extract_spec.py` recovers JSON from HTML; `generate_story.py` generates stories + Piper TTS audio. |
| `books/` | 18 generated storybooks (`Book1`–`Book12`, `Book14`–`Book19`; Book 13 was scrapped intentionally — never renumber). |
| `games/` | Standalone HTML5/JS mini-games (`feelings_faces.html`, `pose_parade.html`, `rhyme_time.html`, `sentence_builder.html`, `sound_it_out.html`, `whos_missing.html`) sharing sprites and `localStorage` star progress. |
| `rewards-api/` | Standalone FastAPI + SQLAlchemy + Stripe + Printify backend for the $10 physical reward box, merch shop, and community cork-board moderation. Deployed separately on Render (`render.yaml`, `rootDir: rewards-api`). |
| `scripts/` | Verification, art import, and build guards (`link_check.py`, `cache_bump_guard.py`, `placeholder_audit.py`, `generate_sitemap.py`, `import_character_art.py`, `import_background_art.py`). |

### Root HTML Pages (13 Active Entry Points — Not Loose Scratch Files)
- **Reader & Family Pages:** `index.html` (main catalog, badge shelf, 5-stage reading plan), `characters.html` ("Meet the Friends": Maya, Marcus, Sophie, James), `reading-passport.html` (printable 14-location passport), `book-nook.html` & `book-nook-bookplate.html` (book donation hub & printable bookplates).
- **Maryland & Educator Pages:** `resources.html` (Maryland Family Resources Hub — 24 vetted orgs across 7 domains), `grants.html` (Maryland ECE grants & scholarships), `stats.html` (Common Core RL/SL crosswalk, 4-tier phonics levels), `board.html` (moderated community cork board).
- **Commerce, Legal & Admin:** `rewards.html` ($10 Stripe Checkout reward box), `shop.html` (Printify merch shop), `privacy.html` (COPPA-compliant policy: client-side `localStorage` only, 90-day address auto-purge), `admin.html` (cookie-gated moderation & order fulfillment dashboard).

---

## Hard Constraints & Domain Rules

1. **"If it's on `main`, it's live."** GitHub Pages deploys directly from `main`. Non-trivial feature work goes on a feature branch + PR unless the user asks to land on `main`.
2. **Never hand-edit `books/*.html`.** Always edit the JSON spec in `build_pipeline/specs/` or the template in `build_pipeline/render.py`, then run `python build_pipeline/build.py`.
3. **Bump `CACHE_VERSION` in `sw.js` when changing site assets.** `.git/hooks/pre-push` runs `scripts/cache_bump_guard.py` and `scripts/link_check.py` and will block pushes if cached files changed without bumping `CACHE_VERSION`.
4. **COPPA & Zero Passive Tracking.** All child reading progress, stars, and badges stay strictly in browser `localStorage`. No third-party analytics or tracking pixels on kid-facing pages. Physical mailing addresses in `rewards-api` are collected only via Stripe Checkout (payment-as-parental-consent) and auto-purged after 90 days.
5. **Double Engine Pedagogy.** Every book pairs decodable phonics text with a social-emotional learning (SEL) beat and a book-specific "For Grown-Ups" panel at the end. Keep SEL fields (`feeling`, `ask`, `try_this`) separate from factual comprehension games.

---

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

---

## Session Handoff (Last Worked On · Current State · Next Up)

- **Last Worked On:**
  - Merged PR #8 (`9e3a3c9`): community cork-board moderation + `admin.html` dashboard, SEO cards (`8ea8df1`), and Maryland resource card photos (`12ea472`).
  - Added Books 16–19 (classic fable adaptations: *Tortoise and the Hare*, *Lion and the Mouse*, *Boy Who Cried Wolf*, *Ant and the Grasshopper*) and staged community center background pack into `raw_art/`.
  - Prepared 4 open feature branches/PRs: PR #9 (`visitor-flow-and-nav`), PR #10 (`phonics-scope-and-sequence`), PR #11 (`games-for-older-kids`: Word Dash & Helper Detective), and PR #13 (`shop-coming-soon`).
- **Current State (2026-10-17):**
  - `main` is live with 18 books, 6 games, Maryland Family Resources Hub, and consolidated `rewards-api/`.
  - `rewards-api` is code-complete and tested; live Render + Stripe deployment waits on user go-ahead.
- **What Needs To Be Worked On Next:**
  1. Review and merge the 4 open feature PRs (#9, #10, #11, #13) in sequence, resolving shared `index.html` / `sw.js` `CACHE_VERSION` conflicts on each merge.
  2. Run `python scripts/import_background_art.py` on the community center background pack in `raw_art/` if new location scenes are scheduled.
  3. Deploy `rewards-api/` to Render + connect live Stripe keys only when the owner gives the explicit spend/publish sign-off.
