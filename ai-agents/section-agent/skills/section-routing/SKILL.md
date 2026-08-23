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

| Codename                              | Role                                          |
| ------------------------------------- | --------------------------------------------- |
| `GBModuleTypeArticle`                 | Text/article feed (list + detail)             |
| `GBModuleTypePhoto`                   | Image gallery                                 |
| `GBModuleTypeVideo`                   | Video feed                                    |
| `GBModuleTypeSound`                   | Audio / podcast feed                          |
| `GBModuleTypeMaps`                    | Geolocated points feed                        |
| `GBModuleTypeAgenda`                  | Events / calendar feed                        |
| `GBModuleTypeHome`                    | Composable widget landing page (singleton)    |
| `GBModuleTypeNode`                    | Menu / sub-section container                  |
| `GBModuleTypeAbout`                   | Single static page                            |
| `GBModuleTypeContact`                 | Contact details page                          |
| `GBModuleTypeForm`                    | Form builder                                  |
| `GBModuleTypeSubmit`                  | User content submission                       |
| `GBModuleTypeSearch`                  | Cross-section search                          |
| `GBModuleTypeBookmark`                | Favorites (auto-added)                        |
| `GBModuleTypeSettings`                | App settings screen (auto-added)              |
| `GBModuleTypeTos`                     | Legal page — Terms / Privacy (auto-added, ×2) |
| `GBModuleTypeProfile`                 | User account / profile (account-enabled apps) |
| `GBModuleTypeClickto`                 | Real deep link / external link                |
| `GBModuleTypeFakeclickto`             | Link-out styled as a native section           |
| `GBModuleTypeCustom`                  | External URL / embedded web view              |
| `GBModuleTypePlugin`                  | Installed extension or Custom Code section    |
| `GBModuleTypeLive`                    | Live audio / live video stream                |
| `GBModuleTypeQrcode`                  | QR code scanner                               |
| `GBModuleTypeFacebook`                | Facebook integration                          |
| `GBModuleTypeInstagram`               | Instagram integration                         |
| `GBModuleTypeTwitter`                 | X (Twitter) integration                       |
| `GBModuleTypeShop`                    | External storefront (Shopify / Amazon / Etsy) |
| `GBModuleTypeUserslist`               | Directory of app users                        |

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
0. Decompose the description into intents, and say the split out loud.
1. Screen or behaviour?  behaviour → extensions[], skip to 5
2. Type      → §4. no fit → 5 (NOT 6 — a missing type is not yet a gap)
3. Service   → content-sections. platform not listed → look it up
4. custom?   → if type is a content type and 3 found nothing, `custom` is available
5. Look up   → search the store before conceding anything
6. Gap       → only if 2, 3, 4 AND 5 all came up empty.
               alternatives[]
7. Template  → template-choices. matched content sections only;
               default unless the description justifies otherwise
8. Validate  → §8, then emit
```

**Two steps get skipped, and both produce false gaps.**

Step 4: `custom` exists on all six content types and turns most "connect it to my own API" requests into an ordinary matched section.

Step 5: an unfamiliar capability is a **lookup, not a gap**. The store carries far more than the section catalog, and it grows. "There is no section for this" does not mean "the platform cannot do this."

Step 7 is the one that gets *over*-thought rather than skipped. A template is presentation only and changes nothing about what a section can do, so the default is the right answer for most sections — see `template-choices` §2.

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

Reaching for `Plugin` when `Custom` would do means writing a custom-code spec for something that needed a URL field. Ask whether the thing already exists on the web.

### Feed-backed vs owner-authored

Any section whose service is external has **no "Edit the content" action** — the service owns the items, and the app only reads them. If the user pictures writing posts by hand in GoodBarber, the answer is `mcms`, not a connector.

## 7. Output format

One Markdown report containing a fenced JSON block.

Prose carries what JSON can't: the reasoning and the disclosures. The JSON block carries what prose can't: a machine-readable plan for a later implementation step.

### Report structure

```
# App Structure — <app name>
## Summary          what the app is, how many sections, total monthly cost
## Plan (JSON)      the fenced block
## Sources          with access dates
```

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
      "name": "Wish list",
      "intent": "Users build a private list of products they want",
      "status": "gap",
      "type": null,
      "typeVerified": true,
      "service": null,
      "serviceVerified": true,
      "catalogEntry": null,
      "template": null,
      "templateVerified": true,
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
      "name": "Loyalty Program",
      "note": "Configured on the shop; adds no section to the structure."
    }
  ]
}
```

**Field notes**

- **`status`** is one of three:
  - `"matched"` — a type was found. `type` is a non-null codename.
  - `"gap"` — no type, no service, no extension. `type: null`, and **both** `alternatives` and `customCode` required.
  - `"undetermined"` — the screen exists in the platform but its codename wasn't captured. `type: null`, no `alternatives` and a `notes` field saying what's missing and why you didn't guess. This status exists so that "I don't know the constant" never has to masquerade as either a match or a gap.
- **`service`** is always present. Emit `null` explicitly for types that take none — never omit the key.
- **`catalogEntry`** is always present, `null` if no tile corresponds.
- **`template`** is an object with **both** a `list` and a `detail` key on matched content sections — the two design slots are chosen independently and a plan naming one is incomplete. `null` (the whole object) on gaps and on non-content types, whose template vocabulary was never captured. A single key may be `null` where its family wasn't captured — `Photo` has no captured detail family. See `template-choices`.
- **`templateVerified: false`** means the template was chosen on a reading of its codename rather than a documented description. Defaults are `true`; most non-defaults are `false`.
- **`typeVerified: false`** means *this type being right for this intent* was inferred, not observed. A codename existing in §2 is not the same as having seen it on a live section of the kind you're describing. The whole `Commerce*` family is `false`, including `Commercecollectionslist` — a strong name match is still a name match.
- There is no `sectionLimit` field. Apps carry a per-app instance cap the back office reports at runtime; you don't assert it and never use it to limit a plan.

## 8. Validation checklist

Run before emitting. Each failure is either a fix or a stated warning — never a silent pass.

- [ ] Every non-null `type` is a verbatim string from §2. Nothing invented. `null` only on `"gap"` or `"undetermined"`.
- [ ] Every `service` key is present, `null` where the type takes none, and otherwise in the known list for **that specific type** or carrying `serviceVerified: false`. `mcms` is not universal — `Photo` has it, `Clickto` does not.
- [ ] Every matched content section carries a `template` object with both `list` and `detail`, each a verbatim string from `template-choices` or an explicit `null`. Nothing invented.
- [ ] Every non-default template has a one-sentence justification quoting the user's description, and `templateVerified: false` unless the template is one GoodBarber documents.
- [ ] Every `status: "gap"` carries `alternatives`.
- [ ] Every gap passed **all four** checks: no type, no `custom` service, no `GBModuleTypeCustom` web view, and an empty store search. Steps 4 and 5 are the ones that get skipped.
- [ ] Every `status: "undetermined"` says in `notes` what wasn't captured and why nothing was guessed.
- [ ] Behaviours that create no screen are in `extensions[]`, not `sections[]`.
- [ ] `Home` appears at most once; `Bookmark`, `Settings`, `Tos` are referenced, never created.
- [ ] Every `Fakeclickto` section says, in prose, that it is a link.
- [ ] Every connector-backed section says, in prose, that content can't be authored in-app.
- [ ] Section count is reported, not capped.
- [ ] Sources listed with access dates.

---

*Sources: `section-docs/0-section-type-codenames.md`
