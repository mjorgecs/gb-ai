# Plan — App Structure Agent

**Status:** planning only. Nothing built yet. This document is the design to approve before writing any skill file.

**Goal (restated):** an agent that reads a plain-English app description and returns the required GoodBarber structure — the section types, the service behind each one, the price, and, where nothing fits, a developer-ready custom-code specification.

**Decisions taken (2026-08-13):**

| Question | Answer |
|---|---|
| Output format | One Markdown report with an embedded JSON block |
| Number of skills | 5, split by family and complexity |
| Scope | Structure only — no design, navigation or Home |
| Catalog source | Static tables in the skills; live web lookup only for gaps |

---

## 1. Three corrections to the brief

These change the design, so they come first.

### 1.1 The output is a provisioning plan, not a `gbsettings` document

The example JSON in the prompt is shaped like `gbsettings.sections` — `appId` at the top, sections keyed by index. But `7-section-type-codenames.md` §7 established that this document cannot create structure:

- the JSON editor runs with `canChangeProperty: false`, so no key can be added — and a new section *is* a new key;
- of 539 fields, the 8 read-only ones are exactly `type`, `id`, `title`, `contentSource.url`, `ids`, `category_index` — every structural field;
- sections are actually created by `GET /manage/app/content-add-<service>/`.

So the agent must emit **actions to perform**, not a document to paste. Same JSON shape, different meaning — and each section should carry the `content-add-<service>` route that would create it. This is the difference between a plan that can be executed later by an implementation agent and one that looks executable but isn't.

### 1.2 `baseSource` doesn't live where the example puts it

§5 of the same report: the RSS URL is **not** in the section JSON. `contentSource.url` on both `Artigos` (mcms) and `Notícias` (rss) is the same internal path `/front/get_items/{appId}/{sectionId}/`, and a recursive scan for any `http(s)://` in either object returned zero results. The feed address is a separate server-side record, edited in Settings.

Keep the field — the user needs to know a source is required and what to point it at — but move it into its own `sourceBinding` object flagged as a **second, separate step**. Otherwise the output implies "write this URL into the section JSON", which cannot work.

### 1.3 The Photos case in your example is not actually a gap

Your walkthrough concludes that "a photos section linked to an api with images" has no match and falls to custom code. It has an exact match: `GBModuleTypePhoto` + service `custom` — the *Photo custom feeds* tile, documented as "point at your own JSON matching GoodBarber's Content API spec."

This matters more than one wrong example. `custom` recurs across all six content types (`Article`, `Sound`, `Video`, `Photo`, `Agenda`, `Maps`) and is the single most-missed escape hatch in the whole catalog. An agent that forgets it will declare a gap on most "connect it to my API" requests and generate custom-code specs nobody needed. **Checking `custom` on the matched type is a mandatory step before any gap is declared.**

The skill needs a *real* gap example instead. A good one: "users can save products to a wish list they build themselves" — no type in the enum models user-owned mutable collections (`Bookmark` is auto-added and read-only over existing items), so it genuinely resolves to `GBModuleTypePlugin` + custom code. Convenient, since `ai-output/lista-desejos-custom-code/` already exists as the worked answer.

*(Minor: the example prompt says the guide works in New York, the app is about Barcelona, and the news is about New York. I'll normalise it to New York throughout.)*

---

## 2. Architecture

```
CLAUDE.md            project rules, GoodBarber background, where outputs go
SYSTEM-PROMPT.md     role, the decision ladder, invariants, refusal rules
   │
   ├── section-routing/       ← always applies: intent → type, owns output schema
   ├── content-sections/      ← the 6 feed types + the 47-service axis
   ├── utility-sections/      ← the other 24 types, mostly zero-config
   ├── extensions-pricing/    ← free vs paid, plan gating, live store lookup
   └── custom-code-spec/      ← the gap path: developer-ready specification
```

### Why this split (your Question 2)

The split follows **where the decisions are**, not where the types are.

| Skill | Triggers when | Owns | Rough size |
|---|---|---|---|
| `section-routing` | every request | the 30-type enum, catalog→type map, the decision ladder, the output schema, validation rules | large, always loaded |
| `content-sections` | request mentions any feed of items — articles, news, blog, photos, video, audio, events, places | Article / Photo / Video / Sound / Maps / Agenda; the full service table for each; list+detail model; categories; `custom` feed rules | large |
| `utility-sections` | request mentions a static page, contact, form, link, search, QR, social, storefront, live stream | About, Contact, Form, Submit, Search, Qrcode, Clickto, Fakeclickto, Custom, Node, Shop, Live, Facebook/Instagram/Twitter, and the auto-added set | medium |
| `extensions-pricing` | any section resolves to something billable, or nothing matches | free/paid tiers, Shop-plan gating for `Commerce*`, `Profile` account gating, the live goodbarber.com/extensions lookup | small |
| `custom-code-spec` | `section-routing` declares a gap | the spec template, the level of detail required, the two worked examples in `ai-output/` | medium |

Rejected alternatives, briefly:

- **One skill.** Loads ~30 types × 47 services + pricing + spec guidance on every request. Most of it is irrelevant to any single app, and long context is where type/service confusion starts.
- **One skill per type (~30).** Claude routes to skills by matching the description text. Thirty descriptions that all read "handles a GoodBarber section" trigger unreliably, and a four-section app would pull in four skills. The catalog's own shape argues against it too: 84 tiles collapse to 30 types, and 13 of those tiles are one type.

The chosen split reflects the real asymmetry: `Article` alone has 10 services and needs a page of guidance; `Qrcode` has none and needs one line.

---

## 3. The decision ladder

This is the core algorithm, and it belongs verbatim in the system prompt.

For each feature the user describes:

**Step 0 — Decompose.** Turn the description into discrete feature intents. One intent ≈ one section. Say so explicitly, because "a page with news and photos" is two sections.

**Step 1 — Type.** Map the intent to exactly one of the 30 `GBModuleType*` values. Match on *intent*, never on the user's noun — users say "newsletter", "wish list", "TikTok", and none of those are types. If no type fits, go to Step 5.

**Step 2 — Service.** Given the type, choose from that type's service list only (the §5 table is a whitelist, not a suggestion):

- user names a platform they already publish on (WordPress, YouTube, Spotify, Substack…) → that platform's service;
- user has their own API or JSON feed → `custom`;
- user will author the content inside GoodBarber → `mcms`;
- type has no services → omit the field.

**Step 3 — Check `custom` before giving up.** If Step 2 found no service but the type is one of the six content types, `custom` is available. This step exists because skipping it is the most likely failure mode (§1.3).

**Step 4 — Price and plan.** Annotate free/paid. Flag `Commerce*` (Shop plans only) and `Profile` (account-enabled apps only) as unavailable rather than proposing them silently.

**Step 5 — Gap path.** Only reachable when Steps 1–3 all failed. Emit `status: "gap"` and produce **both** required outputs:
  1. the nearest existing sections, with an explicit statement of what each one *won't* do;
  2. a full custom-code specification (`GBModuleTypePlugin`, no service) per §6.

  Never one or the other — the brief requires both.

**Step 6 — Validate** (§5), then emit.

### Two disclosure rules the agent must never skip

- **`Fakeclickto` is a link, not a section.** TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat produce a branded tile that opens the external app. A user asking for "a TikTok feed in my app" is going to get a link and must be told so in the same breath. This is the sharpest expectation mismatch in the catalog and the type name is the only warning.
- **`Custom` vs `Plugin`.** `Custom` = a web view pointed at a URL (Typeform, JotForm, Tawk.to are this with a preset). `Plugin` = code running inside the app. If the user's need is "embed this existing web thing", it's `Custom` and no custom-code spec is warranted.

---

## 4. Output format (your Question 1)

**One Markdown file, with a JSON block inside it.**

The reasoning: requirement 3.2 says a developer must be able to build the section after reading the description. That is multi-paragraph prose with headings and a data contract — it does not survive being a JSON string value. Meanwhile requirement 4 asks for "a document". Markdown carries both; the JSON block keeps the machine-readable half intact for a later implementation agent to consume.

### Report structure

```
# App Structure — <app name>
## Summary                  what the app is, how many sections, total cost
## Sections                 one ## per section: intent → type → service → price → notes
## Gaps                     for each gap: alternatives table + full custom-code spec
## Validation               limits checked, warnings raised
## Plan (JSON)              the fenced block below
## Sources
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
      "service": "rss",
      "catalogEntry": "RSS feeds",
      "createRoute": "/manage/app/content-add-rss/",
      "sourceBinding": {
        "required": true,
        "kind": "feedUrl",
        "suggested": "https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml",
        "note": "Bound server-side via section Settings. Not part of the section JSON."
      },
      "pricing": { "tier": "free" },
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
          "service": null,
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
      "pricing": { "tier": "free" }
    }
  ],
  "validation": {
    "sectionCount": 4,
    "sectionLimit": 120,
    "warnings": []
  }
}
```

Changes from your example, and why:

| Your field | Change | Reason |
|---|---|---|
| `sections` as `{"1": {...}}` | array with `order` | order is data, not a key; keys were already index-like |
| `baseSource` | `sourceBinding` object | separate provisioning step, not a JSON field (§1.2) |
| `options: [(...), "customCode": "..."]` | `alternatives[]` + `customCode{}` | the tuple/string mix isn't valid JSON and conflates the two required answers |
| `"type": none` | `"type": null` + `"status"` | `none` is Python; `status` makes the gap explicit rather than inferred from nulls |
| — | `createRoute` | makes the plan executable (§1.1) |
| `"price": "free"` | `pricing: {tier, extension?, price?}` | paid extensions need a name and an amount |

---

## 5. Validation rules

Run before emitting; every failure is either a fix or a stated warning.

- `type` ∈ the 30-value enum. No invented codenames, ever.
- `service` ∈ the allowed list for that specific type. `mcms` is *not* universal — `Photo` has it, `Clickto` does not.
- total sections ≤ **120** (platform cap).
- section `name` ≤ **32** characters.
- `Home` is a singleton — never propose creating a second one.
- `Bookmark`, `Settings`, `Tos` (×2) are auto-added — reference them, never create them.
- `Commerce`, `Commercealias`, `Commercecollectionslist` → Shop plans only; `Profile` → account-enabled apps only. Flag, don't silently emit.
- every `status: "gap"` carries **both** `alternatives` and `customCode`.
- every `service` that fetches externally has a `sourceBinding`.

---

## 6. Custom-code specification template

What makes it "detailed enough for a developer" — required headings, in order:

1. **Purpose** — one paragraph: what the section does and who uses it.
2. **Screens and flow** — every screen, every transition, what the user sees first.
3. **Data model** — entities, fields, types, which are required.
4. **External contract** — endpoint, method, auth, request and response shapes with a real example payload. If there is no external API, say so and specify local persistence instead.
5. **Rendering** — the HTML/CSS/JS structure inside the `GBModuleTypePlugin` custom-code section: containers, list item markup, loading and empty states.
6. **State and persistence** — what survives a reload, what doesn't, and where it lives.
7. **GoodBarber integration points** — how it is opened from navigation, deep links, which theme variables it should inherit.
8. **Edge cases** — empty result, network failure, slow response, unsupported content.
9. **Acceptance criteria** — a numbered checklist a developer can tick off.

Reference implementations already in the repo: `ai-output/gatos-custom-code/index.html` and `ai-output/lista-desejos-custom-code/index.html`. The skill should point at these as the target shape and level of finish.

---

## 7. Files to create

```
ai-agent/
  agent-app-structure/
    CLAUDE.md
    SYSTEM-PROMPT.md
    skills/
      section-routing/SKILL.md
      content-sections/SKILL.md
      utility-sections/SKILL.md
      extensions-pricing/SKILL.md
      custom-code-spec/SKILL.md
    examples/
      01-tour-guide.md
      02-wish-list-gap.md
      03-social-traps.md
```

**Reconciliation needed.** `ai-agent/skills/` already holds `app-structure`, `app-design` and `app-extensions`. The new `section-routing` + `content-sections` + `utility-sections` trio overlaps `app-structure`, and `extensions-pricing` overlaps `app-extensions`. Two options — decide before step 1:

- **(a) Supersede** — the new agent's skills replace `app-structure` and `app-extensions`; `app-design` stays untouched and out of scope.
- **(b) Fork** — build under `agent-app-structure/` as a clean second implementation, compare, then merge.

(a) is tidier; (b) preserves whatever is already working. I did not read those three files, since the prompt restricted reading to CLAUDE.md, `4-structure-backoffice.md` and `7-section-type-codenames.md` — so this call is yours.

---

## 8. Build order

1. **Reconciliation decision** (above) — blocks everything else.
2. **`section-routing/SKILL.md`** — the enum, the catalog→type map, the ladder, the output schema, the validation rules. Everything else hangs off this.
3. **`content-sections/SKILL.md`** — the six feed types, service tables, `custom` rules, list/detail and categories model.
4. **`utility-sections/SKILL.md`** — the remaining types, with the `Fakeclickto` and `Custom`-vs-`Plugin` disclosure rules.
5. **`extensions-pricing/SKILL.md`** — tiers, plan gating, when to hit the live store.
6. **`custom-code-spec/SKILL.md`** — the §6 template plus the two worked examples.
7. **`SYSTEM-PROMPT.md` and `CLAUDE.md`** — written last, once the skills have settled.
8. **Run the three test cases** (§9) and fix what breaks.

---

## 9. Test cases

**A — Everything matches** (your example, corrected). Tour-guide app: news, photos from an API, map, info page.
Expected: `Article`+`rss`, `Photo`+`custom` (**not** a gap — this is the §1.3 check), `Maps`+`mcms`, `Article`+`mcms`. Four sections, all free, one `sourceBinding` on each of the first two.

**B — Genuine gap.** "Users can save products to a wish list and reorder it."
Expected: `status: "gap"`; `Bookmark` offered as the near miss with its shortfall stated; a full custom-code spec.

**C — Traps.** "A TikTok feed, an AI chatbot that answers from my PDFs, and a Shopify store."
Expected: `Fakeclickto` + explicit "this is a link, not a feed"; `Plugin`+`rag` flagged **paid, $35–55/month**; `Shop`+`shopify`. Case C is the one that catches an agent that pattern-matches on brand names.

---

## 10. Open risks

- **Prices drift.** The store is ~190 extensions and the figures above came from one fetch today. The skill should cite prices as "as of <date>, verify" rather than assert them.
- **The 47-service table is from one app's back office.** ReBook's plan doesn't expose `Commerce*` or `Profile`, so their service lists are unverified. Mark them as such.
- **`createRoute` is a pattern, not a captured list.** `/manage/app/content-add-<service>/` was observed on catalog tiles, so routes for real services (`rss`, `shopify`…) follow. Custom Code has *no* service, so its route is a guess — hence `createRouteVerified: false` in the schema. Any route the agent emits without having seen the tile should carry that flag.
- **Intent→type mapping is the hard part and can't be tested statically.** The ladder is only as good as the examples in the skill. Budget for expanding the example set after the first real failures.
- **One intent ≠ one section, always.** "A shop with a loyalty card" is a section plus an extension, not two sections. Step 0 needs a rule for this and currently doesn't have one — worth resolving during step 2 of the build.

---

## Sources

- `ai-output/7-section-type-codenames.md` — the 30-type enum (§2), catalog→type mapping (§3), the 47-service table and the server-side binding finding (§5), the read-only structural fields and provisioning routes (§7).
- `ai-output/4-structure-backoffice.md` — the 120-section cap and title limits (§8), the list/detail/categories model (§5), section creation flow (§7).
- `CLAUDE.md` — project context and rules.
- [GoodBarber Extensions](https://www.goodbarber.com/extensions/) — ~190 extensions, 8 categories, free/paid tiers and prices, accessed 2026-08-13.
- [Understand app sections and structure](https://www.goodbarber.com/help/organize-your-content-r93/understand-app-sections-and-structure-a34/) — the six section families and the connector model, accessed 2026-08-13.
