---
name: commerce-sections
description: Plan the structure of a GoodBarber eCommerce (Shop) app — the product list, collections list, product detail, cart, orders and customer account screens, and the plan gate that makes all of them unavailable to standard apps. Use when a description involves selling products in the app, a product catalogue, collections or categories of products, a cart or checkout, customer accounts, or shop features like loyalty, discount codes, stock or abandoned-cart recovery. Owns the rule that most shop features are extensions that create no section at all. Do NOT use when the user only wants to link out to an existing Shopify, Amazon or Etsy store (that is GBModuleTypeShop, in utility-sections).
---

# Commerce Sections

The Shop product line. A separate plan, a separate section set, and a separate extension store from the standard app catalog — which is why this is its own skill and not a category inside another one.

## 1. Read this before anything else in here

**Two gates and one honesty requirement.**

**Gate 1 — the plan.** `GBModuleTypeCommerce`, `GBModuleTypeCommercealias`, `GBModuleTypeCommercecollectionslist` are Shop-plan only. `GBModuleTypeProfile` needs an account-enabled app. If the user hasn't said they're on a Shop plan, **state the gate before planning the shop**, because the entire plan is void without it.

**Gate 2 — selling in the app vs linking to a store.** These are different products with very different costs:

| The user wants | Answer | Cost |
|---|---|---|
| Products browsable and buyable **inside** the app | `Commerce*` — this skill | Shop plan |
| A tile that opens their existing Shopify / Amazon / Etsy store | `GBModuleTypeShop` — `utility-sections` | Any plan |

"I want a shop in my app" is ambiguous between the two. Ask, or plan the cheaper one and name the other.

**The honesty requirement.** The `GBModuleType*` codenames are read from a back-office DOM. The app that was captured is not on a Shop plan, so most of the mapping below is **inferred from the public help documentation, not observed**. Every inferred type must be emitted with `typeVerified: false` and described as inferred in the report body. Do not present these with the same confidence as the content types.

## 2. The mapping, with confidence

The help documentation names the shop's sections; the enum contains four commerce-adjacent codenames. Lining them up:

| Shop section (documented) | Type | Confidence | Basis |
|---|---|---|---|
| Collections list | `GBModuleTypeCommercecollectionslist` | **Highest** | The codename is literally this, and the enum describes it as "eCommerce collections index". Still an inference — a name match, not an observation |
| Products list | `GBModuleTypeCommerce` | Medium | The primary commerce type; described as "Native eCommerce (Shop-plan apps only)" |
| A second product list scoped to one collection | `GBModuleTypeCommercealias` | Medium | Enum describes it as "eCommerce alias/duplicate view", which matches a duplicated, filtered product list |
| My Account | `GBModuleTypeProfile` | Medium | Enum describes it as "User account / profile"; documented as account-gated |
| Product detail | *not a section* | High | A detail view of the products list — the same list/detail pairing every content type has |
| Cart | unknown | **Low** | Documented as a designable screen; no matching codename in the captured enum. May be shop runtime rather than an enumerable section |
| Order | unknown | **Low** | Same as Cart |

**Services for all `Commerce*` types are unverified.** They are native rather than connector-backed, so most likely none — but that is an inference. Emit `"service": null` with `serviceVerified: false`. Never omit the key and never guess a value.

**All four types get `typeVerified: false`, including `Commercecollectionslist`.** The flag means *this type is right for this screen* was inferred rather than observed. A codename existing in the enum and matching a documented screen name is a strong signal, not an observation — nobody has watched a live Shop app report that constant on its Collections screen. High confidence still gets flagged.

**Cart and Order:** do not invent a codename for these. If a plan needs them, emit `status: "undetermined"` with `type: null` and a note saying the codename wasn't captured — the schema's third state exists for exactly this. Not `"matched"` (no type) and not `"gap"` (the platform clearly provides the screen). This is exactly the case where a plausible-looking constant would be worse than an admission.

**How to close this gap.** One capture from a Shop-plan back office resolves all of it — read the `data-type` attributes off the Structure screen, the same method that produced the content-type enum. Recommend that rather than accumulating more inference.

## 3. The rule this skill exists for: extension ≠ section

The eCommerce extension store splits into two kinds of thing, and treating them alike produces wrong plans in both directions.

### Extensions that create a section

| Extension | Price (as of 2026-08-13) |
|---|---|
| Blog | Free |
| YouTube | Free |
| Contact Form | Free |
| Form | Free |
| Search for eCommerce | Free |

### Extensions that create no section at all

| Extension | Price (as of 2026-08-13) | What it is |
|---|---|---|
| Loyalty Program | $10/month | Points and rewards on the shop |
| Discount Codes | $10/month | Promotional codes |
| Abandoned Order | $10/month | Email and push recovery of unfinished orders |
| Stock Management | $5/month | Centralised inventory |
| Buy Again | $5/month | One-click reorder |
| Cart Reminder | $5/month | Popup showing cart contents on return |
| App Walkthrough | $5/month | First-launch onboarding overlay |
| Push Notifications | Free | — |
| Statistics & Dashboard | Free | — |
| Payment methods | Free | Stripe, PayPal, Apple Pay, Klarna, Alipay, Bancontact, iDeal, and more |
| Business integrations | Free | Zapier, Make, Mailchimp, HubSpot, Google Sheets, Slack, and many others |

Prices move. Treat this table as a starting point and verify through `extensions-pricing` — but the **structural** split (creates a section or doesn't) is stable and is the part that matters here.

### What to do with it

"I want a loyalty card in my shop" produces **no section**. An agent whose only output shape is a list of sections has two ways to be wrong about that: invent a section that doesn't exist, or declare a gap and write a custom-code spec for a $10/month feature that already ships.

So, for every shop intent, ask first: **screen, or behaviour?**

- Screen → `sections[]` with a type.
- Behaviour → `extensions[]` with `createsSection: false`, a price, and an `asOf` date.

Both arrays appear in the same plan. A shop app typically has a handful of sections and a longer list of extensions.

## 4. Planning a shop app

A minimal native shop is roughly:

1. **Collections list** — `GBModuleTypeCommercecollectionslist`. The browse-by-category entry point.
2. **Products list** — `GBModuleTypeCommerce`. The catalogue. Its detail view is the product page.
3. **My Account** — `GBModuleTypeProfile`. Orders, addresses, details.
4. **Cart and checkout** — provided by the shop; describe in prose, don't invent a type.

Then, depending on the description:

- Several **product lists scoped to different collections** → `GBModuleTypeCommercealias` for the extras, since it's the duplicate-view type.
- **Content alongside the shop** — a blog, videos, an about page — are ordinary sections from `content-sections` and `utility-sections`. A shop app is a normal app that also sells.
- **Behaviours** → `extensions[]`.

Two design facts worth stating in a plan:

- **Product page design is global.** The documentation is explicit that the product page design applies to all products; there is no per-product layout. If the user imagines different-looking product pages for different ranges, say it isn't available.
- **Section design is per-section, over a global style.** A global style applies to all pages by default and individual sections can be customised on top. Design is out of scope for this agent, but the constraint above is a structural expectation worth setting early.

## 5. Before emitting a commerce plan

- [ ] The Shop-plan gate is stated in prose, not just flagged in JSON.
- [ ] `Shop` (link out) vs `Commerce` (native) was decided explicitly, and the alternative named.
- [ ] **Every** commerce type carries `typeVerified: false` **and** a sentence in the report saying it's inferred — `Commercecollectionslist` included.
- [ ] No codename invented for Cart or Order; emitted as `status: "undetermined"`.
- [ ] `"service": null` for `Commerce*` — key present, never omitted — with `serviceVerified: false`.
- [ ] Every shop feature was sorted into section or extension before being planned.
- [ ] Every extension in `extensions[]` has `createsSection: false`, a price and an `asOf` date.
- [ ] Prices verified through `extensions-pricing` rather than copied from the table above (§3).
- [ ] If the user might get a Shop-plan back office, the plan recommends capturing the real codenames.

---

*Sources: section-docs/0-section-type-codenames.md; GoodBarber help — [Section design (Shop)](https://www.goodbarber.com/help/shop/design-of-your-sections-r89/section-design-a106/) for the documented shop section list and the global product-page design rule, accessed 2026-08-13; [eCommerce extensions collection](https://www.goodbarber.com/extensions/collections/ecommerce/) for the extension list, prices and which entries create a section, accessed 2026-08-13.*