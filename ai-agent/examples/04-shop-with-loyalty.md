# Example 04 — Shop with behaviours

**What this example tests:** the section-vs-behaviour split, and honest handling of inferred codenames. Two of the four requested features create no section at all. Two of the section types are inferred rather than observed.

## Input

> A shop app selling our ceramics, where people browse by collection, with a loyalty card and emails to people who leave something in their basket.

## Must get right

- **Loyalty and abandoned-cart go in `extensions[]` with `createsSection: false`.** Putting them in `sections[]` is a failure; declaring them gaps is a worse failure.
- The Shop-plan gate stated in prose before the plan, not just flagged.
- `GBModuleTypeCommercecollectionslist` at high confidence; `GBModuleTypeCommerce` and `GBModuleTypeProfile` with `typeVerified: false` **and** a sentence saying they're inferred.
- No codename invented for Cart or Order; emitted as `status: "undetermined"` rather than forced into matched or gap.
- `catalogEntry` present on every section, `null` where no tile corresponds.
- Prices dated.

## Must not do

- Write a custom-code spec for the loyalty card.
- Present inferred codenames with the same confidence as the content-type enum.
- Guess a `service` value for the `Commerce*` types.

---

# App Structure — Ceramics shop

## Summary

A native eCommerce app: browse by collection, buy in the app, with loyalty rewards and abandoned-basket recovery.

Four requested features split two ways — **two are sections, two are behaviours that add no screen.** That distinction is the main thing to take from this plan.

> **Plan gate.** Native in-app selling requires a **GoodBarber Shop plan**. Every section below is unavailable on a standard plan. If you're on a standard plan today, the alternative is `GBModuleTypeShop` — a section linking out to an existing storefront on Shopify, Amazon or Etsy — which works on any plan but sells nothing inside the app.

> **Confidence note.** The section codenames below come from lining up GoodBarber's public shop documentation against a section-type enum captured from a **non-Shop** back office. `GBModuleTypeCommercecollectionslist` is a direct match. The other two are inferred and marked as such. One capture from a Shop-plan back office would confirm all of them — the same method used for the content types.

## Sections

### 1. Collections — `GBModuleTypeCommercecollectionslist`

The browse-by-collection entry point. Confidence: **highest of the three** — the enum describes this codename as "eCommerce collections index", a direct name match to the documented Collections list.

Still emitted with `typeVerified: false`. A name matching is not the same as having watched a live Shop app's Collections screen report that constant, and the whole `Commerce*` family is inference until one does.

Directly satisfies "browse by collection".

### 2. Products — `GBModuleTypeCommerce` *(inferred)*

The catalogue. Its detail view is the product page — the same list/detail pairing every content section has, so the product page is not a separate section.

Confidence: **medium**. `GBModuleTypeCommerce` is the enum's primary commerce type ("Native eCommerce, Shop-plan apps only") and the documentation lists a Products list section, but the pairing wasn't observed directly.

> **Product page design is global.** GoodBarber's documentation is explicit: the product page design applies to every product. There is no per-product layout, so different-looking pages for different ranges aren't available.

*If you want a second product list scoped to one collection — a "New in" screen, say — that's `GBModuleTypeCommercealias`, the duplicate-view type. Also inferred.*

### 3. My Account — `GBModuleTypeProfile` *(inferred)*

Orders, addresses, customer details. Confidence: **medium** — the enum describes `Profile` as "User account / profile" and documents it as account-gated, which matches the documented My Account screen.

Needed here regardless: loyalty and abandoned-basket recovery both require identifiable customers.

### Cart and checkout — *codename not captured*

The documentation lists Cart and Order as designable screens, and no codename in the captured enum matches either. Two possibilities: they're sections whose codenames weren't in the non-Shop app's markup, or they're shop runtime rather than enumerable sections.

**Not guessing.** They're emitted with `status: "undetermined"` — the schema's third state, for a screen that exists but whose codename wasn't captured. Not `"matched"` (there is no type) and not `"gap"` (the platform clearly provides this). A plausible-looking constant that doesn't exist would be worse than this admission — someone would try to use it.

## Extensions

These add no sections. They're configured on the shop, and nothing appears in the app's structure.

| Extension | Price (as of 2026-08-13) | What it does |
|---|---|---|
| **Loyalty Program** | $10/month | Points and rewards. This is the "loyalty card" — a shop behaviour, not a screen. |
| **Abandoned Order** | $10/month | Recovers unfinished orders by email and push. This is the "emails to people who leave something in their basket". |

**About $20/month on top of the Shop plan.** Verify both on the eCommerce extensions page before committing — the store's list badge and full pricing line can disagree, and only the pricing line is reliable.

Neither needs a section, and neither is a gap. An agent that put these in `sections[]` would send you looking for screens that will never exist; one that called them gaps would have you commission custom code for features that ship for $10/month.

Worth knowing, unasked: **Stock Management** ($5/month) is usually wanted alongside these, and **payment methods are all free** — Stripe, PayPal, Apple Pay, Klarna and the rest.

## Gaps

None. Every requested feature exists — two as sections, two as extensions.

## Validation

- Shop-plan gate stated in prose and flagged in JSON.
- Every intent sorted into section or behaviour before being planned.
- Both extensions carry `createsSection: false`, a price and a date.
- **All three** inferred codenames carry `typeVerified: false` and a sentence in the body — including the strong name match.
- No codename invented for Cart or Order; emitted as `status: "undetermined"` rather than forced into matched or gap.
- `catalogEntry` present on every section, `null` where no tile corresponds.
- `service` omitted for all `Commerce*` types, with `serviceVerified: false`.
- `Shop` named as the standard-plan alternative.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-13",
  "summary": "Native eCommerce app for a ceramics studio, browsable by collection.",
  "planRequirement": "GoodBarber Shop plan — all Commerce* sections are gated.",
  "sections": [
    {
      "order": 1,
      "name": "Collections",
      "intent": "Browse products by collection",
      "status": "matched",
      "type": "GBModuleTypeCommercecollectionslist",
      "typeVerified": false,
      "service": null,
      "serviceVerified": false,
      "catalogEntry": "Collections list",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "plan-gated", "note": "Shop plan", "asOf": "2026-08-13" },
      "notes": "Highest confidence of the three — the enum describes this codename as the eCommerce collections index, a direct name match to the documented Collections list. Still typeVerified:false: a name match is not an observation of a live section."
    },
    {
      "order": 2,
      "name": "Products",
      "intent": "The product catalogue",
      "status": "matched",
      "type": "GBModuleTypeCommerce",
      "typeVerified": false,
      "service": null,
      "serviceVerified": false,
      "catalogEntry": "Products list",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "plan-gated", "note": "Shop plan", "asOf": "2026-08-13" },
      "notes": "INFERRED from public docs against a non-Shop enum capture. Product page is the detail view, not a separate section. Product page design is global across all products."
    },
    {
      "order": 3,
      "name": "My Account",
      "intent": "Customer orders, addresses and details",
      "status": "matched",
      "type": "GBModuleTypeProfile",
      "typeVerified": false,
      "service": null,
      "serviceVerified": false,
      "catalogEntry": "My Account",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "plan-gated", "note": "Account-enabled app", "asOf": "2026-08-13" },
      "notes": "INFERRED. Required regardless — loyalty and abandoned-order recovery both need identifiable customers."
    },
    {
      "order": 4,
      "name": "Cart and checkout",
      "intent": "Buying in the app",
      "status": "undetermined",
      "type": null,
      "typeVerified": false,
      "service": null,
      "serviceVerified": false,
      "catalogEntry": null,
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "plan-gated", "note": "Shop plan", "asOf": "2026-08-13" },
      "notes": "CODENAME NOT CAPTURED. Documented as designable screens; no matching constant in the captured enum. May be shop runtime rather than enumerable sections. Deliberately not guessed."
    }
  ],
  "extensions": [
    {
      "name": "Loyalty Program",
      "createsSection": false,
      "pricing": { "tier": "paid", "price": "$10/month", "asOf": "2026-08-13" },
      "note": "The 'loyalty card'. Configured on the shop; adds no section."
    },
    {
      "name": "Abandoned Order",
      "createsSection": false,
      "pricing": { "tier": "paid", "price": "$10/month", "asOf": "2026-08-13" },
      "note": "Email and push recovery of unfinished orders. Adds no section."
    }
  ],
  "validation": {
    "sectionCount": 4,
    "warnings": [
      "Shop plan required — the entire plan is void on a standard plan. GBModuleTypeShop is the standard-plan alternative.",
      "GBModuleTypeCommerce and GBModuleTypeProfile are inferred, not observed. Confirm from a Shop-plan back office.",
      "Cart and Order codenames were not captured and are deliberately null.",
      "Extension prices are ~$20/month combined; re-verify on the eCommerce extensions page."
    ]
  }
}
```

## Sources

- `ai-output/7-section-type-codenames.md` — the four commerce-adjacent codenames and their enum descriptions; the note that they never appear in the standard catalog. Back-office capture 2026-08-12.
- [Section design (Shop)](https://www.goodbarber.com/help/shop/design-of-your-sections-r89/section-design-a106/) — the documented shop section list and the global product-page design rule, accessed 2026-08-13.
- [eCommerce extensions collection](https://www.goodbarber.com/extensions/collections/ecommerce/) — extension list, prices, and which entries create a section, accessed 2026-08-13.
