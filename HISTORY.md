# Little Sprout Stories — history

Every session's log, **newest first**. Read on demand, not at startup. The current
snapshot is the Session Handoff at the bottom of `CLAUDE.md`.

**Adding an entry:** at the end of a session, move the old handoff here as a new entry
at the top, then overwrite the handoff. One entry per session, 5–10 lines:

```
## YYYY-MM-DD — <what, in a few words>
*<machine: Mac | PC> · <agent: Claude | Antigravity> · commits `abc1234`*
- **Changed:** what is different now, for the user and in the code.
- **Why:** the ask or the problem, and any decision made (with its reason).
- **Verified:** what was run and what it said; what was NOT checked.
- **Left open:** anything unfinished or waiting on the owner.
```

This repo is public, so private planning notes stay in the owner's vault, not here.

---

## 2026-10-29 — community center multi-variant background art import & cache bump

*PC · Antigravity*
- **Changed:** Imported `raw_art/LittleSprout_community-center_Backgrounds.zip` into `assets/backgrounds/` (`center_1.jpg` .. `center_5.jpg` and `center.jpg`). Updated `scripts/import_background_art.py` with specific zip/slug argument targeting and `--skip-existing` support. Bumped `sw.js` `CACHE_VERSION` from `littlesprout-v35` to `littlesprout-v36`. All 13 backdrop locations now have complete 5-variant coverage (78 total images).
- **Why:** The community center was the sole remaining location running on single-variant art.
- **Verified:** `python scripts/link_check.py` passed (712 local links verified, 0 broken). `python scripts/placeholder_audit.py` passed (0 placeholders). `cache_bump_guard.py` verified against `sw.js` v36 bump.
- **Left open:** Review and merge the open feature PRs (#9–#13).

## 2026-10-24 — docs restructured to the uniform standard

*Mac · Claude · docs only, no site change*
- **Changed:** `CLAUDE.md` now opens with the big picture and follows the standard seven sections, with the product's settled decisions moved in. `scripts/cache_bump_guard.py` now also skips `AGENTS.md`, `HISTORY.md` and `.claudeignore` — none are cached by the service worker, so a docs-only push no longer needs a `CACHE_VERSION` bump. The handoff now lists all five open PRs (#12 was missing). This file is new.
- **Why:** one structure across every repo — a short always-read file, and a log read only when needed.
- **Verified:** every line of the old `CLAUDE.md` checked against the new files; the guard's rule applied to this commit flags nothing (the script itself needs Python 3.10+, which this Mac lacks — its system Python is 3.9).
- **Left open:** none.

## 2026-10-17 — the state recorded in the old handoff

*From the old `CLAUDE.md`, word for word:*

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

## Before 2026-10-17

See `git log` and the merged pull requests. Earlier session notes are kept privately in the owner's vault.
