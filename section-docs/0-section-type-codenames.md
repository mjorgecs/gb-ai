# Section Type Code-Names (`GBModuleType*`)

Findings from direct inspection of the ReBook back office (`rebook.goodbarber.app/manage/app/content/` and `/manage/app/content-add/`) on 2026-08-12. All type names below were extracted from the live back-office DOM, not inferred.

## 1. What the `type` field is

Every section object in `gbsettings.sections.<id>` carries a `type` field whose value is a constant like `GBModuleTypeArticle`, `GBModuleTypeSound`, `GBModuleTypePlugin`. It is the **section's class discriminator** — the one field that says *what kind of thing this section is*. Everything else in the JSON (`list`, `detail`, `contentSource`, `template`, `thumbFormat`, …) is interpreted relative to it.

### Why it exists

**1. The app JSON is a polymorphic document.** All sections live in one flat map and share a common envelope (`id`, `title`, `icon`, `list`, `detail`). But an Articles section has `uneAuthorFont`, a Podcasts section has `Play settings`, a Link section has neither. `type` is the tag that tells the renderer which schema branch to apply — the standard tagged-union pattern. Without it, a consumer reading `sections.78648653` could only guess the shape by probing which keys happen to exist.

**2. The native runtime is not a web app.** GoodBarber apps compile to native iOS/Android. The `GB` prefix and `PascalCase` suffix are Objective-C/Cocoa naming convention (no namespaces in ObjC, so every symbol carries a vendor prefix — `NSString`, `UIView`, `GBModuleType…`). These constants are almost certainly a real `enum` in the native SDK, and the back office serializes that enum straight into the JSON. The code-name isn't back-office jargon leaking out — it's the **native SDK's own vocabulary**, and the JSON is the wire format between them.

**3. It is stable; the display name is not.** The label in the UI is localized (your app shows `Artigos`, the type is still `GBModuleTypeArticle`) and is marketing-facing, so it can be renamed freely. `type` cannot change without breaking every app already built. This is why it's exposed in Advanced settings at all: the raw editor edits the contract, not the presentation layer.

**4. It decouples the *catalog* from the *data model* (the important one).** The "+ Add a section" catalog shows ~84 entries, but they resolve to only **30 distinct types**. `WordPress`, `Medium`, `Substack`, `Blogger`, `Squarespace`, `RSS feeds`, `WP.com`, `WMaker` and `Article custom feeds` are all `GBModuleTypeArticle` — same section, same renderer. What separates them is a *second, independent* field: `service` (see §5). GoodBarber can ship a "new feature" as a catalog tile + a server-side service adapter without touching the native app at all. The catalog is a **product surface**; `type` is the **engineering surface**.

### Why this matters for the AI-integration case study

An agent generating an app must emit `type`, not display names — the type set is the real, closed, finite vocabulary it has to choose from, and it is **30 items, not 120**. That is a dramatically smaller decision space than the catalog implies. The corollary is that the agent's job splits cleanly in two:

1. pick one of 30 `type` values (structural decision), then
2. fill in `contentSource` (integration decision).

Most of what looks like "which of 120 features do I want?" is actually step 2. See §4.

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
| `GBModuleTypeFakeclickto`             | Link-out styled as a native section (see §3)        |
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

The three `Commerce*` types and `Profile` never appear in the ReBook catalog — they belong to the Shop product line and to account-enabled apps respectively. They are in the enum but not offered in this app's plan.

### Verified against the live app

The ReBook sections carry exactly these values in their `data-type` attribute:

| Section | `type` |
|---|---|
| Artigos | `GBModuleTypeArticle` |
| Notícias | `GBModuleTypeArticle` |
| Podcasts | `GBModuleTypeSound` |
| Gatos | `GBModuleTypePlugin` |
| Lista de desejos | `GBModuleTypePlugin` |
| Favorites | `GBModuleTypeBookmark` |
| Terms and conditions of sale | `GBModuleTypeTos` |
| Privacy policy | `GBModuleTypeTos` |
| Settings | `GBModuleTypeSettings` |
| Home | `GBModuleTypeHome` |

Note `Notícias` (an RSS section) and `Artigos` (a native content section) share one type — the difference lives in the `service` axis (§5). Both Custom Code sections are `GBModuleTypePlugin`, i.e. Custom Code is not its own type, it's an instance of the extension type.

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

**`Clickto` vs `Fakeclickto`.** Facebook, Instagram and X get first-class types with their own renderers. TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat get `Fakeclickto` — a tile that *looks* like a native section in the catalog and in the menu but is really just a branded link-out to an external app or URL. The naming is candid about it. Practical consequence: a user asking for "a TikTok section in my app" gets a link, not embedded content, and the type name is how you know that before building it.

**`Custom` vs `Plugin`.** `Custom` = point a web view at a URL (Typeform, JotForm, Tawk.to are all just this with a preset URL). `Plugin` = an installed extension running inside the app, including Custom Code sections and the RAG Chatbot. `Plugin` is the extensible slot; `Custom` is the escape hatch.

---

## 5. The second axis: `service`

`type` alone does not distinguish Articles from WordPress. A second, orthogonal discriminator does: **`service`**. Every section carries one, exposed in the back office as a `service-*` CSS class on both catalog tiles and live section rows.

### Verified on the live app

| Section                   | `type`                | `service`        |
| ------------------------- | --------------------- | ---------------- |
| Artigos (native CMS blog) | `GBModuleTypeArticle` | `mcms`           |
| Notícias (RSS feed)       | `GBModuleTypeArticle` | `rss`            |
| Podcasts                  | `GBModuleTypeSound`   | `mcms`           |
| Terms and conditions      | `GBModuleTypeTos`     | `classictos`     |
| Privacy policy            | `GBModuleTypeTos`     | `classicprivacy` |
| Gatos / Lista de desejos  | `GBModuleTypePlugin`  | *(none)*         |

**`mcms` = "GoodBarber managed CMS"** — the built-in content editor. It is just one service among many, not a privileged default. "Articles" the catalog tile is really `Article` + `mcms`.

### The two axes are genuinely independent

| | meaning | who consumes it |
|---|---|---|
| `type` | **what shape the data has, and how to render it** — list+detail layout, which fields exist, which design templates apply | the **native app** |
| `service` | **where the data comes from, and how to fetch/normalize it** | the **server** |

The 84 catalog entries are a sparse grid of (30 types × 47 services). WordPress and RSS are the *same point on the type axis*, different points on the service axis.

### Where the WordPress URL actually lives — not in the section JSON

This is the part that surprised me, and it invalidates the obvious guess. I dumped the full raw JSON for both `Artigos` and `Notícias` and diffed them:

- They share **44 of 46 keys**. The only two keys unique to Artigos are `infosContentType` and `subsections` — cosmetic/taxonomy, nothing to do with sourcing.
- `contentSource` on **both** contains exactly one key, `url`, and both values are the *same internal relative path shape*: `/front/get_items/{appId}/{sectionId}/`.
- Scanning both objects recursively for any absolute `http(s)://` URL returns **zero results**. The RSS feed address is not in the section JSON at all.

So the native app never talks to WordPress or to an RSS publisher. Every section — native or third-party — reads from GoodBarber's own normalized endpoint, keyed only by `appId` and `sectionId`. The service adapter runs **server-side**: it fetches the WordPress/RSS/YouTube source on a schedule, normalizes it into GoodBarber's item schema, and serves it at the same internal URL the built-in CMS uses.

```
[WordPress]──┐
[RSS]────────┼─→ server-side `service` adapter ─→ /front/get_items/{app}/{section}/ ─→ native app
[mcms CMS]───┘        (normalizes to one item schema)         (identical for all)
```

**Consequences worth internalizing:**

- The section JSON is a **pure rendering contract**. It describes presentation, not data acquisition. Editing it can never change where content comes from.
- The source binding is a **separate server-side record** keyed by section id. That's why the RSS feed URL is edited in *Settings*, not in Advanced settings — it isn't part of this document.
- This is why **feed-backed sections have no "Edit the content" action** (noted in `4-structure-backoffice.md` §2): the service owns the items, the app only reads them.
- It also explains **why every service produces a usable section**. The adapter guarantees a uniform item schema, so the native renderer needs no per-service knowledge whatsoever.

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

Note `custom` recurs across all six content types — that is the `<Type> custom feeds` family, i.e. "point at your own JSON matching GoodBarber's Content API spec."

---

## 6. Implications for the agentic-AI concept

- **The generation target is small.** An agent chooses among 30 `type` values, not 120 catalog names. This is small enough to enumerate in a system prompt and validate against exhaustively — a closed vocabulary is the difference between generation and hallucination.
- **Two independent decisions, not one.** `type` (structure/rendering) and `service` (data source) are orthogonal. "A blog fed by my WordPress" = `type: Article` + `service: wordpress`. An agent that conflates the axes treats 10 Article variants as 10 unrelated choices; an agent that separates them makes one 30-way choice and one 47-way choice, each independently validatable. Most of what looks like feature selection is really service selection.
- **The agent cannot configure a data source by writing JSON.** Since the source binding is server-side (§5), an agent emitting section JSON can set up *structure and design* but must go through a separate API/UI path to bind a feed. This is a hard architectural boundary the integration design has to respect — it likely means two distinct tool calls, not one JSON write.
- **Type-to-schema validation is possible.** Since `type` determines which keys are legal, a generated section can be validated statically before it's ever written to the app — no need to render it to find out it's malformed.
- **The catalog display name is the wrong index for a user request.** Users say "TikTok", "wish list", "newsletter". Those map to types only through intent, not string matching — and sometimes map to *nothing* (`Fakeclickto` is a link; a wish list has no type at all and must be `Plugin`). The `app-structure` skill's routing table (§3) is doing exactly this job and should be keyed on these type constants.
- **Sibling naming conventions.** The same convention runs through the rest of the JSON: `GBArticleListTemplateTypeVisualCardCondensed` (design template), `GBThumbFormat169` (thumbnail aspect ratio). The design vocabulary is a second closed enum, worth extracting the same way for the `app-design` skill.

---

## 7. Can structure be changed by editing the JSON? No — and the lock is deliberate

Tested directly on the Advanced settings editor, both the per-section view (`renderJson(<id>)`) and the app-wide view (`Settings > Advanced settings`).

### The editor is values-only

The back office initialises the JSON editor widget with the option **`canChangeProperty: false`**. Consequences, all verified in the live DOM:

- All **539 property-name inputs are `readonly`** — zero are editable. You cannot rename a key, and you cannot create one.
- The widget's `Add property` / `Add object` / `Add array` / `delete` controls exist in the markup (1342 and 4993 instances respectively) but every one sits inside a container set to `display: none`. They are shipped-but-suppressed.
- The per-section editor is scoped by a hidden `json_settings_id` field to a **single section id**. It cannot address a sibling section, let alone a new one.

**A new section would be a new key under `gbsettings.sections`. Adding keys is exactly what the editor forbids.** So: no, you cannot add a section by editing JSON.

### Which values are locked tells you what the JSON is *for*

Of 539 editable value fields, exactly **8 are read-only** — and they are precisely the structural/identity ones:

| Locked field | Why it must be |
|---|---|
| `type` | Changing it would mean the section is a different class of object entirely |
| `id` | Server-assigned primary key |
| `title` (×2) | Owned by Settings; drives the menu label |
| `contentSource.url` (×2) | The server-side data binding (§5) |
| `ids`, `category_index` | Taxonomy references to server-side records |

The other 531 fields — fonts, colours, `template`, `thumbFormat`, `thumbPosition`, padding, toolbars — are all freely editable.

That split *is* the design intent, stated in code: **the JSON editor exposes the presentation axis and locks the structural axis.** It's a design tool that happens to look like a data editor. §5 found the same boundary from the other direction — the source binding isn't in this document either.

### So how *does* structure change?

Through dedicated server endpoints that the UI calls, never through the document:

| Operation | Mechanism |
|---|---|
| Add a section | `GET /manage/app/content-add-<service>/` — provisions an id, a service record, and a menu link server-side |
| Reorder | `/manage/section/orderSections/` |
| Delete | `/manage/content/controlDeleteSection/` |
| Edit presentation | Advanced settings JSON (staged, then published) |

Note also that JSON edits are **staged, not live** — the back office showed *"You have 84 modifications ready to be published in your app"*. Structure and design changes both queue behind an explicit publish step.

### Why this matters for the AI-integration concept

This is the single most important architectural constraint found so far, because the obvious agent design is wrong:

> ❌ "The agent writes a JSON document describing the app; the platform renders it."

That cannot work. The JSON is not the source of truth for structure — it's a projection of server-side state, with the structural fields deliberately frozen. An agent that builds an app must:

1. **Call provisioning endpoints** to create/order/delete sections (structure),
2. **Bind data sources** through a separate service-configuration path (§5),
3. **Write JSON** only for presentation,
4. **Publish** to make any of it live.

Four distinct capabilities, three of which are *not* JSON authoring. The tool surface an agent needs is therefore an **API/action set**, not a document schema — and the design work is defining those actions, not defining a JSON format.

---

## Sources

- ReBook back office, Structure screen — `https://rebook.goodbarber.app/manage/app/content/` (live section `data-type` attributes), accessed 2026-08-12.
- ReBook back office, Add-a-section catalog — `https://rebook.goodbarber.app/manage/app/content-add/` (catalog tile `section-GBModuleType*` classes), accessed 2026-08-12.
- Advanced settings JSON editor — full raw section objects for `Artigos` (id 78648540, `service: mcms`) and `Notícias` (id 78796277, `service: rss`), captured and diffed on 2026-08-12.
- Catalog tile creation routes (`/manage/app/content-add-<service>/`) and `service-*` icon classes, same page.
- Advanced settings JSON editor widget initialisation options (`canChangeProperty: false`) and read-only field audit, per-section and app-wide (`/manage/settings/apisettings/`), 2026-08-13. Read-only inspection only — no modifications were made or saved.
- Prior report: `ai-output/4-structure-backoffice.md`.
