---
name: section-routing
description: The core routing skill for planning a GoodBarber app structure from a plain-English description. Use for every structure-planning request. Owns the complete GBModuleType* codename enum, the catalog-name-to-type mapping, the decision ladder that turns a described feature into a type plus a service, the output document schema, and the validation rules run before emitting. Use when deciding what section a described feature needs, when checking whether a codename is real, or when assembling the final report. Do NOT use to choose a service for a content feed (use content-sections).
---

# Section Routing

## 1. What you are choosing between

A GoodBarber app is a set of **sections**. Every section carries two independent discriminators:

| Field | Answers | Consumed by |
|---|---|---|
| `type` | *What shape is this data, and how is it rendered?* | the native app |
| `service` | *Where does the data come from?* | the server |

They are orthogonal, and conflating them is the classic error. "A blog fed by my WordPress" is not one exotic choice out of a hundred catalog tiles — it is `type: GBModuleTypeArticle` plus `service: wordpress`, two small independent decisions.

This matters because the catalog lies about the size of the problem. Thirteen of those tiles — WordPress, Medium, Substack, Blogger, Squarespace, RSS, WP.com, WMaker, Article custom feeds and more — are all the same type. What separates them is the service axis alone.

> **Read `type` and `service` as two questions, never one.**

### What you are *not* producing

The section JSON in a live app (`gbsettings.sections.<id>`) is a **presentation contract**, and its structural fields are read-only. Sections are created through provisioning routes (`/manage/app/content-add-<service>/`), the data source is bound by a separate server-side record, and neither can be set by writing JSON.

So your output is a **plan of actions**, not a document to paste. Each section you emit carries the route that would create it. An implementation agent, or a human, executes it later.

## 2. The type enum

Codenames, captured from a live back office on 2026-08-12. This is the closed vocabulary — **use these exact strings, and never invent one.**

| Codename                  | Role                                          |
| ------------------------- | --------------------------------------------- |
| `GBModuleTypeArticle`     | Text/article feed (list + detail)             |
| `GBModuleTypePhoto`       | Image gallery                                 |
| `GBModuleTypeVideo`       | Video feed                                    |
| `GBModuleTypeSound`       | Audio / podcast feed                          |
| `GBModuleTypeMaps`        | Geolocated points feed                        |
| `GBModuleTypeAgenda`      | Events / calendar feed                        |
| `GBModuleTypeHome`        | Composable widget landing page (singleton)    |
| `GBModuleTypeNode`        | Menu / sub-section container                  |
| `GBModuleTypeAbout`       | Single static page                            |
| `GBModuleTypeContact`     | Contact details page                          |
| `GBModuleTypeForm`        | Form builder                                  |
| `GBModuleTypeSubmit`      | User content submission                       |
| `GBModuleTypeSearch`      | Cross-section search                          |
| `GBModuleTypeBookmark`    | Favorites (auto-added)                        |
| `GBModuleTypeSettings`    | App settings screen (auto-added)              |
| `GBModuleTypeTos`         | Legal page — Terms / Privacy (auto-added, ×2) |
| `GBModuleTypeProfile`     | User account / profile (account-enabled apps) |
| `GBModuleTypeClickto`     | Real deep link / external link                |
| `GBModuleTypeFakeclickto` | Link-out styled as a native section           |
| `GBModuleTypeCustom`      | External URL / embedded web view              |
| `GBModuleTypePlugin`      | Installed extension or Custom Code section    |
| `GBModuleTypeLive`        | Live audio / live video stream                |
| `GBModuleTypeQrcode`      | QR code scanner                               |
| `GBModuleTypeFacebook`    | Facebook integration                          |
| `GBModuleTypeInstagram`   | Instagram integration                         |
| `GBModuleTypeTwitter`     | X (Twitter) integration                       |
| `GBModuleTypeShop`        | External storefront (Shopify / Amazon / Etsy) |
| `GBModuleTypeUserslist`   | Directory of app users                        |

These types are what was present that day, not a guarantee about today. If a request clearly needs something none of these covers, that is the gap path.

Four of these are **auto-added** to apps and must never be proposed as new sections: `Bookmark`, `Settings`, and `Tos` twice (terms and privacy). `Home` is a **singleton** — one per app, never a second.

## 3. Catalog name → type

When the user names a catalog tile, this is the translation. Grouped by the type each tile actually produces.

| Type | Catalog tiles that produce it |
|---|---|
| `Article` | Articles · WordPress · RSS feeds · Substack · Medium · Squarespace · Article custom feeds · WP.com · Blogger · WMaker |
| `Sound` | Podcasts · Spotify for Podcasters · Spreaker · Ausha · Podcast feeds · Simplecast · Podcast custom feeds · WM Podcast |
| `Video` | Videos · YouTube · Vimeo · Video Podcast feeds · Dailymotion · Video custom feeds · WMaker TV |
| `Fakeclickto` | TikTok · Reddit · WhatsApp · Discord · Threads · Snapchat |
| `Photo` | Photos · Photo custom feeds · Flickr · WM Photos |
| `Agenda` | Events · iCal/vCal · Event custom feeds · WM Events |
| `Custom` | URL · Typeform · Tawk.to · Airtable Form · JotForm |
| `Plugin` | Create with AI (BETA) · Custom Code · RAG Chatbot |
| `Maps` | Map · Kml · Map custom feeds |
| `Shop` | Shopify · Amazon · Etsy |
| `Live` | Live Audio · Live Video |
| `Tos` | Terms and conditions · Privacy policy |
| `About` `Contact` `Form` `Node` `Submit` `Search` `Qrcode` `Clickto` `Home` | About · Contact us · Form · Menu · Submission · Search · QR Code · Link · Home |
| `Facebook` `Instagram` `Twitter` | Facebook · Instagram · X (Twitter) |

**The catalog display name is the wrong index for a user request.** Users don't say "Article custom feeds", they say "photos from my API" or "a newsletter" or "a wish list". Route on intent (§4), and use this table only when a brand name is spoken aloud.

## 4. Intent → type routing

Match the **shape of the data and who owns it**, not the noun.

| What the user describes                                                    | Type                                 | Watch out for                                                           |
| -------------------------------------------------------------------------- | ------------------------------------ | ----------------------------------------------------------------------- |
| A feed of written items the owner updates — blog, news, changelog, guides  | `Article`                            | → `content-sections` for the service                                    |
| A gallery of images                                                        | `Photo`                              | —                                                                       |
| A feed of videos                                                           | `Video`                              | —                                                                       |
| Audio episodes, a podcast, a radio archive                                 | `Sound`                              | Live streaming is `Live`, not `Sound`                                   |
| Places on a map, locations, points of interest                             | `Maps`                               | —                                                                       |
| Events with dates, a calendar, a schedule                                  | `Agenda`                             | —                                                                       |
| One static page — about, credits, legal text, an "info" page               | `About`                              | Not a content section; one non-repeating page                           |
| Address, phone, opening hours                                              | `Contact`                            | —                                                                       |
| Collect structured input from users                                        | `Form`                               | —                                                                       |
| Users propose content for the owner to publish                             | `Submit`                             | Public contribution pipeline, not a private list                        |
| Search across the app's content                                            | `Search`                             | —                                                                       |
| Scan a QR code                                                             | `Qrcode`                             | —                                                                       |
| A grouping screen that leads to other sections                             | `Node`                               | The only nesting the platform has                                       |
| Open an external site or app from the menu                                 | `Clickto`                            | Adds a nav entry, creates no screen                                     |
| Embed an existing web page, form or chat widget                            | `Custom`                             | **Not** `Plugin` — see §6                                               |
| TikTok, Reddit, WhatsApp, Discord, Threads, Snapchat                       | `Fakeclickto`                        | **It's a link.** Mandatory disclosure — §6                              |
| Facebook, Instagram, X                                                     | `Facebook` / `Instagram` / `Twitter` | First-class types, unlike the six above                                 |
| A live radio or live video stream                                          | `Live`                               | —                                                                       |
| Link out to a Shopify / Amazon / Etsy store                                | `Shop`                               | External storefront.                      |
| Landing page aggregating other sections                                    | `Home`                               | Singleton; assemble after the sections it references exist              |
| Users save items **already in the app**                                    | `Bookmark`                           | Auto-added — verify, don't create                                       |

## 5. The decision ladder

The full ladder lives in the system prompt. Condensed, per intent:

```
0. Decompose the description into intents (they become the `intent` fields)
1. Screen or behaviour?  behaviour → extensions[], skip to 6
2. Type      → §4. no fit → run 3 and 4 anyway before conceding
3. Service   → content-sections. platform not listed → service null,
               serviceVerified false, "undetermined". Never search.
4. custom?   → if type is a content type and 3 found nothing, `custom` is available
5. Gap       → only if 2, 3 AND 4 all came up empty.
               one line + alternatives[]. No custom-code spec. Stop.
6. Template  → default unless the description justifies otherwise;
               only open template-choices if it does
7. Validate  → §8, then emit JSON-first
```

**Step 4 gets skipped, and skipping it produces false gaps.** `custom` exists on all six content types and turns most "connect it to my own API" requests into an ordinary matched section.

**An unfamiliar capability is `undetermined`, not a gap — and not a search.** The Extensions store carries far more than the section catalog, and you cannot see it. "It isn't in my tables" does not mean "the platform cannot do this", and it does not license you to go and find out. Say which one it is:

| Situation | Status |
|---|---|
| The platform genuinely has no shape for this — it isn't a feed, a page, a form or a link | `"gap"` |
| It might exist as an extension or a newer connector, but isn't in your tables | `"undetermined"` |

**Step 6 gets *over*-thought rather than skipped.** A template is presentation only and changes nothing about what a section can do, so the default is the right answer for most sections. If the description says nothing about how it should look, take the default and don't open `template-choices` at all.

## 6. Distinctions that change the answer

### `Fakeclickto` vs `Facebook`/`Instagram`/`Twitter`

Facebook, Instagram and X get real types with their own renderers. TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat get `Fakeclickto` — a tile that looks native in the catalog and in the menu, but is a branded link-out to an external app.

**Mandatory disclosure.** A user asking for "a TikTok section" is picturing embedded content and will get a link. Say so in the same sentence as the recommendation. The type name is the platform's only warning.

### `Custom` vs `Plugin`

| | `GBModuleTypeCustom` | `GBModuleTypePlugin` |
|---|---|---|
| What it is | A web view pointed at a URL | Code or an extension running inside the app |
| Typical use | Typeform, JotForm, Tawk.to — all of these are this type with a preset URL | Custom Code sections, RAG Chatbot, Create with AI |
| When to pick it | The thing already exists on the web and just needs embedding | Nothing pre-built fits and behaviour must be written |

Reaching for `Plugin` when `Custom` would do turns a URL field into a development project. Ask whether the thing already exists on the web.

You may name `Plugin` when the user explicitly asks for Custom Code or a RAG Chatbot. You may **not** reach for it to close a gap, and you never describe what the code would do — see §7.

### Feed-backed vs owner-authored

Any section whose service is external has **no "Edit the content" action** — the service owns the items, and the app only reads them. If the user pictures writing posts by hand in GoodBarber, the answer is `mcms`, not a connector.

## 7. Output format

**The JSON block is the report.** Everything else is a frame around it, and the frame is deliberately small — the plan is meant to be read by a person scanning a structure and by an implementation step that parses it, and neither needs a narrative.

Reasoning, disclosures and caveats go in each section's **`notes`** field, where they stay attached to the thing they describe. Prose that restates the JSON is the single biggest source of bloat in this report, and it is a defect.

### Report structure

```
# App Structure — <app name>

<= 2 lines: what the app is, how many sections.

## Plan (JSON)     the fenced block — the main content

## Before you build   (optional, <= 3 lines, omit if empty)
                   only things a human must resolve first:
                   an open question, a prerequisite the user must supply
```

**Hard limits.** Two lines before the JSON, three after. No section-by-section walkthrough. No sources section — you did not browse, so there is nothing to cite. No prices, ever. If a section needs explaining, it needs a `notes` field.

### JSON schema

```json
{
  "appId": null,
  "generatedAt": "YYYY-MM-DD",
  "summary": "One line: what this app is for.",
  "sections": [
    {
      "order": 1,
      "name": "News",
      "intent": "News about the city, pulled from a publisher",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": "rss",
      "serviceVerified": true,
      "catalogEntry": "RSS feeds",
      "template": {
        "list": "GBArticleListTemplateTypeClassic",
        "detail": "GBArticleDetailTemplateTypeClassic"
      },
      "templateVerified": true,
      "notes": "Feed-backed — no 'Edit the content' action; the service owns the items. Templates left at the defaults: the description says nothing about layout, and a public RSS feed's image supply is unreliable."
    },
    {
      "order": 2,
      "name": "My reading list",
      "intent": "Each user keeps a private list of things they want to come back to, including items the app doesn't carry",
      "status": "gap",
      "type": null,
      "typeVerified": true,
      "service": null,
      "serviceVerified": true,
      "catalogEntry": null,
      "template": null,
      "templateVerified": true,
      "notes": "No section type stores per-user, user-created records.",
      "alternatives": [
        {
          "type": "GBModuleTypeBookmark",
          "shortfall": "Saves items already in the app; users cannot add things the app doesn't carry."
        }
      ]
    }
  ],
  "extensions": [
    {
      "name": "Push notifications",
      "createsSection": false,
      "note": "A behaviour layered onto the app; adds no section to the structure."
    }
  ]
}
```

**Field notes**

- **`status`** is one of three:
  - `"matched"` — a type was found. `type` is a non-null codename.
  - `"gap"` — the platform has no shape for this. `type: null`, `alternatives` required, `notes` giving the one-line reason. **No `customCode` field exists.** A gap is named and closed; it is never specified, scoped or designed.
  - `"undetermined"` — the capability may well exist, but not in your tables: an uncaptured codename, a connector for a platform you don't have listed, an extension you can't see. `type: null` where the constant is unknown, no `alternatives`, and a `notes` field saying what's missing and why you didn't guess. This status exists so that "I can't confirm this" never has to masquerade as either a match or a gap — and so that not being able to search is never a reason to invent.
- **`service`** is always present. Emit `null` explicitly for types that take none — never omit the key.
- **`catalogEntry`** is always present, `null` if no tile corresponds.
- **`template`** is an object with **both** a `list` and a `detail` key on matched content sections — the two design slots are chosen independently and a plan naming one is incomplete. `null` (the whole object) on gaps and on non-content types, whose template vocabulary was never captured. A single key may be `null` where its family wasn't captured — `Photo` has no captured detail family. See `template-choices`.
- **`templateVerified: false`** means the template was chosen on a reading of its codename rather than a documented description. Defaults are `true`; most non-defaults are `false`.
- **`notes`** is where reasoning lives. Disclosures, the justification for a non-default template, what an `undetermined` status couldn't confirm — all of it, one or two sentences, attached to the section it concerns rather than narrated in prose.
- **`typeVerified: false`** means *this type being right for this intent* was inferred, not observed. A codename existing in §2 is not the same as having seen it on a live section of the kind you're describing — a strong name match is still a name match.
- There is no `sectionLimit` field. Apps carry a per-app instance cap the back office reports at runtime; you don't assert it and never use it to limit a plan.

## 8. Validation checklist

Run before emitting. Each failure is either a fix or a stated warning — never a silent pass.

- [ ] Every non-null `type` is a verbatim string from §2. Nothing invented. `null` only on `"gap"` or `"undetermined"`.
- [ ] Every `service` key is present, `null` where the type takes none, and otherwise in the known list for **that specific type** or carrying `serviceVerified: false`. `mcms` is not universal — `Photo` has it, `Clickto` does not.
- [ ] Every matched content section carries a `template` object with both `list` and `detail`, each a verbatim string from `template-choices` or an explicit `null`. Nothing invented.
- [ ] Every non-default template has a one-line justification in `notes` quoting the user's description, and `templateVerified: false` unless the template is one GoodBarber documents.
- [ ] Every `status: "gap"` carries `alternatives` and **nothing resembling a custom-code specification** — no design for the missing feature, no implementation sketch, no effort estimate.
- [ ] Every gap passed **all three** checks: no type, no `custom` service, no `GBModuleTypeCustom` web view. Step 4 is the one that gets skipped.
- [ ] Anything that might exist but isn't in the tables is `"undetermined"`, not `"gap"` — and its `notes` says what wasn't captured and why nothing was guessed.
- [ ] Behaviours that create no screen are in `extensions[]`, not `sections[]`.
- [ ] `Home` appears at most once; `Bookmark`, `Settings`, `Tos` are referenced, never created.
- [ ] Every `Fakeclickto` section says in its `notes` that it is a link.
- [ ] Every connector-backed section says in its `notes` that content can't be authored in-app.
- [ ] Section count is reported, not capped.

**Scope checks — each of these is a defect, not a stylistic preference:**

- [ ] **No price, plan tier or cost appears anywhere** in the report, including in `notes`.
- [ ] **Nothing eCommerce.** No store, cart, product, order or `Commerce*` anything. `GBModuleTypeShop` is a link out to an external storefront and is the only shop-shaped section allowed.
- [ ] **Nothing was searched or browsed**, and no URL is cited. No sources section.
- [ ] **The JSON block is the bulk of the output**: at most two lines of prose before it and three after, with no section-by-section walkthrough.

---

*Sources: `section-docs/0-section-type-codenames.md`
