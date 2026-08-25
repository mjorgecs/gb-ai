---
name: template-choices
description: "Choose the design template for a GoodBarber content section once its type and service are already decided. Owns the list/detail two-slot model, the default-first rule, the template vocabulary for Article, Sound, Video, Photo, Agenda and Maps, and the signals in a user's description that justify leaving the default. Use when a plan needs a template value, when the user describes a look (magazine, immersive, grid, photo-heavy, minimal, store locator, split map), or when deciding whether a described feed has enough imagery to carry a visual layout. Do NOT use to pick the section type (use section-routing) or the data source (use content-sections)."
---

# Template Choices

`section-routing` decided the **type**. `content-sections` decided the **service**. What remains is the **template** — how the section is drawn.

A template is a pure presentation choice. It changes nothing about what the section can hold or where its data comes from, which is why it is the last decision and the cheapest one to get wrong. It is also the decision with the weakest evidence behind it, so this skill is built to make a **defensible default** the normal answer and a deviation the exception.

## 1. Two slots, not one

Every content section is designed in **two independent halves**, and a plan that names only one is incomplete:

| Slot | What it draws | Back office label |
|---|---|---|
| **List** | The feed — every item | "List of articles" → *Edit the design* |
| **Detail** | One item, opened from the list | "Article page" → *Edit the design* |

Each half has its own template family, its own codename prefix, and its own default. Emit both.

### Family prefixes

| Type | List family | Detail family |
|---|---|---|
| `GBModuleTypeArticle` | `GBArticleListTemplateType…` | `GBArticleDetailTemplateType…` |
| `GBModuleTypeVideo` | `GBVideoListTemplateType…` | `GBVideoDetailTemplateType…` |
| `GBModuleTypeSound` | `GBSoundListTemplateType…` | `GBSoundContentTemplateType…` |
| `GBModuleTypeAgenda` | `GBEventListTemplateType…` | `GBEventContentTemplateType…` |
| `GBModuleTypeMaps` | `GBMapsListTemplateType…` | `GBMapsContentTemplateType…` **and** `GBMapsDetailTemplateType…` |
| `GBModuleTypePhoto` | `GBPhotoListTemplateType…` | *none captured* |

**Three irregularities, and none of them may be smoothed over.**

- The detail family is called `Detail` on Article, Video and Maps, and `Content` on Sound, Agenda and Maps. Never translate one into the other — `GBSoundDetailTemplateType…` does not exist.
- `Maps` has **both** a `Content` and a `Detail` family in the capture. Why there are two is not known. Emit the `Content` value, and add a `notes` line saying a third family exists and wasn't understood.
- `Photo` has **no captured detail family**. Emit `"detail": null` with a note that the family wasn't captured — not that it doesn't exist.

**This skill covers the six content types only.** For every other type — `About`, `Contact`, `Form`, `Node`, `Home`, `Live`, `Shop`, `Custom`, `Plugin`, the social types — no template vocabulary has been captured. Emit `"template": null` with `templateVerified: false` and say so. Menu (`Node`) and section headers do have template pickers in the back office; their codenames are simply not in hand. **Never invent one.**

## 2. The default-first rule

> **The default template is the answer unless the description gives a positive reason to leave it.**

This is the rule this skill exists to enforce. The defaults are what GoodBarber ships, what its back office pre-selects, and what the platform's own design system is tuned around. An agent that picks an exotic template because it sounds impressive produces a plan that looks confident and is unjustifiable — and templates are the one axis a user can change later in two clicks, so an unnecessary deviation costs more than it buys.

| Family                                 | Default    |
| -------------------------------------- | ---------- |
| `GBArticleListTemplateTypeEnriched`    | Enriched   |
| `GBArticleDetailTemplateTypeToolBarUp` | ToolBarUp  |
| `GBVideoListTemplateTypeVisualCard`    | VisualCard |
| `GBVideoDetailTemplateTypeClassic`     | Classic    |
| `GBSoundListTemplateTypeEnriched`      | Enriched   |
| `GBSoundContentTemplateTypeClassic`    | Classic    |
| `GBPhotoListTemplateTypePinterest`     | Pinterest  |
| `GBEventListTemplateTypeCondensed`     | Condensed  |
| `GBEventContentTemplateTypeClassic`    | Classic    |
| `GBMapsListTemplateTypeEnriched`       | Enriched   |
| `GBMapsContentTemplateTypeBanner`      | Banner     |
| `GBMapsDetailTemplateTypeClassic`      | Classic    |

**A deviation costs one sentence.** Any non-default template must carry a prose justification quoting the phrase in the user's description that motivated it. No quotable phrase → no deviation.

## 3. How to read the tables

Confidence is marked per template, because most of these names have never been documented publicly:

| Mark | Meaning |
|---|---|
| **✔** | Described in GoodBarber's own help or blog. Quote it freely. |
| **○** | **Inferred from the codename alone.** The name is real — captured from a live back office — but the description of what it looks like is a reading of the word, not an observation. Emit `templateVerified: false` and phrase it as "the name suggests", never as fact. |

The distinction matters more than the descriptions do. A wrong template is a two-click fix; a confident-sounding invented capability is the failure mode this whole agent is built to avoid.

## 4. The template tables

### `GBModuleTypeArticle` — list

| Template                       | What it looks like                                                                                                                                                                          | Pick it when                                                                                         |     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --- |
| `Enriched`                     | The default cell. Title never truncated, author **plus avatar**, token info above the title, below the title and at the cell foot, actions in the list. Adapts to the app's margin setting. | Long headlines, named authors, "show the author", metadata-rich editorial.                           | ✔   |
| `Classic`                      | Thumbnail, title, summary line.                                                                                                                                                             | Nothing in the description argues otherwise.                                                         | ✔   |
| `Immersive`                    | Thumbnail **full screen**, one article at a time, **bottom-to-top swipe** between them, TikTok-style. Comments, bookmark and share act directly from the list.                              | "immersive", "like TikTok/Instagram", "swipe through", fresh news with a strong image on every item. | ✔   |
| `Condensed`                    | Sleek and dense — a clear, concise preview per item. Heavily customisable: colours, fonts, image formats, element positioning.                                                              | Many items, skim-reading, "compact", "clean", "a lot of posts".                                      | ✔   |
| `VisualCard`                   | Card cell with **shadow** support and an **edge-to-edge image** option.                                                                                                                     | "cards", "modern", a strong image on every item.                                                     | ✔   |
| `Grid`                         | Name suggests a multi-column grid of thumbnails.                                                                                                                                            | Image-led browsing where the picture identifies the item.                                            | ○   |
| `ClassicUne`                   | *Une* is French for a newspaper front page — name suggests a classic list with the newest item promoted as a large headline cell.                                                           | "front page", "featured story", "highlight the latest".                                              | ○   |
| `UneGrid`                      | Name suggests the same featured item above a grid.                                                                                                                                          | Featured story plus image-led browsing.                                                              | ○   |
| `Visuels`                      | *Visuels* = "visuals" — name suggests an image-dominant list.                                                                                                                               | Photo-led feed with short titles.                                                                    | ○   |
| `SlideShow`                    | Name suggests a horizontally swiped carousel.                                                                                                                                               | A short, curated feed — carousels hide items past the first few.                                     | ○   |
| `MinimalColor`                 | Name suggests a text-first cell using colour rather than imagery.                                                                                                                           | Feeds with **no reliable thumbnail**.                                                                | ○   |
| `MinimalPhotos`                | Name suggests a minimal cell that keeps a small photo.                                                                                                                                      | Text-first with an optional small image.                                                             | ○   |
| `Checkerboard`                 | Name suggests alternating image/text sides down the list.                                                                                                                                   | "alternating", "magazine-style".                                                                     | ○   |
| `VisualCardCondensed`          | Name suggests the card cell in a denser variant.                                                                                                                                            | Cards, but many items.                                                                               | ○   |
| `GridVisualCard`               | Name suggests cards arranged in a grid.                                                                                                                                                     | Cards, image-led, multi-column.                                                                      | ○   |
| `VisualCardGridVisualCard`     | Name suggests a card feature cell above a card grid.                                                                                                                                        | No description justifies this over `VisualCard`. Treat as an expert option.                          | ○   |
| `ImmersiveStorySlideCondensed` | Name suggests a stories-style slide strip over a condensed list.                                                                                                                            | "stories at the top", social-style. Compound name — confirm before promising.                        | ○   |

### `GBModuleTypeArticle` — detail

| Template                                                         | What it looks like                                                                                                     | Pick it when                                                                                       |     |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | --- |
| `ToolBarUp`                                                      | The default article page.                                                                                              | Always, unless the user describes the reading toolbar.                                             | ✔   |
| `ToolBarSlide` `ToolBarAndroid` `ToolBarSwipe` `ToolBarInsideUp` | All four vary **where the action toolbar sits and how it behaves** — the toolbar carrying share, bookmark and comment. | Only when the user describes the toolbar's position or behaviour. Nothing else distinguishes them. | ○   |
| `ToolBarSlideGrenadine`                                          | A `Grenadine` variant — GoodBarber's design-system naming, believed theme-tied rather than structural.                 | Do not select on a theme guess. Flag as available.                                                 | ○   |

**One documented constraint:** the HTML/token editor is **not available on the fourth detail template**. If the plan depends on editing the detail page's token markup — removing the date or author line — say that some detail templates lock it, and keep `Classic`.

### `GBModuleTypeVideo`

The list family is a **strict subset of Article's** — eleven of Article's seventeen, same names, same readings. The detail family is **identical** to Article's seven.

| Template                                    | Note                                                                                                   |                                                            |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| `VisualCard` (list)                         | Default, both slots.                                                                                   | ✔                                                          |
| `Enriched` `VisualCardCondensed`            | Read as on `Article`.                                                                                  | ✔ on Article's documentation, ○ for the behaviour on Video |
| `Grid` `UneGrid` `Visuels` `SlideShow`      | Thumbnail-led. Video items almost always carry a thumbnail, so these are safer here than on `Article`. | ○                                                          |
| `ClassicUne` `MinimalColor` `MinimalPhotos` | Read as on `Article`.                                                                                  | ○                                                          |

**Six Article list templates are NOT available on Video:** `Immersive`, `Condensed`, `Checkerboard`, `GridVisualCard`, `VisualCardGridVisualCard`, `ImmersiveStorySlideCondensed`. A "TikTok-style video feed" therefore cannot be answered with `GBVideoListTemplateTypeImmersive` — that string does not exist. Say the immersive list layout is captured on `Article` only, and leave Video at its default rather than inventing the parallel.

### `GBModuleTypeSound`

| Template                     | What it looks like                                                  | Pick it when                                                                            |     |
| ---------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --- |
| `Enriched` (list)            | The default episode list.                                           | Default.                                                                                | ✔   |
| `SoundCloud` (list)          | Name suggests a SoundCloud-styled list — waveform-ish presentation. | Only if the user names SoundCloud. Note it is a **look**, not the `soundcloud` service. | ○   |
| `GrenadinePodcast` (list)    | A `Grenadine` design-system variant for podcasts.                   | Flag as available; don't select on a guess.                                             | ○   |
| `Classic` (content)          | Default episode page.                                               | Default.                                                                                | ✔   |
| `Banner` (content)           | Name suggests cover art as a banner above the player.               | Strong per-episode or show artwork.                                                     | ○   |
| `ClassicGrenadine` (content) | Theme-tied variant.                                                 | Flag only.                                                                              | ○   |

**Do not confuse template with service.** `SoundCloud` here is a layout; `soundcloud` in `content-sections` is a data source. They are unrelated and a plan may legitimately use one without the other.

### `GBModuleTypePhoto`

| Template     | What it looks like                                                            | Pick it when                                                                  |     |
| ------------ | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | --- |
| `Pinterest`  | Default gallery. Name suggests a masonry grid preserving each image's height. | Default. "Pinterest-style", portrait and landscape mixed.                     | ✔   |
| `VisualCard` | Card gallery — shadow controls, edge-to-edge option, and **8 image ratios**.  | "cards", mixed aspect ratios, "modern gallery".                               | ✔   |
| `Instagram`  | Name suggests a uniform square grid.                                          | "like Instagram", square photos. **Layout only** — no Instagram data. Say so. | ○   |
| `Square`     | Name suggests square crops.                                                   | Uniform crops acceptable.                                                     | ○   |
| `Fullsize`   | Name suggests one large image per row.                                        | Few, large, high-quality photos.                                              | ○   |
| `Edgetoedge` | Name suggests images bleeding to the screen edges, no margin.                 | "full bleed", "no borders".                                                   | ○   |
| `Flickr`     | Name suggests a Flickr-styled layout.                                         | Only if the user names Flickr. Again: a look, not the `flickr` service.       | ○   |
| `List`       | Name suggests one photo per row with its caption.                             | Captions matter more than the images.                                         | ○   |
| `Visuels`    | Name suggests an image-dominant layout.                                       | Generic visual gallery.                                                       | ○   |

Detail slot: **not captured.** `"detail": null`, `templateVerified: false`, plus a note.

### `GBModuleTypeAgenda`

| Template                 | What it looks like                                          | Pick it when                                 |     |
| ------------------------ | ----------------------------------------------------------- | -------------------------------------------- | --- |
| `Condensed` (list)       | The **only captured Event list template**, and the default. | Default. There is nothing to choose between. | ✔   |
| `Classic` (content)      | Default event page.                                         | Default.                                     | ✔   |
| `Banner` (content)       | Name suggests the event image as a banner header.           | Events with artwork — concerts, festivals.   | ○   |
| `BannerCustom` (content) | Name suggests a banner with custom configuration.           | Only on an explicit customisation ask.       | ○   |
| `Cover` (content)        | Name suggests a full-width cover image header.              | Image-led events.                            | ○   |

Events are documented as shareable and bookmarkable through a toolbar on the detail page, and the list is classified by date regardless of template.

### `GBModuleTypeMaps`

| Template                                      | What it looks like                                                                                                            | Pick it when                                                                                              |     |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --- |
| `Enriched` (list)                             | **Default.** Richer per-place cell — carries the place's address and a favourites button.                                     | The default, and a good fit for most place lists: an address in the list is what people want from a map.  | ✔   |
| `Single` (list)                               | Name suggests a single-location view.                                                                                         | One place only — a venue, a shop, an office.                                                              | ○   |
| `Multi` (list)                                | Name suggests several points on one map.                                                                                      | Several locations in one area.                                                                            | ○   |
| `MultiDistant` (list)                         | Name suggests several points spread far apart, so the map opens zoomed out.                                                   | Nationwide or international locations.                                                                    | ○   |
| `SplitView` (list)                            | **Split list-and-map, like Google Maps** — the user sees where they are and what they're looking for without switching modes. | "store locator", "find the nearest", browsing while seeing the map. The strongest documented Maps choice. | ✔   |
| `Visual` (list)                               | Each place carries **several images in a slideshow** — built for high visual impact per place.                                | Tourism, restaurants, venues, "show photos of each place".                                                | ✔   |
| `SplitEnriched` (list)                        | The split view with the enriched cell.                                                                                        | Both of the above.                                                                                        | ✔   |
| `Classic` (list)                              | A plain list of places.                                                                                                       | Text-first directory.                                                                                     | ○   |
| `Grid` (list)                                 | Name suggests a grid of places.                                                                                               | Image-led place browsing.                                                                                 | ○   |
| `Banner` (content)                            | **Default** for the content slot.                                                                                             | Default.                                                                                                  | ✔   |
| `Classic` `HTML` `ClassicGrenadine` (content) | `HTML`'s name suggests a free-form HTML place page.                                                                           | Only on an explicit ask.                                                                                  | ○   |
| `Classic` (detail)                            | The lone `GBMapsDetailTemplateTypeClassic`.                                                                                   | Emit only if the plan needs the third family; note it isn't understood.                                   | ○   |

`Maps` has the most useful default of the six: `Enriched` puts each place's address in the list, which is what most people want from a map section, and it is documented rather than inferred. Leave it there unless the description says something specific — **one** location (`Single`), places spread across a country (`MultiDistant`), a locator people search (`SplitView`), or photos of each place (`Visual`).

## 5. Signals in the description → template

Read the **description**, not the section name. Match a phrase, or take the default.

| The user says… | List template | Why |
|---|---|---|
| nothing about look or feel | **the default** | §2. This is the majority case. |
| "immersive", "full screen", "swipe like TikTok" | `Immersive` | Documented full-screen swipe list. |
| "modern cards", "clean cards" | `VisualCard` | Documented card cell with shadow. |
| "lots of posts", "compact", "easy to skim" | `Condensed` | Documented dense preview cell. |
| "show the author", long headlines, rich metadata | `Enriched` | Documented author avatar, untruncated title. |
| "front page", "featured story on top" | `ClassicUne` / `UneGrid` | ○ Name reading — say so. |
| "grid", "tiles", "gallery of thumbnails" | `Grid` | ○ |
| "magazine", "alternating" | `Checkerboard` | ○ Article only. |
| "no images", "text only", a feed with no thumbnails | `MinimalColor` or `Classic` | Never a visual layout — see §6. |
| "like Instagram" (a gallery) | `Photo` + `Instagram` | ○ Layout only. Disclose that no Instagram data is involved. |
| "Pinterest-style", mixed portrait/landscape | `Photo` + `Pinterest` | ○ |
| "store locator", "find the nearest one" | `Maps` + `SplitView` | Documented split view. |
| "photos of each place", tourism, restaurants | `Maps` + `Visual` | Documented per-place slideshow. |
| "show the address in the list", saved places | `Maps` + `Enriched` / `SplitEnriched` | Documented. |
| one venue, one office | `Maps` + `Single` | ○ The only case that beats the `Enriched` default — one place needs no list. |
| several / distant places | `Maps` + `Multi` / `MultiDistant` | ○ The default is wrong here — deviate. |
| "play episodes from the list" | `Sound` + `Enriched` | ○ |

**Check availability before applying a row.** The families do not share a vocabulary, and a name that exists on one type is not a name you may compose on another.

A signal pointing at a template the type doesn't have is not a licence to compose the name. The type keeps its default, and its `notes` says which type does carry that layout.

## 6. Constraints that override a preference

**A visual template needs images, and the service decides whether there are any.** This is the one place where the template decision genuinely depends on earlier decisions:

- `service: rss` on a publisher's public feed often yields headline-plus-summary with an unreliable image. `Immersive`, `Visuels`, `Grid` and the card templates all render a hole where the thumbnail should be. Default to `Classic` or `Condensed` and say why.
- `service: custom` shows images only if the JSON exposes them. If the user hasn't confirmed an image field, do not plan a visual layout on top of it.
- `service: mcms` means the owner uploads every image by hand. A visual template is a **content commitment** — a promise to attach a good image to every item, forever. Say so before recommending one.
- `youtube`, `vimeo`, `flickr` and podcast feeds carry artwork reliably. Visual templates are safe there.

**The thumbnail fallback is not universal.** A default thumbnail can be configured for list pages, but the help notes that option is *not available on all templates*. So the fix for a patchy image supply is a text-first template, not a fallback image.

**Categories are a separate template axis.** Multi-category sections carry their own category templates — `Tags` and `Labels` are documented, usable across all content lists. Their codenames are not captured. Mention the axis when the description implies browsing by topic; emit no codename for it.

## 7. What goes in the plan

For each content section:

```json
"template": {
  "list": "GBArticleListTemplateTypeCondensed",
  "detail": "GBArticleDetailTemplateTypeClassic"
},
"templateVerified": false
```

- Both keys always present. `null` where a family wasn't captured — never omit the key.
- `templateVerified: true` **only** when the chosen template is a documented one (✔ in §4) *and* the reason for choosing it is in the user's own words. Defaults chosen for lack of a signal are `true` — the default is captured fact. Anything ○ is `false`.
- One sentence **in the section's `notes`** per non-default choice, quoting the phrase that drove it. Not in prose — the report's prose budget is two lines before the JSON and three after, and template reasoning does not earn a line of it.
- One sentence in `notes` whenever a template is a **look-alike**, not an integration: the `Instagram`, `Flickr` and `SoundCloud` templates pull no data from those platforms.
- Defaults need no justification at all. Say nothing — an unexplained default is the expected case, and writing "left at the default" for every section is exactly the bloat this budget exists to prevent.

## 8. Validation checklist

- [ ] Every template string is verbatim from §4 — family prefix plus a captured variant. Nothing invented, no `Detail`/`Content` swap.
- [ ] Both slots emitted for every content section; `null` where the family wasn't captured, with a note saying so.
- [ ] Non-content types carry `"template": null` and `templateVerified: false` — this skill has no vocabulary for them.
- [ ] Every non-default template has a one-sentence justification **in `notes`**, quoting the description. Defaults carry none.
- [ ] No visual template sits on a service with an unconfirmed image supply (§6).
- [ ] Agenda used `Condensed`, and Maps used `Enriched`/`Banner` — not `Classic` — as their defaults.
- [ ] Every ○ template carries `templateVerified: false` and is phrased as inference in its `notes`.
- [ ] `Instagram` / `Flickr` / `SoundCloud` templates carry the "layout only, no data" line in `notes`.
- [ ] Maps' unexplained third template family is noted, not silently dropped.
- [ ] Nothing from the sources footer below appears in the report — no URLs, no access dates.

---

*The references below are provenance for whoever maintains this skill. **They are not for the agent's output** — the report cites no sources and carries no URLs.*

*Template codenames: `section-docs/0-section-type-codenames.md`, captured from a live back office 2026-08-12.*

*Template behaviour, accessed 2026-08-21 — GoodBarber help, [Design individual sections](https://www.goodbarber.com/help/design-your-app-sections-r89/design-individual-sections-a106/) (last updated July 2026: the two design slots, toolbar/navigation/thumbnail/HTML options, the thumbnail and HTML-editor limits); GoodBarber blog — [Modernize your article lists with the new immersive template](https://www.goodbarber.com/blog/modernize-your-article-lists-with-the-new-immersive-template-a1207/) (Immersive), [Design update: a new template for the Articles section](https://www.goodbarber.com/blog/design-update-a-new-template-for-the-articles-section-of-your-goodbarber-app-a1267/) (Enriched Classic), [Design Update: A new template for displaying your article lists](https://www.goodbarber.com/blog/design-update-a-new-template-for-displaying-your-article-lists-a1329/) (Condensed Classic), [Design update: a new Split View map template](https://www.goodbarber.com/blog/design-update-a-new-split-view-map-template-a1229/) and [A stunning new template for your Map section](https://www.goodbarber.com/blog/design-update-a-stunning-new-template-for-your-map-section-a1223/) (Maps SplitView and Visual), [Design update: a new template for all your content lists](https://www.goodbarber.com/blog/design-update-a-new-template-for-all-your-content-lists-a1248/) (category Tags/Labels templates), and the [Changelog](https://www.goodbarber.com/changelog/) (VisualCard shadow and edge-to-edge options, Photo VisualCard's 8 ratios, Maps Enriched/SplitEnriched address and favourites).*

*Everything marked ○ is a reading of the codename with no source behind it. GoodBarber does not publish a per-template reference; the back office's own template picker is the only complete one. Until someone captures it, the honest position is the one in §2 — **the default is the best available choice**, and a deviation needs a phrase from the user to stand on.*
