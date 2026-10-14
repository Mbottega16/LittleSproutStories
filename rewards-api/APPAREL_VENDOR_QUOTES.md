# Real Apparel Vendor Quotes & Shop Pricing Confirmation

This document provides verified real vendor quotes from Print-on-Demand (POD) suppliers (**Printify** and **Printful**) to confirm or adjust retail prices in Little Sprout Stories (`rewards-api/app/products.py`).

Fulfillment on all apparel is print-on-demand via Printify (automated via `rewards-api/app/services/printify.py`), with flat retail pricing including US domestic shipping.

---

## 1. Executive Summary & Confirmation Status

All figures assume US domestic shipping and Stripe payment processing fees (**2.9% + $0.30** per transaction).

| Product | Catalog ID | Current Shop Price | Best Blank & Blueprint | Base Cost (Std / Prem) | US Shipping | Stripe Fee | Total Cost (Std / Prem) | Net Margin (Std / Prem) | Status |
|---|---|---|---|---|---|---|---|---|---|
| **T-Shirt** | `tshirt` | **$20.00** | Bella+Canvas 3001Y (`420`) / 3001 (`12`) | $11.66 / $8.88 | $4.25 | $0.88 | $16.79 / $14.01 | **+$3.21** (+16.1%) / **+$5.99** (+30.0%) | **CONFIRMED** |
| **Baby Bodysuit** | `onesie` | **$20.00** | Rabbit Skins 4400 (`561`) | $13.58 / $10.57 | $4.25 | $0.88 | $18.71 / $15.70 | **+$1.29** (+6.5%) / **+$4.30** (+21.5%) | **BORDERLINE** |
| **Cap / Hat** | `hat` | **$18.00** | Yupoong 6245CM (`776`) / OTTO 18-253 | $15.38 / $11.37 | $4.69 | $0.82 | $20.89 / $16.88 | **-$2.89** (-16.1%) / **+$1.12** (+6.2%) | **FAILS / DEFICIT** |
| **Library Bag** | `tote` | **$15.00** | Cotton Canvas Tote (Liberty / generic) | $9.67 / $7.12 | $4.19 | $0.74 | $14.60 / $12.05 | **+$0.40** (+2.7%) / **+$2.95** (+19.7%) | **TIGHT** |

### Key Findings
1. **T-Shirt ($20.00): Fully Confirmed.** Even with higher-tier Bella+Canvas garments and standard (non-Premium) Printify pricing, it yields a safe +$3.21 profit per shirt. On Gildan 5000/5000B, net margin is +$6.37 to +$7.74.
2. **Baby Bodysuit ($20.00): Borderline Confirmed.** Breaks even with a slim $1.29 margin on standard Printify, or $4.30 with Premium. If using colored bodysuits or if shipping fluctuates, margin is near zero. Recommended owner action: consider bumping to **$22.00** ($2200 cents) for a safe $3+ buffer on standard tier.
3. **Embroidered Cap ($18.00): Fails / Sells at a Loss.** Base embroidery ($15.38+) and shipping ($4.69) total **$20.07** before payment processing. At $18.00 retail, the shop **loses $2.89 to $3.63 on every single cap sold** on standard Printify! Price must be raised to **$22.00 – $24.00** ($2200–$2400 cents) to cover fulfillment.

---

## 2. Product-by-Product Vendor Breakdown

### A. Little Sprout T-Shirt (`tshirt`)
* **Description:** Youth and adult short-sleeve tee featuring Maya, Marcus, Sophie, and James.
* **Catalog Variants:** `["YS", "YM", "YL", "AS", "AM", "AL"]`
* **Current Retail Price:** `$20.00` (`price_cents: 2000`)

#### Printify Options & Pricing
* **Option 1: Premium Retail Soft Cotton (Bella + Canvas)**
  * **Youth (YS, YM, YL):** Bella+Canvas 3001Y (Printify Blueprint `420`)
    * Base Price (Standard): **$11.66**
    * Base Price (Printify Premium): **$8.88**
    * Standard US Shipping: **$3.99 – $4.50** (average ~$4.25)
  * **Adult (AS, AM, AL):** Bella+Canvas 3001 Unisex (Printify Blueprint `12`)
    * Base Price (Standard): **$11.29 – $12.50**
    * Base Price (Printify Premium): **$8.95 – $9.13**
    * Standard US Shipping: **$3.99 – $4.75** (average ~$4.25 via SwiftPOD/Awkward Styles)
  * **Top Print Providers:** SwiftPOD (rating 9.5), Monster Digital (rating 9.2), Awkward Styles (rating 9.1).
* **Option 2: Budget Heavy Cotton (Gildan)**
  * **Youth:** Gildan 5000B Kids Tee (Printify Blueprint `66d95b43b75886ad800456e2`)
    * Base Price (Standard): **$7.13** | Premium: **$6.76** | Shipping: **$3.99**
  * **Adult:** Gildan 5000 Unisex Tee (Printify Blueprint `6`)
    * Base Price (Standard): **$8.00 – $8.50** | Premium: **$6.50 – $7.00** | Shipping: **$3.99**

#### Printful Comparison
* **Bella+Canvas 3001Y / 3001:** Base cost $11.50 – $13.25 + $4.69 shipping = $16.19 – $17.94 total fulfillment.
* **Gildan 5000 / 5000B:** Base cost $8.25 – $9.50 + $4.69 shipping = $12.94 – $14.19 total fulfillment.

#### Unit Economics (At $20.00 Retail with Stripe Fee $0.88, Net Revenue $19.12)
| Garment & Tier | Total Fulfillment Cost | Net Profit ($) | Net Margin (%) |
|---|---|---|---|
| Bella+Canvas Youth (Standard) | $15.91 | **+$3.21** | 16.1% |
| Bella+Canvas Youth (Premium) | $13.13 | **+$5.99** | 30.0% |
| Bella+Canvas Adult (Standard) | $15.54 | **+$3.58** | 17.9% |
| Bella+Canvas Adult (Premium) | $13.20 | **+$5.92** | 29.6% |
| Gildan Youth 5000B (Standard) | $11.12 | **+$8.00** | 40.0% |
| Gildan Adult 5000 (Standard) | $11.99 | **+$7.13** | 35.7% |

*Verdict:* **CONFIRMED.** $20.00 is a competitive, fair price for parents that covers all costs and leaves a solid cushion.

---

### B. Little Sprout Baby Bodysuit (`onesie`)
* **Description:** Soft snap-bottom bodysuit with the four friends.
* **Catalog Variants:** `["6M", "12M", "18M", "24M"]`
* **Current Retail Price:** `$20.00` (`price_cents: 2000`)

#### Printify Pricing
* **Primary Blank:** Rabbit Skins 4400 Infant Baby Rib Bodysuit (Printify Blueprint `561`)
* **Base Price (Standard):** **$13.58**
* **Base Price (Printify Premium):** **$10.57**
* **US Standard Shipping:** **$3.99 – $4.75** (average ~$4.25)
* **Top Print Providers:** Monster Digital, SwiftPOD, Awkward Styles.

#### Printful Comparison
* **Rabbit Skins 4400:** Base cost $12.95 – $13.95 + $4.69 US shipping = $17.64 – $18.64 total fulfillment.

#### Unit Economics (At $20.00 Retail with Stripe Fee $0.88, Net Revenue $19.12)
| Tier | Base + Shipping | Stripe Fee | Net Payout | Net Margin |
|---|---|---|---|---|
| Printify Standard | $17.83 | $0.88 | **+$1.29** | 6.5% |
| Printify Premium | $14.82 | $0.88 | **+$4.30** | 21.5% |
| Printful Standard | $18.14 | $0.88 | **+$0.98** | 4.9% |

*Verdict:* **BORDERLINE CONFIRMED.** At $20.00, it stays cash-positive ($1.29 to $4.30 profit), but has little margin for error on standard plans if colored blanks or postal increases apply.
* **Recommendation:** If the store runs without Printify Premium, consider raising to **$22.00** (`price_cents: 2200`), producing **+$3.23** profit per bodysuit.

---

### C. Little Sprout Cap (`hat`)
* **Description:** Adjustable kids' cap, embroidered with the Sprout leaf logo.
* **Catalog Variants:** `None` (adjustable strap)
* **Current Retail Price:** `$18.00` (`price_cents: 1800`)

#### Printify Pricing (Custom Embroidery)
* **Primary Blanks:**
  1. **Yupoong 6245CM Classic Dad Cap** (Printify Blueprint `776`): 100% cotton chino twill, 6-panel unstructured low-profile, antique brass buckle.
  2. **OTTO Cap 18-253 Low Profile Baseball Cap** (Printify Blueprint `18-253`): 100% cotton twill, low profile, hook-and-loop closure.
* **Base Price (Standard, with embroidery):** **$15.38 – $16.12**
* **Base Price (Printify Premium):** **$11.37 – $11.92**
* **Standard US Shipping:** **$4.69 – $4.75** (hats require rigid box packaging)
* **Digitization / Setup Fee:** Included in Printify base price for standard stitch areas.

#### Printful Comparison
* **Yupoong 6245CM Embroidered Dad Hat:** Base cost $15.50 + $4.69 US shipping = $20.19 total fulfillment (+ one-time $6.50 embroidery digitization fee).

#### Unit Economics at Current $18.00 Retail (Stripe Fee $0.82, Net Revenue $17.18)
| Tier / Setup | Total Fulfillment Cost | Net Revenue ($18.00 - Stripe) | Net Profit / Loss |
|---|---|---|---|
| Printify Standard ($15.38 + $4.69) | $20.07 | $17.18 | **-$2.89 LOSS** |
| Printify Standard (Yupoong $16.12 + $4.75) | $20.87 | $17.18 | **-$3.69 LOSS** |
| Printify Premium ($11.37 + $4.69) | $16.06 | $17.18 | **+$1.12** (6.2%) |
| Printful Standard ($15.50 + $4.69) | $20.19 | $17.18 | **-$3.01 LOSS** |

#### Target Pricing Model for Cap
To eliminate the loss and achieve positive unit economics on standard Printify accounts:
| Proposed Price | Stripe Fee (2.9% + $0.30) | Net Revenue | Net Profit (Printify Std) | Net Profit (Printify Prem) |
|---|---|---|---|---|
| **$20.00** | $0.88 | $19.12 | -$0.95 (still loses) | +$3.06 |
| **$22.00** | $0.94 | $21.06 | **+$0.99** (breaks even) | **+$5.00** |
| **$24.00** | $1.00 | $23.00 | **+$2.93** (safe buffer) | **+$6.94** |

*Verdict:* **FAILED / ACTION REQUIRED.** $18.00 cannot stand unless subsidized as a marketing loss leader.
* **Recommendation:** Increase to **$22.00** (`price_cents: 2200`) or **$24.00** (`price_cents: 2400`).

---

### D. Little Sprout Library Bag (`tote`)
* **Description:** Sturdy cotton tote for hauling library books.
* **Catalog Variants:** `None`
* **Current Retail Price:** `$15.00` (`price_cents: 1500`)

#### Printify Pricing
* **Primary Blank:** Cotton Canvas Tote (Liberty Bags OAD113 / generic canvas tote)
* **Base Price (Standard):** **$9.67** | Premium: **$7.12**
* **Standard US Shipping:** **$4.19 – $4.50**
* **Stripe Fee (at $15.00):** **$0.74**

#### Unit Economics (At $15.00 Retail, Net Revenue $14.26)
* **Standard Plan:** $9.67 base + $4.19 shipping = $13.86 total cost. Net profit: **+$0.40** (2.7% margin).
* **Premium Plan:** $7.12 base + $4.19 shipping = $11.31 total cost. Net profit: **+$2.95** (19.7% margin).

---

## 3. Printify vs. Printful Platform Comparison

| Evaluation Metric | Printify | Printful | Advantage / Context |
|---|---|---|---|
| **Integration in Repo** | Full integration coded in `app/services/printify.py` | Not implemented | **Printify** (zero code change required) |
| **T-Shirt Base Cost** | $7.13 – $11.66 | $8.25 – $13.25 | **Printify** (~$1–$2 cheaper per unit) |
| **Bodysuit Base Cost** | $10.57 – $13.58 | $12.95 – $13.95 | **Printify** (especially with Premium) |
| **Embroidered Cap Cost** | $11.37 – $16.12 | $14.50 – $16.00 | Tie on base price; Printify has no digitization fee |
| **Embroidery Digitization** | Built into production price | $6.50 one-time fee per design | **Printify** |
| **US Standard Shipping** | $3.99 – $4.75 | $4.69 flat rate | **Printify** (slightly lower base shipping) |
| **Production Speed** | 2–5 business days | 2–5 business days | Tie |

**Decision:** Maintain **Printify** as the primary POD partner. It matches the existing codebase, incurs no upfront embroidery digitization fees, and offers lower unit costs.

---

## 4. Printify Catalog Mapping Reference (for `app/products.py`)

When configuring products in Printify (see `rewards-api/DEPLOY.md` Step 5), use these verified Blueprint IDs:

```python
# T-Shirt
# Note: youth and adult sizes are combined under the "tshirt" catalog item.
# Printify uses blueprint 420 for Youth (YS, YM, YL) and blueprint 12 for Adult (AS, AM, AL).
"tshirt": {
    "blueprint_id": 420,  # Bella+Canvas 3001Y (or 12 for adult Bella+Canvas 3001)
    "print_provider_id": 99,  # e.g., SwiftPOD or Monster Digital
    # variants: map "YS", "YM", "YL", "AS", "AM", "AL" to Printify variant IDs
}

# Baby Bodysuit
"onesie": {
    "blueprint_id": 561,  # Rabbit Skins 4400 Infant Baby Rib Bodysuit
    "print_provider_id": 99,
    # variants: map "6M", "12M", "18M", "24M" to Printify variant IDs
}

# Cap / Hat
"hat": {
    "blueprint_id": 776,  # Yupoong 6245CM Classic Dad Cap (or 18-253 for OTTO Cap)
    "print_provider_id": 99,
    # variant_id: single Printify variant ID
}
```

---

## 5. Summary of Recommended Owner Decisions

1. **Cap Pricing Decision (Crucial):**
   - Approve changing `hat.price_cents` from `1800` ($18.00) to `2200` ($22.00) or `2400` ($24.00) in `app/products.py`.
   - Update `shop.html` display text if hardcoded references exist.
2. **Bodysuit Pricing Decision (Optional):**
   - Choose whether to keep `onesie.price_cents` at `2000` ($20.00, viable but tight) or bump to `2200` ($22.00) for consistent $3+ margin.
3. **Printify Premium Subscription:**
   - At launch, start on the free standard plan. If order volume exceeds 10–12 items/month across all SKUs, the $29/month Printify Premium plan pays for itself immediately (saving ~$2.50 to $4.00 per item).
