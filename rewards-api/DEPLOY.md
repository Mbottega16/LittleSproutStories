# Deploying the rewards / Shop API

The static site (repo root) needs nothing — GitHub Pages serves it. This
doc is only for `rewards-api/`, which powers the reward box, the Shop, and
the cork board. Do the steps **in order**; each unblocks the next.

Until every step is done, the site still works — the Shop and reward-box
pages just show "temporarily unavailable".

---

## 1. Stripe account  *(you; ~30–60 min, verification can take a day)*

1. Create the account at dashboard.stripe.com, verify the email.
2. Business type: **Company → LLC**. Country can't be changed later.
3. Business details: legal name, **EIN**, address, the site URL, a support
   email, a statement descriptor (e.g. `LITTLE SPROUT STORIES`).
4. Representative + any 25%+ owners: name, DOB, address, SSN last 4.
5. Bank account for payouts (a business checking account under the LLC).
6. **Activate payments.** Card payments usually work at once; full
   activation can take ~1 business day.
7. Developers → API keys. Keep the **test-mode** keys for step 4; the
   **live** secret key goes into Render only at go-live.

No Stripe Identity / no separate consent product — a completed Checkout
payment is itself FTC-approved verifiable parental consent.

## 2. A Postgres database  *(you; ~15 min)*

Render's filesystem is wiped on every deploy, so SQLite there loses every
pending address. Pick any Postgres:

- Render's own managed Postgres (simplest — provision it in the same
  dashboard), **or**
- a free tier elsewhere (Neon, Supabase).

Create the database and copy its connection URL (starts `postgres://` or
`postgresql://` — the app normalises either).

## 3. Render web service  *(you; ~20 min)*

1. New → Web Service → connect the `LittleSproutStories` repo.
2. Render reads `rewards-api/render.yaml`: root dir `rewards-api`, build
   `pip install -r requirements.txt && alembic upgrade head`, start
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, health `/api/health`.
3. Keep the service name **`littlesprout-rewards`** so the public URL is
   `https://littlesprout-rewards.onrender.com` — that's the value already
   hardcoded in `shop.html` / `rewards.html` / `board.html`.
4. Set the `sync: false` env vars in the dashboard:
   | var | value |
   |---|---|
   | `DATABASE_URL` | the Postgres URL from step 2 |
   | `STRIPE_API_KEY` | Stripe **test** secret key (for now) |
   | `STRIPE_WEBHOOK_SECRET` | from step 4 below |
   | `ADMIN_PASSWORD` | pick a real one |
   | `ADMIN_SESSION_SECRET` | `python -c "import secrets;print(secrets.token_urlsafe(32))"` |
   | `PRINTIFY_API_TOKEN` / `PRINTIFY_SHOP_ID` | from step 5 (optional for the first smoke test) |
   | `PRINTIFY_FALLBACK_EMAIL` / `PRINTIFY_FALLBACK_PHONE` | your own contact |
5. Deploy. Check `https://littlesprout-rewards.onrender.com/api/health`
   returns `{"status":"ok"}`.

## 4. Stripe webhook  *(you; ~5 min, needs the Render URL)*

1. Stripe → Developers → Webhooks → Add endpoint:
   `https://littlesprout-rewards.onrender.com/api/webhooks/stripe`
2. Events: `checkout.session.completed` (add `checkout.session.expired`).
3. Copy the **signing secret** → Render env `STRIPE_WEBHOOK_SECRET`, redeploy.

## 5. Printify  *(you; ~half a day incl. artwork)*

1. Printify → My Account → Connections → API tokens → **Generate**
   (scope `orders.write`, plus `catalog.read` while you look up ids).
   *Not* a Shopify token. Copy the token and the numeric **shop id**.
2. For each Shop product in `app/products.py`, fill its `"printify"` map:
   - `blueprint_id` + `print_provider_id` from the Printify catalog for
     the exact product + print shop (see verified apparel IDs in `APPAREL_VENDOR_QUOTES.md`:
     `tshirt` youth `420` / adult `12`, `onesie` `561`, `hat` `776` / `18-253`);
   - `image_url` — upload the artwork to Printify (or host the PNG) and
     put its URL/id here;
   - `variant_id` for a product with no sizes, **or** a `variants`
     `{size: id}` map for one with sizes (`tshirt`, `onesie`).
3. `printify_mapping_ready()` gates each product — a half-filled map just
   falls back to manual, it won't send a broken order.
4. Confirm real base cost + shipping per product against the live Printify
   quote and update `price_cents`. See `APPAREL_VENDOR_QUOTES.md` for the
   full quote breakdown:
   - `tshirt` ($20) is confirmed viable (+$3.21 profit standard, +$5.99 premium).
   - `onesie` ($20) breaks even (+$1.29 profit standard, +$4.30 premium); consider $22.
   - `hat` ($18) **sells at a loss** (-$2.89 to -$3.63 per cap standard); must be raised to $22–$24.
   - Non-apparel prices (`sticker_sheet` $6, `journal` $14, `puzzle` $22) remain unconfirmed guesses and likely sell below cost.

## 6. Point the site at the live API + smoke test  *(you + me)*

1. In `shop.html`, `rewards.html`, `board.html`: set
   `const API_BASE = 'https://littlesprout-rewards.onrender.com/api';`
   (currently a placeholder), bump `sw.js` `CACHE_VERSION`, ship.
2. With Stripe still in **test mode**, buy something with test card
   `4242 4242 4242 4242`. Confirm: webhook flips the order to paid →
   address form → `POST /api/requests` returns 201 → a Printify **draft**
   order appears (don't send test orders to production) → the reward box
   instead shows as an unsent row in the admin dashboard.
3. Flip Stripe to **live** keys in Render. Done.

## 7. Reward box (separate track)

The box is `fulfillment: "manual"` — no API. Print the components, kit a
first run (~25–50 boxes), send them to a kitting 3PL, then work the admin
dashboard's unsent list against the 3PL. See the project notes for the
$10 unit economics.

## 8. Reading Passport Kit (separate track)

Also `fulfillment: "manual"` — it bundles a Lulu Print API booklet with a
Printify sticker sheet, two vendors that can't ship as one automated parcel.
See `READING_PASSPORT_KIT_VENDOR_QUOTES.md` for the full cost breakdown
behind the $18.00 price.

1. Finalize the booklet's interior layout (page count, trim size), then
   pull a firm quote from Lulu's pricing calculator for that exact spec.
2. Order a first batch of booklets (Lulu) and sticker sheets (Printify) to
   whichever kitting 3PL already handles the reward box — get a quote for
   packing + mailing the two together before committing to a batch size.
3. Work the admin dashboard's unsent list against that 3PL, same as the
   reward box.
