"""The product catalog. Plain Python, not a DB table -- there's no admin
UI for adding products, and a code change + deploy is the right weight
for a solo operator with a handful of SKUs, not a content-management
system.

Prices are working assumptions sized against realistic print-on-demand
(Printify-style) small-batch costs plus shipping plus Stripe's processing
fee. Real apparel vendor quotes have been verified in APPAREL_VENDOR_QUOTES.md:
- tshirt ($20.00): confirmed viable (+16% to +38% net margin).
- onesie ($20.00): borderline viable (+6.5% standard, +21.5% premium); $22 suggested.
- hat ($18.00): sells at a loss on standard Printify (-$2.89 to -$3.63); flagged
  for owner decision to raise to $22.00-$24.00.
Non-apparel items (stickers, journal, puzzle) remain working assumptions.

Fulfillment
-----------
Every entry declares how it ships:

* ``"printify"`` -- made to order by Printify. When an address is
  submitted (POST /api/requests) the backend creates + produces a
  Printify order automatically (app/services/printify.py). Needs a
  filled-in ``"printify"`` mapping AND a configured token/shop id;
  until both exist the order simply falls back to manual handling.
* ``"manual"`` -- hand-kitted items held by a kitting 3PL (the reward box
  and the Reading Passport Kit); the operator works the admin dashboard's
  unsent list and hands addresses to the 3PL, then marks each row sent.
  No API call. The Reading Passport Kit bundles a Lulu Print API booklet
  with a Printify sticker sheet -- two separate vendors can't ship as one
  parcel automatically, so it's kitted by hand like the reward box rather
  than wired up as a second automated fulfillment path.

The ``"printify"`` mapping is a stub until a real Printify account
exists. Fill it from Printify's catalog + your uploaded artwork:

* ``blueprint_id`` / ``print_provider_id`` -- ints from the Printify
  catalog, for the exact product and print shop (see verified apparel IDs
  in APPAREL_VENDOR_QUOTES.md).
* ``image_url`` -- the print image: a public ``https`` URL (or the id of
  an image already uploaded to Printify).
* ``variant_id`` -- the single Printify variant id, for a product with
  **no** size axis (``"variants": None`` in the catalog).
* ``variants`` -- for a product **with** sizes, a map from each catalog
  size key (``PRODUCTS[...]["variants"]``) to its Printify variant id,
  e.g. ``{"YM": 12345}``; leave ``variant_id`` ``None`` in that case.

``printify_mapping_ready()`` reports whether a mapping is complete enough
to actually place an order.
"""

def _unmapped_printify() -> dict:
    """A fresh, all-placeholder Printify mapping. A factory (not a shared
    module constant) so each product owns its own nested dicts -- filling
    one in later can't leak into the others."""
    return {
        "blueprint_id": None,
        "print_provider_id": None,
        "image_url": None,
        "variant_id": None,   # a product with no size axis
        "variants": {},        # size-key -> Printify variant id, for a sized product
    }


PRODUCTS: dict[str, dict] = {
    "reward_box": {
        "name": "Little Sprout reward box",
        "description": "Poster, certificate, sticker sheet, bookmark, and button -- "
                        "for a reader who finished all 14 books.",
        "price_cents": 1000,
        "variants": None,
        # Shown on rewards.html only, reached via the badge shelf's
        # "finished all 14 books" CTA -- not listed in the general Shop.
        "shop_visible": False,
        # Hand-kitted box held by a 3PL -- never a Printify order.
        "fulfillment": "manual",
    },
    "tshirt": {
        "name": "Little Sprout T-Shirt",
        "description": "Youth tee featuring all four friends -- Maya, Marcus, Sophie, and James.",
        "price_cents": 2000,
        "variants": ["YS", "YM", "YL", "AS", "AM", "AL"],
        "shop_visible": True,
        "fulfillment": "printify",
        # Verified POD: Bella+Canvas 3001Y (blueprint 420, youth) / 3001 (blueprint 12, adult).
        # See APPAREL_VENDOR_QUOTES.md for full economics ($3.21 - $5.99 margin).
        "printify": _unmapped_printify(),
    },
    "onesie": {
        "name": "Little Sprout Baby Bodysuit",
        "description": "Soft snap-bottom bodysuit with the four friends -- for the littlest siblings.",
        "price_cents": 2000,
        "variants": ["6M", "12M", "18M", "24M"],
        "shop_visible": True,
        "fulfillment": "printify",
        # Verified POD: Rabbit Skins 4400 (blueprint 561).
        # See APPAREL_VENDOR_QUOTES.md ($1.29 margin standard / $4.30 premium).
        "printify": _unmapped_printify(),
    },
    "hat": {
        "name": "Little Sprout Cap",
        "description": "Adjustable kids' cap, embroidered with the Sprout leaf logo.",
        "price_cents": 1800,
        "variants": None,
        "shop_visible": True,
        "fulfillment": "printify",
        # Verified POD: Yupoong 6245CM (blueprint 776) / OTTO 18-253.
        # WARNING: Sells at a loss (-$2.89 to -$3.63) at $18.00 on standard Printify!
        # Recommended: raise price_cents to 2200 ($22) or 2400 ($24) upon owner sign-off.
        # See APPAREL_VENDOR_QUOTES.md.
        "printify": _unmapped_printify(),
    },
    "water_bottle": {
        "name": "Little Sprout Water Bottle",
        "description": "Reusable bottle printed with all four friends.",
        "price_cents": 1500,
        "variants": None,
        "shop_visible": True,
        "fulfillment": "printify",
        "printify": _unmapped_printify(),
    },
    "tote": {
        "name": "Little Sprout Library Bag",
        "description": "Sturdy cotton tote for hauling library books, sized for small hands.",
        "price_cents": 1500,
        "variants": None,
        "shop_visible": True,
        "fulfillment": "printify",
        "printify": _unmapped_printify(),
    },
    "sticker_sheet": {
        "name": "Little Sprout Sticker Sheet",
        "description": "A kiss-cut sheet of the four friends and reading badges.",
        "price_cents": 600,
        "variants": None,
        "shop_visible": True,
        "fulfillment": "printify",
        "printify": _unmapped_printify(),
    },
    "puzzle": {
        "name": "Little Sprout Jigsaw Puzzle",
        "description": "A friendly jigsaw of Maya, Marcus, Sophie, and James on a reading day.",
        "price_cents": 2200,
        "variants": None,
        "shop_visible": True,
        "fulfillment": "printify",
        "printify": _unmapped_printify(),
    },
    "journal": {
        "name": "My Reading Journal",
        "description": "A spiral notebook to track books read -- pairs with the reading plan on the site.",
        "price_cents": 1400,
        "variants": None,
        "shop_visible": True,
        "fulfillment": "printify",
        "printify": _unmapped_printify(),
    },
    "reading_passport_kit": {
        "name": "Little Sprout Reading Passport Kit",
        "description": "A printed, bound Reading Passport booklet -- a page for every "
                        "community-helper location in the series -- plus a sticker "
                        "sheet of all 14 badges to fill it in. The mailed keepsake "
                        "version of the free printable passport.",
        "price_cents": 1800,
        "variants": None,
        "shop_visible": True,
        # Kitted by hand from two vendors (Lulu booklet + Printify sticker
        # sheet) and shipped by a 3PL, like reward_box. See
        # READING_PASSPORT_KIT_VENDOR_QUOTES.md for the cost breakdown.
        "fulfillment": "manual",
    },
}


def get_product(product_id: str) -> dict | None:
    return PRODUCTS.get(product_id)


def shop_products() -> dict[str, dict]:
    """Everything the general Shop page lists -- excludes the reward box,
    which is only ever reached through the badge-shelf completion CTA."""
    return {k: v for k, v in PRODUCTS.items() if v.get("shop_visible")}


def known_variants(product_id: str) -> list[str] | None:
    """The allowed size/variant keys for a product, or None if it has no
    variant axis. Used to validate a submitted variant instead of storing
    whatever free text the client sent."""
    product = PRODUCTS.get(product_id)
    if not product:
        return None
    return product.get("variants")


def printify_mapping_ready(product: dict) -> bool:
    """True when the product's Printify mapping has enough real ids to
    place an order: a blueprint, a print provider, an artwork image, and
    a Printify variant id -- one per catalog size if the product has
    sizes, otherwise the single ``variant_id``."""
    mapping = product.get("printify")
    if not mapping:
        return False
    if not (mapping.get("blueprint_id") and mapping.get("print_provider_id") and mapping.get("image_url")):
        return False
    sizes = product.get("variants")
    if sizes:
        mapped = mapping.get("variants") or {}
        return all(size in mapped for size in sizes)
    return bool(mapping.get("variant_id"))
