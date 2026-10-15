# Reading Passport Kit -- Vendor Quotes & Pricing Confirmation

This document checks real print-on-demand vendor pricing for the **physical Reading
Passport Kit** (`reading_passport_kit` in `rewards-api/app/products.py`) against its
`$18.00` shop price, the same way `APPAREL_VENDOR_QUOTES.md` checked the apparel line.

The free printable at `reading-passport.html` is a fold-and-staple booklet the parent
prints and cuts at home. The kit is the mailed, already-bound version of that same
booklet, plus a sticker sheet of the 14 badges so a reader can stick a badge in
instead of drawing one.

---

## 1. Why this is two vendors, not one

Printify -- the vendor already integrated for every other Shop item -- only lets a
buyer customize a notebook's **cover**; the interior pages are fixed, blank
lined/dotted/plain stock. It has no product that prints custom content (a how-to
page, 14 different stamp pages, a back cover) on the inside of a booklet. A real
multi-page custom interior needs a book/booklet printer instead:

- **Lulu Print API** (`print-api.lulu.com`) -- print-on-demand booklets and books,
  no minimum order (including a single copy), with its own dropship API. Supports
  saddle-stitch (staple) binding, which is the same binding the free printable
  already tells parents to use by hand.
- Printify remains the right vendor for the **sticker sheet** -- kiss-cut stickers
  are already a Printify product class (the unmapped `sticker_sheet` catalog item
  uses it too).

Because the booklet and the sticker sheet come from two different vendors, they
can't be combined into one Printify order and auto-shipped the way `tshirt` or
`hat` are. That's why `reading_passport_kit.fulfillment` is `"manual"`, matching
`reward_box`: the operator orders both components ahead of time, a kitting 3PL
packs booklet + sticker sheet into one mailer, and the admin dashboard's unsent-list
workflow (already built for the reward box) handles the rest. No new fulfillment
code is needed.

---

## 2. Booklet cost -- Lulu Print API

Lulu publishes starting prices by trim size, binding, and paper on its own pricing
calculator (`lulu.com/pricing`) rather than a flat catalog price, so the figure below
is Lulu's own published **starting** price for the closest match, not a quote for
this exact page count -- confirm the exact per-unit price on the calculator (trim
size, page count, interior color, 80# paper, saddle stitch) before the first batch
order, same caveat the apparel doc raises for its own base-cost ranges.

| Spec | Value |
|---|---|
| Trim size | Digest / Half Letter (5.5" x 8.5") -- a comfortable kid-booklet size, smaller than the free printable's full-page home version |
| Binding | Saddle stitch (staple), matching the free printable's own fold-and-staple instructions |
| Interior | Full color, 80# paper |
| Lulu starting price (this spec) | **$4.30** |
| Lulu flat fulfillment fee (per order) | **$1.75** |
| US domestic shipping (Mail/Ground, single lightweight item) | **$3.99 - $5.75** (Lulu's own published range; a single-book example came in at $5.75 via Priority, cheaper Mail-class service is usually $3.99-$4.50) |

**Booklet landed cost: $4.30 + $1.75 + ~$4.25 shipping (mid-range) = ~$10.30.**

Lulu's Print API can dropship directly to the end customer on its own -- it doesn't
strictly need manual kitting. The kit stays `"manual"` here only because it's
bundled with the sticker sheet, not because Lulu requires it.

---

## 3. Sticker sheet cost -- Printify (kiss-cut)

| Spec | Value |
|---|---|
| Product | Kiss-cut sticker sheet, 14 badge icons (reuses the badge-shelf art) |
| Printify published price range | **$1.21 - $2.69** per sheet (SKU-dependent) |
| Used for this estimate | **$2.00** (mid-upper range, conservative) |

This is the same product class as the catalog's existing unmapped `sticker_sheet`
item -- no new Printify blueprint research needed once that item is mapped.

---

## 4. Kitting & unit economics

| Line item | Cost |
|---|---|
| Booklet (Lulu, landed) | $10.30 |
| Sticker sheet (Printify, landed) | $2.00 |
| Poly mailer / kitting materials | ~$0.35 (typical small flat mailer) |
| **Total fulfillment cost** | **~$12.65** |
| Stripe fee at $18.00 (2.9% + $0.30) | $0.82 |
| Net revenue at $18.00 | $17.18 |
| **Net margin** | **+$4.53 (25.2%)** |

**Status: LIKELY VIABLE.** $18.00 clears a healthy margin even using the
conservative (higher) end of both the Lulu shipping range and the Printify sticker
range. It sits between `journal` ($14.00) and `puzzle` ($22.00) in the existing Shop
lineup, which fits a bound, mailed keepsake positioned above a generic notebook.

This isn't a fully verified quote the way the apparel figures are (those came from
confirmed Printify/Printful blueprint-specific pricing). The two real gaps before a
first batch order:

1. **Exact Lulu price for the real page count and trim size**, pulled from Lulu's
   live pricing calculator once the final interior layout (how many pages: a how-to
   page, one stamp page per location vs. a grid, a back cover) is set.
2. **3PL kitting/handling fee** for packing the booklet + sticker sheet together and
   mailing -- no figure for this exists in the repo (`reward_box`'s own 3PL fee
   isn't tracked here either); get a quote from whichever 3PL already handles the
   reward box before committing to a first run.

Even a few extra dollars of kitting fee still leaves room before $18.00 turns
unprofitable, given the $4.53 buffer above -- but it should be confirmed, not assumed.

---

## 5. Recommended owner decisions

1. **Approve the $18.00 price** (`reading_passport_kit.price_cents = 1800`) based on
   the estimate above, or hold for a firm Lulu calculator quote first.
2. **Reuse the reward box's kitting 3PL** (or get a one-off quote) for packing and
   shipping this kit, rather than standing up a second 3PL relationship.
3. **Finalize the booklet's interior layout** (page count/trim size) so a real Lulu
   quote can be pulled -- this doc used Lulu's published starting price, not a
   quote for a specific finished file.

---

## Sources consulted

- [Printify: Custom notebooks & journals](https://printify.com/custom-notebooks/) -- cover-only customization, confirms no custom interior option.
- [Lulu: Custom Booklets Printed On Demand](https://www.lulu.com/create/booklets)
- [Lulu Print API: Custom Book Sizes & Book Binding Options](https://www.lulu.com/print-api/products)
- [Lulu blog: Booklet Printing With Lulu](https://blog.lulu.com/booklet-printing/)
- [Lulu: Are there fees to use Lulu's Print API?](https://help.api.lulu.com/en/support/solutions/articles/64000254631-are-there-fees-to-use-lulu-s-print-api-)
- [Lulu: Shipping: The Basics](https://help.lulu.com/en/support/solutions/articles/64000255307-shipping-the-basics)
- [podvector.ai: Lulu Print-on-Demand Pricing](https://podvector.ai/articles/print-on-demand/costs-and-suppliers/lulu-print-on-demand-pricing)
- [Printify: Make Your Own Stickers from $1.34](https://merch.printify.com/make-your-own-stickers/)
- [apparelhub.ai: Best Print on Demand Supplier for Stickers in 2026](https://apparelhub.ai/blog/best-print-on-demand-supplier-for-stickers)
