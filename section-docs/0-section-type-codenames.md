# Section Type Code-Names (`GBModuleType*`)

Findings from direct inspection of the ReBook back office (`rebook.goodbarber.app/manage/app/content/` and `/manage/app/content-add/`) on 2026-08-12. All type names below were extracted from the live back-office DOM, not inferred.

## 1. What the `type` field is

Every section object in `gbsettings.sections.<id>` carries a `type` field whose value is a constant like `GBModuleTypeArticle`, `GBModuleTypeSound`, `GBModuleTypePlugin`. It is the **section's class discriminator** — the one field that says *what kind of thing this section is*. Everything else in the JSON (`list`, `detail`, `contentSource`, `template`, `thumbFormat`, …) is interpreted relative to it.

### Why it exists

**1. The app JSON is a polymorphic document.** All sections live in one flat map and share a common envelope (`id`, `title`, `icon`, `list`, `detail`). But an Articles section has `uneAuthorFont`, a Podcasts section has `Play settings`, a Link section has neither. `type` is the tag that tells the renderer which schema branch to apply.

**2. It is stable; the display name is not.** The label in the UI is localized (the app shows `Artigos`, the type is still `GBModuleTypeArticle`) and is marketing-facing, so it can be renamed freely. `type` cannot change without breaking every app already built. This is why it's exposed in Advanced settings at all: the raw editor edits the contract, not the presentation layer.

**4. It decouples the *catalog* from the *data model* (the important one).** The "+ Add a section" catalog shows ~84 entries, but they resolve to only **30 distinct types**. `WordPress`, `Medium`, `Substack`, `Blogger`, `Squarespace`, `RSS feeds`, `WP.com`, `WMaker` and `Article custom feeds` are all `GBModuleTypeArticle` — same section, same renderer. What separates them is a *second, independent* field: `service`. GoodBarber can ship a "new feature" as a catalog tile + a server-side service adapter without touching the native app at all. 

### Why this matters for the AI-integration case study

An agent generating an app must emit `type`, not display names — the type set is the real, closed, finite vocabulary it has to choose from, and it is **30 items, not 120**. That is a dramatically smaller decision space than the catalog implies.

---

## 2. The complete type enum (30)

Extracted from all `GBModuleType*` identifiers present in the back-office markup.

| Code-name                             | Role                                                |
| ------------------------------------- | --------------------------------------------------- |
| `GBModuleTypeArticle`                 | Text/article feed (list + detail)                   |
| `GBModuleTypePhoto`                   | Image gallery                                       |
| `GBModuleTypeVideo`                   | Video feed                                          |
| `GBModuleTypeSound`                   | Audio / podcast feed                                |
| `GBModuleTypeMaps`                    | Geolocated points feed                              |
| `GBModuleTypeAgenda`                  | Events / calendar feed                              |
| `GBModuleTypeHome`                    | The composable widget landing page (singleton)      |
| `GBModuleTypeNode`                    | Menu / sub-section container (nests other sections) |
| `GBModuleTypeAbout`                   | Single static page                                  |
| `GBModuleTypeContact`                 | Contact details page                                |
| `GBModuleTypeForm`                    | Form builder                                        |
| `GBModuleTypeSubmit`                  | User content submission                             |
| `GBModuleTypeSearch`                  | Cross-section search                                |
| `GBModuleTypeBookmark`                | Favorites (auto-added)                              |
| `GBModuleTypeSettings`                | App settings screen (auto-added)                    |
| `GBModuleTypeTos`                     | Legal page — Terms / Privacy (auto-added, ×2)       |
| `GBModuleTypeProfile`                 | User account / profile                              |
| `GBModuleTypeClickto`                 | Real deep link / external link                      |
| `GBModuleTypeFakeclickto`             | Link-out styled as a native section                 |
| `GBModuleTypeCustom`                  | External URL / embedded web view                    |
| `GBModuleTypePlugin`                  | Installed extension or Custom Code section          |
| `GBModuleTypeLive`                    | Live audio / live video stream                      |
| `GBModuleTypeQrcode`                  | QR code scanner                                     |
| `GBModuleTypeFacebook`                | Facebook-specific integration                       |
| `GBModuleTypeInstagram`               | Instagram-specific integration                      |
| `GBModuleTypeTwitter`                 | X (Twitter)-specific integration                    |
| `GBModuleTypeShop`                    | External storefront (Shopify / Amazon / Etsy)       |
| `GBModuleTypeCommerce`                | Native eCommerce (Shop-plan apps only)              |
| `GBModuleTypeCommercealias`           | eCommerce alias/duplicate view                      |
| `GBModuleTypeCommercecollectionslist` | eCommerce collections index                         |

---

## 3. Full catalog → type mapping (84 entries → 30 types)

Every "+ Add a section" tile observed, grouped by the type it actually creates.

| Type | Catalog entries that produce it |
|---|---|
| `Article` (13) | Articles · Wordpress · RSS feeds · Substack · Medium · Squarespace · Article custom feeds · WP.com · Blogger · WMaker |
| `Sound` (10) | Podcasts · Spotify for Podcasters · Spreaker · Ausha · Podcast feeds · Simplecast · Podcast custom feeds · WM Podcast |
| `Video` (8) | Videos · YouTube · Vimeo · Video Podcast feeds · Dailymotion · Video custom feeds · WMaker TV |
| `Fakeclickto` (6) | TikTok · Reddit · Whatsapp · Discord · Threads · Snapchat |
| `Photo` (5) | Photos · Photo custom feeds · Flickr · WM Photos |
| `Agenda` (5) | Events · iCal/vCal · Event custom feeds · WM Events |
| `Custom` (5) | URL · Typeform · Tawk.to · Airtable Form · JotForm |
| `Plugin` (5) | Create with AI (BETA) · Custom Code · RAG Chatbot |
| `Maps` (4) | Map · Kml · Map custom feeds |
| `Shop` (3) | Shopify · Amazon · Etsy |
| `Live` (2) | Live Audio · Live Video |
| `Settings` (2) | Settings (already added) |
| `Tos` (2) | Terms and conditions · Privacy policy |
| `Bookmark` (2) | Favorites (already added) |
| `About` / `Contact` / `Form` / `Node` / `Submit` / `Search` / `Qrcode` / `Clickto` / `Home` (1 each) | About · Contact us · Form · Menu · Submission · Search · QR Code · Link · Home |
| `Facebook` / `Instagram` / `Twitter` (1 each) | Facebook · Instagram · X (Twitter) |

### Two mappings worth flagging

**`Clickto` vs `Fakeclickto`.** Facebook, Instagram and X get first-class types (`Clickto`) with their own renderers. TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat get `Fakeclickto` — a tile that *looks* like a native section in the catalog and in the menu but is really just a branded link-out to an external app or URL. The naming is candid about it. Practical consequence: a user asking for "a TikTok section in my app" gets a link, not embedded content, and the type name is how you know that before building it.

**`Custom` vs `Plugin`.** `Custom` = point a web view at a URL (Typeform, JotForm, Tawk.to are all just this with a preset URL). `Plugin` = an installed extension running inside the app, including Custom Code sections and the RAG Chatbot. `Plugin` is the extensible slot; `Custom` is the escape hatch.

---

## 4. The second axis: `service`

`type` alone does not distinguish extensions with the same `type`, for example, Articles from WordPress. A second, orthogonal discriminator does: **`service`**. Every section carries one, exposed in the back office as a `service-*` CSS class on both catalog tiles and live section rows.

|           | meaning                                                                                                                  | who consumes it    |
| --------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| `type`    | **what shape the data has, and how to render it** — list+detail layout, which fields exist, which design templates apply | the **native app** |
| `service` | **where the data comes from, and how to fetch/normalize it**                                                             | the **server**     |

### The service vocabulary (47)

Grouped by the type they attach to.

| Type | Services |
|---|---|
| `Article` | `mcms` `wordpress` `wordpressdotcom` `rss` `substack` `medium` `squarespace` `blogger` `wmarticle` `custom` |
| `Sound` | `mcms` `anchor` `spreaker` `ausha` `podcast` `simplecast` `wmpodcast` `custom` |
| `Video` | `mcms` `youtube` `vimeo` `dailymotion` `videopodcast` `wmvideo` `custom` |
| `Photo` | `mcms` `flickr` `wmphoto` `custom` |
| `Agenda` | `mcms` `vcalendar` `wmevent` `custom` |
| `Maps` | `mcms` `kml` `custom` |
| `Fakeclickto` | `clicktotiktok` `clicktoreddit` `clicktowhatsapp` `clicktodiscord` `clicktothreads` `clicktosnapchat` |
| `Custom` | `typeform` `tawkto` `airtable` `jotform` *(none)* |
| `Shop` | `shopify` `amazon` `etsy` |
| `Live` | `liveradio` `livevideo` |
| `Plugin` | `aistudio` `rag` *(none = Custom Code)* |
| `Tos` | `classictos` `classicprivacy` |
| `Facebook` / `Instagram` / `Twitter` | `facebook` `clicktoinstagram` `clicktotwitter` |
| `About` / `Form` | `mcms` |
| `Clickto` `Contact` `Node` `Qrcode` `Search` `Submit` | *(none — no external source)* |
**`mcms` = "GoodBarber managed CMS"** — the built-in content editor. It is just one service among many, not a privileged default.

Note `custom` recurs across all six content types — that is the `<Type> custom feeds` family, i.e. "point at your own JSON matching GoodBarber's Content API spec."

---

## 6. Implications for the agentic-AI concept

- **The generation target is small.** An agent chooses among 30 `type` values, not 120 catalog names. This is small enough to enumerate in a system prompt and validate against exhaustively — a closed vocabulary is the difference between generation and hallucination.
- **Two independent decisions, not one.** `type` (structure/rendering) and `service` (data source) are orthogonal. "A blog fed by my WordPress" = `type: Article` + `service: wordpress`.
- **The agent cannot configure a data source by writing JSON.** Since the source binding is server-side, an agent emitting section JSON can set up *structure and design* but must go through a separate API/UI path to bind a feed.
- **Type-to-schema validation is possible.** Since `type` determines which keys are legal, a generated section can be validated statically before it's ever written to the app — no need to render it to find out it's malformed.
- **The catalog display name is the wrong index for a user request.** Users say "TikTok", "wish list", "newsletter". Those map to types only through intent, not string matching — and sometimes map to *nothing* (`Fakeclickto` is a link; a wish list has no type at all and must be `Plugin`). There must be a skill to interpret the user request and select the corresponding `type`.

---

## Sources

- ReBook back office, Structure screen — `https://rebook.goodbarber.app/manage/app/content/` (live section `data-type` attributes), accessed 2026-08-12.
- ReBook back office, Add-a-section catalog — `https://rebook.goodbarber.app/manage/app/content-add/` (catalog tile `section-GBModuleType*` classes), accessed 2026-08-12.
- Catalog tile creation routes (`/manage/app/content-add-<service>/`) and `service-*` icon classes, same page.
- Advanced settings JSON editor widget initialisation options (`canChangeProperty: false`) and read-only field audit, per-section and app-wide (`/manage/settings/apisettings/`), 2026-08-13. Read-only inspection only — no modifications were made or saved.
