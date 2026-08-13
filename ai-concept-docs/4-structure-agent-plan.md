# Plan — App Structure Agent

**Status:** planning only. Nothing built yet. This document is the design to approve before writing any skill file.
**Revision 2** (2026-08-13) — adds eCommerce coverage, drops hardcoded catalog sizes, resolves the supersede decision, answers the catalog-location question in §4.

**Goal (restated):** an agent that reads a plain-English app description and returns the required GoodBarber structure — the section types, the service behind each one, the price, and, where nothing fits, a developer-ready custom-code specification.

**Decisions taken:**

| Question | Answer |
|---|---|
| Output format | One Markdown report with an embedded JSON block |
| Number of skills | Split by family and complexity — **6**, up from 5 (see §3) |
| Scope | Structure only — no design, navigation or Home |
| Catalog source | Tiered by volatility — see §4 |
| Existing skills | **Supersede** `app-structure` and `app-extensions`; leave `app-design` alone |

---

## 1. Three corrections to the brief

These change the design, so they come first.

### 1.1 The output is a provisioning plan, not a `gbsettings` document

The example JSON in the prompt is shaped like `gbsettings.sections` — `appId` at the top, sections keyed by index. But `7-section-type-codenames.md` §7 established that this document cannot create structure:

- the JSON editor runs with `canChangeProperty: false`, so no key can be added — and a new section *is* a new key;
- of 539 fields, the read-only ones are exactly `type`, `id`, `title`, `contentSource.url`, `ids`, `category_index` — every structural field;
- sections are actually created by `GET /manage/app/content-add-<service>/`.

So the agent must emit **actions to perform**, not a document to paste. Same JSON shape, different meaning — and each section should carry the `content-add-<service>` route that would create it. This is the difference between a plan that can be executed later by an implementation agent and one that looks executable but isn't.

### 1.2 `baseSource` doesn't live where the example puts it

§5 of the same report: the RSS URL is **not** in the section JSON. `contentSource.url` on both `Artigos` (mcms) and `Notícias` (rss) is the same internal path `/front/get_items/{appId}/{sectionId}/`, and a recursive scan for any `http(s)://` in either object returned zero results. The feed address is a separate server-side record, edited in Settings.

Keep the field — the user needs to know a source is required and what to point it at — but move it into its own `sourceBinding` object flagged as a **second, separate step**. Otherwise the output implies "write this URL into the section JSON", which cannot work.

### 1.3 The Photos case in your example is not a gap

Your walkthrough concludes that "a photos section linked to an api with images" has no match and falls to custom code. It has an exact match: `GBModuleTypePhoto` + service `custom` — the *Photo custom feeds* tile, documented as "point at your own JSON matching GoodBarber's Content API spec."

This matters more than one wrong example. `custom` recurs across all six content types (`Article`, `Sound`, `Video`, `Photo`, `Agenda`, `Maps`) and is the most-missed escape hatch in the catalog. An agent that forgets it will declare a gap on most "connect it to my API" requests and generate custom-code specs nobody needed. **Checking `custom` on the matched type is mandatory before any gap is declared.**

The skill needs a *real* gap example instead: "users can save products to a wish list they build themselves" — no type models user-owned mutable collections (`Bookmark` is auto-added and read-only over existing items), so it genuinely resolves to `GBModuleTypePlugin` + custom code. Convenient, since `ai-output/lista-desejos-custom-code/` is already the worked answer.

*(Minor: the example prompt says the guide works in New York, the app is about Barcelona, and the news is about New York. Normalised to New York throughout.)*

---

## 2. Principle: no hardcoded catalog sizes

*(Your suggestion 1, generalised.)*

The agent must never treat a count as a bound. Not "30 types", not "47 services", not "190 extensions", not "120 sections". Every one of those numbers is a snapshot of one app's back office on one day, and all of them move.

What this changes in practice:

- Counts appear only as **"known as of `<date>`"**, never as "the catalog contains N".
- The 120-section figure comes out of the validation rules as a hard check. It's a real per-app instance cap — ReBook's back office reported *"7 / 120 sections used"* — but it's a number the platform tells you at runtime, not one the agent should assert. If a section count looks large, the agent notes that apps have an instance cap and the back office reports the current one. It does not refuse to plan a 15-section app.
- A user request naming an extension the skill has never heard of is **not** a gap. It's a cue to look it up (§4). Only after the lookup fails does the gap path open.
- The one genuinely closed list stays closed: the agent must never **invent** a `GBModuleType*` codename. Unknown extension → look it up. Unknown type → gap path. Never a guess that looks like a real constant.

---

## 3. Architecture

```
CLAUDE.md            project rules, GoodBarber background, where outputs go
SYSTEM-PROMPT.md     role, the decision ladder, invariants, refusal rules
   │
   ├── section-routing/       ← always applies: intent → type, owns output schema
   ├── content-sections/      ← the 6 feed types + the service axis
   ├── utility-sections/      ← static pages, forms, links, social, live
   ├── commerce-sections/     ← NEW: the Shop product line (§5)
   ├── extensions-pricing/    ← free vs paid, plan gating, live store lookup
   └── custom-code-spec/      ← the gap path: developer-ready specification
```

### Why this split

The split follows **where the decisions are**, not where the types are.

| Skill | Triggers when | Owns |
|---|---|---|
| `section-routing` | every request | the type enum, catalog→type map, the decision ladder, the output schema, validation rules |
| `content-sections` | request mentions a feed of items — articles, news, blog, photos, video, audio, events, places | Article / Photo / Video / Sound / Maps / Agenda; service tables; list+detail model; categories; `custom` feed rules |
| `utility-sections` | request mentions a static page, contact, form, link, search, QR, social, storefront link, live stream | About, Contact, Form, Submit, Search, Qrcode, Clickto, Fakeclickto, Custom, Node, Shop, Live, Facebook/Instagram/Twitter, and the auto-added set |
| `commerce-sections` | request describes selling products, a catalogue, a cart, orders, customer accounts | `Commerce*`, `Profile`; the Shop-plan gate; the section-vs-feature rule (§5.2) |
| `extensions-pricing` | any section resolves to something billable, or nothing matched | tiers, plan gating, the live goodbarber.com/extensions lookup |
| `custom-code-spec` | `section-routing` declares a gap | the spec template, required detail level, the two worked examples |

**Why six and not five:** eCommerce is a separate product line, not a category within the main one. It has its own section types, its own extension store at a different URL, its own pricing, and a plan gate that makes all of it unavailable to most apps. Folding it into `utility-sections` would load shop guidance on every blog-app request and put two unrelated extension catalogues in one skill.

Rejected alternatives, briefly:

- **One skill.** Loads every type × every service + pricing + spec guidance on every request. Most is irrelevant to any single app, and long context is where type/service confusion starts.
- **One skill per type.** Claude routes to skills by matching description text; thirty descriptions that all read "handles a GoodBarber section" trigger unreliably, and a four-section app pulls in four skills. The catalog's own shape argues against it: 84 tiles collapse to 30 types, and 13 of those tiles are one type.

The chosen split reflects the real asymmetry: `Article` has 10 services and needs a page of guidance; `Qrcode` has none and needs one line.

---

## 4. Where the catalog lives — answering your question

**Neither purely.** The vocabularies have different volatility, so they get different mechanisms. Baking in a price is wrong for the same reason searching the web for `GBModuleTypeArticle` is wrong.

| Vocabulary | How fast it moves | Where it lives | What the agent does |
|---|---|---|---|
| **`GBModuleType*` codenames** | barely — it's a native SDK enum; changing a value breaks every app already built | baked into `section-routing` | decide from the skill. Never search, never invent. Nothing fits → gap path |
| **`service` values** | slowly — grows when GoodBarber adds a connector | baked into `content-sections` / `commerce-sections` as *known-good, not exhaustive* | prefer a known service. User names a platform that isn't listed → don't fail: check the site, emit `serviceVerified: false` |
| **Extensions and prices** | fast — 190+ and growing, prices change | **not** baked as truth; a small dated cache exists only as an offline fallback | look it up live whenever a section is billable or nothing matched. Always cite the date |

The rule for the skill, in one line: **types and services are decided from the skill; extensions and prices are verified on the site.**

Why not always search:

- Most requests resolve to free CMS sections where the store is irrelevant — a blog app would fire lookups that change nothing.
- Live search is non-deterministic. The same prompt returning different types on different days makes the agent untestable, and §9's test cases stop meaning anything.
- These are different problems. Picking a type is **classification over a stable closed vocabulary**. Pricing an extension is **lookup over a moving catalog**. Classification wants the vocabulary in context; lookup wants freshness.

Why not always baked:

- Prices go stale silently, and a wrong price in a plan is worse than no price.
- The store grows. A baked list means every new extension reads as a gap, and the agent starts writing custom-code specs for things that shipped last month — exactly the failure your suggestion 1 is guarding against.

When the agent can't reach the site: fall back to the cache, and say so in the output — "as of `<cache date>`, unverified this run."

---

## 5. eCommerce coverage

*(Your suggestion 3.)*

### 5.1 What's confirmed and what isn't

The public help docs name the shop's sections; the `GBModuleType*` codenames come from a back-office DOM, and ReBook is not a Shop-plan app. So the mapping below is part observed, part inferred, and the plan says which is which.

| Shop section (from help docs) | Likely type | Confidence |
|---|---|---|
| Collections list | `GBModuleTypeCommercecollectionslist` | **High** — the codename is literally this |
| Products list | `GBModuleTypeCommerce` | Medium — it's the primary commerce type |
| A second product list scoped to one collection | `GBModuleTypeCommercealias` | Medium — matches "alias/duplicate view" |
| My Account | `GBModuleTypeProfile` | Medium — `Profile` is documented as account-gated |
| Product detail | *not a section* | High — a detail view of the products list, same as Article→Article |
| Cart, Order | unknown | **Low** — may be shop runtime rather than enumerable sections |

Services for all `Commerce*` types are **unverified**. They're native, so most likely none, but that's an inference and the skill must label it.

**This is the honest limit:** codenames cannot be read off the public site — they only exist in a Shop-plan back office. Everything above marked Medium or Low stays marked in the skill, and the agent emits `typeVerified: false` for them so a wrong guess is visible rather than silent. If you ever get access to a Shop-plan app, capturing those `data-type` attributes the way you did for ReBook would resolve all of it in one pass.

### 5.2 The finding that changes the design: extension ≠ section

The eCommerce store splits cleanly into two kinds of thing, and the agent has been assuming everything is the first kind:

- **Extensions that create a section** — Blog (free), YouTube (free), Contact Form (free), Form (free), Search for eCommerce (free).
- **Extensions that add a feature to the shop and create no section at all** — Loyalty Program ($10/mo), Discount Codes ($10/mo), Abandoned Order ($10/mo), Buy Again ($5/mo), Cart Reminder ($5/mo), Stock Management ($5/mo), App Walkthrough ($5/mo), Push Notifications (free), Statistics & Dashboard (free), every payment method (all free), every CRM/automation integration (all free).

So "I want a loyalty card in my shop" produces **no section**. If the agent's only output shape is a list of sections, it has to either invent a section that doesn't exist or declare a gap — and both are wrong.

This closes the open risk flagged in revision 1 ("one intent ≠ one section"). The fix is a second array in the output:

```json
"extensions": [
  {
    "name": "Loyalty Program",
    "createsSection": false,
    "pricing": { "tier": "paid", "price": "$10/month", "asOf": "2026-08-13" },
    "note": "Configured on the shop; adds no section to the structure."
  }
]
```

Step 1 of the ladder gains a fork before the type lookup: **does this intent want a screen, or a behaviour?** Behaviours go to `extensions[]`, screens go to `sections[]`. Cheap to check, and it prevents a whole class of wrong answers.

---

## 6. The decision ladder

Belongs verbatim in the system prompt.

For each feature the user describes:

**Step 0 — Decompose.** Turn the description into discrete feature intents. Say the decomposition out loud — "a page with news and photos" is two intents.

**Step 1 — Screen or behaviour?** A screen the user navigates to → continue to Step 2. A behaviour layered onto the app or shop (loyalty, discounts, push, analytics, payments, abandoned-cart) → `extensions[]`, then Step 5. *(§5.2.)*

**Step 2 — Type.** Map the intent to exactly one `GBModuleType*`. Match on *intent*, never on the user's noun — users say "newsletter", "wish list", "TikTok", and none are types. No fit → Step 6.

**Step 3 — Service.** Given the type, choose from that type's known services:

- user names a platform they already publish on (WordPress, YouTube, Spotify, Substack…) → that platform's service;
- user has their own API or JSON feed → `custom`;
- user will author inside GoodBarber → `mcms`;
- type has no services → omit.

Platform named but not in the known list → check the site before concluding anything (§4).

**Step 4 — Check `custom` before giving up.** If Step 3 found nothing and the type is one of the six content types, `custom` is available. This step exists because skipping it is the most likely failure mode (§1.3).

**Step 5 — Price and plan.** Look up billable items live; cite the date. Flag `Commerce*` (Shop plans only) and `Profile` (account-enabled apps only) as gated rather than proposing them silently.

**Step 6 — Gap path.** Reachable only when Steps 2–4 all failed *and* a live lookup found nothing. Emit `status: "gap"` with **both** required outputs:
1. the nearest existing sections, each with an explicit statement of what it *won't* do;
2. a full custom-code specification (`GBModuleTypePlugin`, no service) per §8.

Never one or the other — the brief requires both.

**Step 7 — Validate** (§9), then emit.

### Two disclosure rules the agent must never skip

- **`Fakeclickto` is a link, not a section.** TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat produce a branded tile that opens the external app. Someone asking for "a TikTok feed in my app" gets a link and must be told so in the same breath. This is the sharpest expectation mismatch in the catalog, and the type name is the only warning.
- **`Custom` vs `Plugin`.** `Custom` = a web view pointed at a URL (Typeform, JotForm, Tawk.to are this with a preset). `Plugin` = code running inside the app. If the need is "embed this existing web thing", it's `Custom` and no custom-code spec is warranted.

---

## 7. Output format

**One Markdown file, with a JSON block inside it.**

Requirement 3.2 says a developer must be able to build the section after reading the description. That's multi-paragraph prose with headings and a data contract — it doesn't survive being a JSON string value. Requirement 4 asks for "a document". Markdown carries both; the JSON block keeps the machine-readable half intact for a later implementation agent.

### Report structure

```
# App Structure — <app name>
## Summary            what the app is, section count, total monthly cost
## Sections           one ## per section: intent → type → service → price → notes
## Extensions         behaviours with no section of their own (§5.2)
## Gaps               per gap: alternatives table + full custom-code spec
## Validation         what was checked, warnings raised
## Plan (JSON)        the fenced block below
## Sources            with access dates
```

### JSON schema

```json
{
  "appId": null,
  "generatedAt": "2026-08-13",
  "summary": "Tour-guide app for visitors to New York.",
  "sections": [
    {
      "order": 1,
      "name": "News",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": "rss",
      "serviceVerified": true,
      "catalogEntry": "RSS feeds",
      "createRoute": "/manage/app/content-add-rss/",
      "sourceBinding": {
        "required": true,
        "kind": "feedUrl",
        "suggested": "https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml",
        "note": "Bound server-side via section Settings. Not part of the section JSON."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Feed-backed, so no 'Edit the content' action — the service owns the items."
    },
    {
      "order": 2,
      "name": "Wish list",
      "status": "gap",
      "type": null,
      "service": null,
      "alternatives": [
        {
          "type": "GBModuleTypeBookmark",
          "shortfall": "Auto-added and read-only over existing items; users cannot create entries."
        }
      ],
      "customCode": {
        "type": "GBModuleTypePlugin",
        "service": null,
        "createRoute": "/manage/app/content-add-customcode/",
        "createRouteVerified": false,
        "specSection": "#custom-code-wish-list"
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" }
    }
  ],
  "extensions": [
    {
      "name": "Loyalty Program",
      "createsSection": false,
      "pricing": { "tier": "paid", "price": "$10/month", "asOf": "2026-08-13" },
      "note": "Configured on the shop; adds no section to the structure."
    }
  ],
  "validation": { "sectionCount": 4, "warnings": [] }
}
```

Changes from your example, and why:

| Your field | Change | Reason |
|---|---|---|
| `sections` as `{"1": {...}}` | array with `order` | order is data, not a key; keys were already index-like |
| `baseSource` | `sourceBinding` object | separate provisioning step, not a JSON field (§1.2) |
| `options: [(...), "customCode": "..."]` | `alternatives[]` + `customCode{}` | the tuple/string mix isn't valid JSON, and it conflates the two required answers |
| `"type": none` | `"type": null` + `status` | `none` is Python; `status` makes the gap explicit rather than inferred from nulls |
| — | `createRoute` | makes the plan executable (§1.1) |
| `"price": "free"` | `pricing: {tier, price?, asOf}` | paid extensions need an amount, and every price needs a date (§4) |
| — | `extensions[]` | behaviours that create no section (§5.2) |
| — | `typeVerified` / `serviceVerified` | inference made visible instead of silent (§5.1) |
| — | *(no `sectionLimit`)* | removed per §2 — the platform reports the cap, the agent doesn't assert it |

---

## 8. Custom-code specification template

What makes it "detailed enough for a developer" — required headings, in order:

1. **Purpose** — one paragraph: what the section does, who uses it.
2. **Screens and flow** — every screen, every transition, what the user sees first.
3. **Data model** — entities, fields, types, which are required.
4. **External contract** — endpoint, method, auth, request and response shapes with a real example payload. No external API → say so and specify local persistence instead.
5. **Rendering** — the HTML/CSS/JS structure inside the `GBModuleTypePlugin` section: containers, list item markup, loading and empty states.
6. **State and persistence** — what survives a reload, what doesn't, where it lives.
7. **GoodBarber integration points** — how it's opened from navigation, deep links, which theme variables it inherits.
8. **Edge cases** — empty result, network failure, slow response, unsupported content.
9. **Acceptance criteria** — a numbered checklist a developer can tick off.

Reference implementations already in the repo: `ai-output/gatos-custom-code/index.html` and `ai-output/lista-desejos-custom-code/index.html`. The skill points at these as the target shape and level of finish.

---

## 9. Validation rules

Run before emitting; every failure is a fix or a stated warning.

- `type` is a real codename from the enum. Never invented. Inferred ones carry `typeVerified: false`.
- `service` is in the known list for that specific type, or carries `serviceVerified: false`. `mcms` is not universal — `Photo` has it, `Clickto` does not.
- `Home` is a singleton — never propose a second.
- `Bookmark`, `Settings`, `Tos` (×2) are auto-added — reference, never create.
- `Commerce*` → Shop plans only; `Profile` → account-enabled apps only. Flag as gated, don't silently emit.
- Every `status: "gap"` carries **both** `alternatives` and `customCode`.
- Every externally-fetching `service` has a `sourceBinding`.
- Every `pricing` object has an `asOf` date.
- Behaviours with no screen are in `extensions[]`, not `sections[]`.
- Section count is reported, not capped (§2). Large counts get a note that the back office reports a per-app instance limit.

---

## 10. Files to create

**Supersede path chosen** — the new skills replace `app-structure` and `app-extensions`. `app-design` is out of scope and untouched.

```
ai-agent/
  CLAUDE.md
  SYSTEM-PROMPT.md
  skills/
    app-design/            (unchanged)
    section-routing/SKILL.md
    content-sections/SKILL.md
    utility-sections/SKILL.md
    commerce-sections/SKILL.md
    extensions-pricing/SKILL.md
    custom-code-spec/SKILL.md
  examples/
    01-tour-guide.md
    02-wish-list-gap.md
    03-social-traps.md
    04-shop-with-loyalty.md
```

Before deleting anything: I still haven't read `app-structure/SKILL.md` or `app-extensions/SKILL.md`, since the prompt restricted reading. Step 1 of the build is to read them and salvage anything the new design doesn't already cover — then delete. Git history holds the originals either way.

---

## 11. Build order

1. **Read and salvage** `app-structure` and `app-extensions`, then remove them.
2. **`section-routing/SKILL.md`** — the enum, catalog→type map, the ladder, output schema, validation rules. Everything else hangs off this.
3. **`content-sections/SKILL.md`** — the six feed types, service tables, `custom` rules, list/detail and categories model.
4. **`utility-sections/SKILL.md`** — remaining types, with the `Fakeclickto` and `Custom`-vs-`Plugin` disclosure rules.
5. **`commerce-sections/SKILL.md`** — the shop sections with confidence flags, the plan gate, the section-vs-feature rule.
6. **`extensions-pricing/SKILL.md`** — the tiered lookup policy from §4, both store URLs, the dated fallback cache.
7. **`custom-code-spec/SKILL.md`** — the §8 template plus the two worked examples.
8. **`SYSTEM-PROMPT.md` and `CLAUDE.md`** — written last, once the skills have settled.
9. **Run the four test cases** (§12) and fix what breaks.

---

## 12. Test cases

**A — Everything matches** (your example, corrected). Tour-guide app: news, photos from an API, map, info page.
Expected: `Article`+`rss`, `Photo`+`custom` (**not** a gap — the §1.3 check), `Maps`+`mcms`, `Article`+`mcms`. Four sections, all free, `sourceBinding` on the first two.

**B — Genuine gap.** "Users can save products to a wish list and reorder it."
Expected: `status: "gap"`; `Bookmark` offered as the near miss with its shortfall stated; a full custom-code spec.

**C — Traps.** "A TikTok feed, an AI chatbot that answers from my PDFs, and a Shopify store."
Expected: `Fakeclickto` + explicit "this is a link, not a feed"; `Plugin`+`rag` flagged paid with a dated price; `Shop`+`shopify`. Catches an agent that pattern-matches on brand names.

**D — Shop with a behaviour.** "A shop selling ceramics, browsable by collection, with a loyalty card and abandoned-cart emails."
Expected: `Commercecollectionslist` and `Commerce` in `sections[]` with `typeVerified: false` and the Shop-plan gate flagged; Loyalty Program and Abandoned Order in `extensions[]` with `createsSection: false` and dated prices. Catches an agent that turns every intent into a section.

---

## 13. Open risks

- **eCommerce codenames are partly inferred.** §5.1 marks them, but the marking only helps if the agent actually propagates `typeVerified: false` into the output. Test D exists to check that. Resolvable in one pass with access to a Shop-plan back office.
- **Prices drift.** Mitigated by §4's live lookup and mandatory `asOf`, not eliminated — a cached fallback can still be wrong.
- **Intent→type mapping can't be tested statically.** The ladder is only as good as the examples in the skill. Budget for expanding the example set after the first real failures.
- **`createRoute` is a pattern, not a captured list.** `/manage/app/content-add-<service>/` was observed on catalog tiles, so routes for real services follow. Custom Code has no service, so its route is a guess — hence `createRouteVerified: false`. Any route emitted without having seen the tile carries that flag.
- **Two extension stores, not one.** The main catalog and the eCommerce collection are different pages with overlapping but non-identical contents and prices. `extensions-pricing` must know which to query from the app type, or it will quote shop prices to blog apps.

---

## Sources

- `ai-output/7-section-type-codenames.md` — the type enum, catalog→type mapping, service table, the server-side binding finding, read-only structural fields and provisioning routes.
- `ai-output/4-structure-backoffice.md` — the per-app instance cap and title limits, the list/detail/categories model, section creation flow.
- `CLAUDE.md` — project context and rules.
- [GoodBarber Extensions](https://www.goodbarber.com/extensions/) — categories, free/paid tiers and prices, accessed 2026-08-13.
- [eCommerce extensions collection](https://www.goodbarber.com/extensions/collections/ecommerce/) — the shop extension list, prices, and which entries create a section, accessed 2026-08-13.
- [Section design (Shop)](https://www.goodbarber.com/help/shop/design-of-your-sections-r89/section-design-a106/) — the shop's section list: products list, collections list, product detail, cart, my account, order; accessed 2026-08-13.
- [Understand app sections and structure](https://www.goodbarber.com/help/organize-your-content-r93/understand-app-sections-and-structure-a34/) — the six section families and the connector model, accessed 2026-08-13.
