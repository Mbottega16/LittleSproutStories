# LittleSprout Stories

Interactive phonics storybooks and feelings games for early readers, ages 4–7.

Fourteen storybooks and three games starring Maya, Marcus, Sophie, and James, built on a
"Double Engine" model: every page pairs decodable phonics text with a social-emotional
learning beat.

**Live site:** https://YOUR-USERNAME.github.io/LittleSproutStories/

---

## Structure

```
index.html          Home — library, games, how-it-works, Maryland resources
characters.html     Meet the Friends — all four kids, all five expressions
assets/sprites/     87 character PNGs, shared by every page
books/              14 storybooks (~12KB each, reference assets/sprites/)
games/              3 games (currently self-contained w/ embedded art)
.nojekyll           Tells GitHub Pages to serve files as-is
```

Static site — no build step, no server code, no dependencies. Plain HTML/CSS/JS.

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

## Editing

**Site copy, layout, resources** — edit `index.html` or `characters.html` directly.

**Storybook content** — do *not* edit files in `books/`. They are generated and get
overwritten. Edit the page specs in the build pipeline instead, then rebuild. See
`build_pipeline/README.md`.

**Character art** — add processed sprites to `assets/sprites/` using the naming
convention `character_expression_pose.png`. Expressions: `happy`, `neutral`, `sad`,
`surprised`, `frustrated`. Poses: `standing`, `sitting`, `walking`, `running`, `jumping`,
`waving`, `kneeling`, `pointing`, `looking`, `reaching`, `giving`, `hands`.

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

## Known placeholders

These are real gaps, documented so nobody mistakes them for finished work:

- **Backgrounds.** Every book uses a CSS gradient backdrop, marked `BACKGROUND-SWAP` in
  the source. Right now a fire station and a bakery differ only by color. Eleven
  locations need exterior + interior art.
- **Helper characters.** The eleven community helpers — Alex, Jasmine, Ms. Chen,
  Dr. Patel, Mr. Rodriguez, Mr. Smith, Keisha, Tom, Rose, David, Nurse Aisha — render as
  an emoji plus a name label in a `.helper-slot` div. The series is named after these
  characters and none of them are drawn yet.
- **Hero image.** `HERO-ART-SWAP` in `index.html` marks where the banner photo goes.
- **No privacy policy.** Needed before any public launch, given the under-13 audience.
- **Games still embed their art** as base64 (~3.6MB total). Fine for now; worth
  converting to `assets/sprites/` references if they get edited often.

---

## Series note

Book 13 was scrapped during development. The series runs 1–12, 14, 15 — fourteen books.
Numbering was left as-is rather than resequencing.
