# Plan — App Structure Agent

**Status:** planning only. Nothing built yet. This document is the design to approve before writing any skill file.

**Goal (restated):** an agent that reads a plain-English app description and returns the required GoodBarber structure — the section types, the service behind each one, the price, and, where nothing fits, a developer-ready custom-code specification.

**Decisions taken:**

| Question         | Answer                                          |
| ---------------- | ----------------------------------------------- |
| Output format    | One Markdown report with an embedded JSON block |
| Number of skills | Split by family and complexity — 6              |
| Scope            | Structure only — no design, navigation or Home  |

---

## 1. Architecture

```
CLAUDE.md            project rules, GoodBarber background, where outputs go
SYSTEM-PROMPT.md     role, the decision ladder, invariants, refusal rules
   │
   ├── section-routing/       ← always applies: intent → type, owns output schema
   ├── content-sections/      ← the 6 feed types + the service axis
   ├── utility-sections/      ← static pages, forms, links, social, live
   ├── commerce-sections/     ← the Shop product line
   ├── extensions-pricing/    ← free vs paid, plan gating, live store lookup
   └── custom-code-spec/      ← the gap path: developer-ready specification
```

### Why this split

The split follows **where the decisions are**, not where the types are.

| Skill                | Triggers when                                                                                         | Owns                                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `section-routing`    | every request                                                                                         | the type enum, catalog→type map, the decision ladder, the output schema, validation rules                                                        |
| `content-sections`   | request mentions a feed of items — articles, news, blog, photos, video, audio, events, places         | Article / Photo / Video / Sound / Maps / Agenda; service tables; list+detail model; categories; `custom` feed rules                              |
| `utility-sections`   | request mentions a static page, contact, form, link, search, QR, social, storefront link, live stream | About, Contact, Form, Submit, Search, Qrcode, Clickto, Fakeclickto, Custom, Node, Shop, Live, Facebook/Instagram/Twitter, and the auto-added set |
| `commerce-sections`  | request describes selling products, a catalogue, a cart, orders, customer accounts                    | `Commerce*`, `Profile`; the Shop-plan gate; the section-vs-feature rule                                                                          |
| `extensions-pricing` | any section resolves to something billable, or nothing matched                                        | tiers, plan gating, the live goodbarber.com/extensions lookup                                                                                    |
| `custom-code-spec`   | `section-routing` declares a gap                                                                      | the spec template, required detail level, the two worked examples                                                                                |

Rejected alternatives, briefly:

- **One skill.** Loads every type × every service + pricing + spec guidance on every request. Most is irrelevant to any single app, and long context is where type/service confusion starts.
- **One skill per type.** Claude routes to skills by matching description text; thirty descriptions that all read "handles a GoodBarber section" trigger unreliably, and a four-section app pulls in four skills.

The chosen split reflects the real asymmetry: `Article` has 10 services and needs a page of guidance; `Qrcode` has none and needs one line.

---

## 2. The decision ladder

Belongs verbatim in the system prompt.

For each feature the user describes:

**Step 0 — Decompose.** Turn the description into discrete feature intents. Say the decomposition out loud — "a page with news and photos" is two intents.

**Step 1 — Screen or behaviour?** A screen the user navigates to (section) → continue to Step 2. A behaviour layered onto the app or shop (loyalty, discounts, push, analytics, payments, abandoned-cart) → `extensions[]`, then Step 5.

**Step 2 — Type.** Map the intent to exactly one `GBModuleType*`. Match on *intent*, never on the user's noun — users say "newsletter", "wish list", "TikTok", and none are types. No fit → Step 6.

**Step 3 — Service.** Given the type, choose from that type's known services:

- user names a platform they already publish on (WordPress, YouTube, Spotify, Substack…) → that platform's service;
- user has their own API or JSON feed → `custom`;
- user will author inside GoodBarber → `mcms`;
- type has no services → omit.

Platform named but not in the known list → check the site before concluding anything.

**Step 4 — Check `custom` before giving up.** If Step 3 found nothing and the type is one of the six content types, `custom` is available. This step exists because skipping it is the most likely failure mode.

**Step 5 — Price and plan.** Look up billable items live; cite the date. Flag `Commerce*` (Shop plans only) and `Profile` (account-enabled apps only) as gated rather than proposing them silently.

**Step 6 — Gap path.** Reachable only when Steps 2–4 all failed *and* a live lookup found nothing. Emit `status: "gap"` with **both** required outputs:
1. the nearest existing sections, each with an explicit statement of what it *won't* do;
2. a full custom-code specification (`GBModuleTypePlugin`, no service).

Never one or the other — the brief requires both.

**Step 7 — Validate**, then emit.

### Two disclosure rules the agent must never skip

- **`Fakeclickto` is a link, not a section.** TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat produce a branded tile that opens the external app. Someone asking for "a TikTok feed in my app" gets a link and must be told so in the same breath. This is the sharpest expectation mismatch in the catalog, and the type name is the only warning.
- **`Custom` vs `Plugin`.** `Custom` = a web view pointed at a URL (Typeform, JotForm, Tawk.to are this with a preset). `Plugin` = code running inside the app. If the need is "embed this existing web thing", it's `Custom` and no custom-code spec is warranted.

---

## 3. Output format

**One Markdown file, with a JSON block inside it.**

Requirement 3.2 says a developer must be able to build the section after reading the description. That's multi-paragraph prose with headings and a data contract — it doesn't survive being a JSON string value. Requirement 4 asks for "a document". Markdown carries both; the JSON block keeps the machine-readable half intact for a later implementation agent.

### Report structure

```
# App Structure — <app name>
## Summary            what the app is, section count, total monthly cost
## Sections           one ## per section: intent → type → service → price → notes
## Extensions         behaviours with no section of their own
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

---

## 4. Custom-code specification template

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

---

## 5. Validation rules

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
- Section count is reported, not capped. Large counts get a note that the back office reports a per-app instance limit.

---

## 6. Files to create


```
ai-agent/
  CLAUDE.md
  SYSTEM-PROMPT.md
  skills/
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

---

## 7. Open risks

- **eCommerce codenames are partly inferred.** eCommerce extensions are not described very well.
- **Prices drift.** Prices may be out of date or wrong.
- **Intent→type mapping can't be tested statically.** The ladder is only as good as the examples in the skill. Budget for expanding the example set after the first real failures.
- **`createRoute` is a pattern, not a captured list.** `/manage/app/content-add-<service>/` was observed on catalog tiles, so routes for real services follow. Custom Code has no service, so its route is a guess — hence `createRouteVerified: false`. Any route emitted without having seen the tile carries that flag.
- **Two extension stores, not one.** The main catalog and the eCommerce collection are different pages with overlapping but non-identical contents and prices. `extensions-pricing` must know which to query from the app type, or it will quote shop prices to blog apps.

---

## Sources

- section-docs/0-section-type-codenames.md` — the type enum, catalog→type mapping, service table, the server-side binding finding, read-only structural fields and provisioning routes.
- `CLAUDE.md` — project context and rules.
- [GoodBarber Extensions](https://www.goodbarber.com/extensions/) — categories, free/paid tiers and prices, accessed 2026-08-13.
- [eCommerce extensions collection](https://www.goodbarber.com/extensions/collections/ecommerce/) — the shop extension list, prices, and which entries create a section, accessed 2026-08-13.
- [Section design (Shop)](https://www.goodbarber.com/help/shop/design-of-your-sections-r89/section-design-a106/) — the shop's section list: products list, collections list, product detail, cart, my account, order; accessed 2026-08-13.
- [Understand app sections and structure](https://www.goodbarber.com/help/organize-your-content-r93/understand-app-sections-and-structure-a34/) — the six section families and the connector model, accessed 2026-08-13.
