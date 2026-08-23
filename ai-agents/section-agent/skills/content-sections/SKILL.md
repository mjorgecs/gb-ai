---
name: content-sections
description: "Choose the service behind a GoodBarber content feed — the six list-plus-detail section types (Article, Photo, Video, Sound, Maps, Agenda) and the connectors that fill them. Use when a described feature is a repeating feed of items: a blog, news, a gallery, videos, a podcast, events, a calendar, or places on a map. Covers picking between the built-in CMS, a platform connector, a plain RSS feed, and a custom JSON feed; validating that an external feed is still alive; and the categories and list/detail model these sections share. Do NOT use for static pages, forms or links (use utility-sections), or for choosing the type itself (use section-routing)."
---

# Content Sections

The six types that share one shape: a **list** of items and a **detail** view of one item. `Article`, `Photo`, `Video`, `Sound`, `Maps`, `Agenda`.

Once `section-routing` has picked one of these, the remaining decision is **`service`** — where the items come from. That is what this skill is for.

## 1. The shared model

Everything in this table is true of all six types.

| | |
|---|---|
| **List view** | The feed. The only part with two editable layers — content *and* design. |
| **Detail view** | One item. Design only; its content is inherited from whichever list item was tapped, so it has no independent content store. |
| **Categories** | A one-level taxonomy **scoped to the section** — not app navigation. Plan them before content is entered; retro-fitting means re-filing every item. |
| **Comments** | An optional shared block — internal comments with a display order, or Disqus, toggled independently. |
| **Metadata** | `Title` (32 chars) and `Description` (200 chars, used for SEO/PWA metadata). |
| **Publication** | A section-level draft/published toggle. |

Each type then adds its own fields — `Sound` has play settings (autoplay, loop) that `Article` doesn't. When planning, mention type-specific settings only when the user's description implies one.

**Where the items actually live.** Not in the section. Every section — CMS-backed or connector-backed — reads from the same internal endpoint, `/front/get_items/{appId}/{sectionId}/`. A server-side service adapter fetches the external source on a schedule and normalises it into one item schema:

```
[WordPress]──┐
[RSS]────────┼─→ server-side `service` adapter ─→ /front/get_items/… ─→ native app
[mcms CMS]───┘        (normalises to one item schema)      (identical for all)
```

Two consequences to carry into every plan:

1. **The feed URL is not in the section JSON.** It's a separate server-side record, edited in the section's Settings. Emit it as `sourceBinding`, described as a second step.
2. **Feed-backed sections have no "Edit the content" action.** The service owns the items. If the user pictures writing posts by hand, they want `mcms`, not a connector — say so.

## 2. The service tables

Known good as of 2026-08-12. Not exhaustive — GoodBarber adds connectors. A platform that isn't listed is **not a gap and not something to go and find**: you have no web access, so emit the matched type with `"service": null`, `serviceVerified: false`, `status: "undetermined"`, and a `notes` line saying a connector may exist but isn't in your tables. Never invent a service name from a brand name.

### `GBModuleTypeArticle`

| Service           | Source                                                  |
| ----------------- | ------------------------------------------------------- |
| `mcms`            | The built-in CMS — the owner writes posts in GoodBarber |
| `wordpress`       | A self-hosted WordPress site                            |
| `wordpressdotcom` | WordPress.com                                           |
| `rss`             | Any RSS/Atom feed                                       |
| `substack`        | Substack                                                |
| `medium`          | Medium                                                  |
| `squarespace`     | Squarespace                                             |
| `blogger`         | Blogger                                                 |
| `wmarticle`       | GoodBarber's own WMaker CMS                             |
| `custom`          | Your own JSON matching GoodBarber's Content API spec    |

### `GBModuleTypeSound`

| Service      | Source                   |
| ------------ | ------------------------ |
| `podcast`    | (a podcast RSS feed)     |
| `soundcloud` | —                        |
| `anchor`     | (Spotify for Podcasters) |
| `spreaker`   | —                        |
| `ausha`      | —                        |
| `simplecast` | —                        |
| `wmpodcast`  | —                        |
| `custom`     | —                        |
| `mcms`       | —                        |

### `GBModuleTypeVideo`

| Service        |
| -------------- |
| `mcms`         |
| `youtube`      |
| `dailymotion`  |
| `rss`          |
| `videopodcast` |
| `vimeo`        |
| `wmvideo`      |
| `custom`       |

### `GBModuleTypePhoto`

| Service   |
| --------- |
| `mcms`    |
| `flickr`  |
| `wmphoto` |
| `custom`  |
| `mcms`    |

### `GBModuleTypeAgenda`

| Service     | Notes       |
| ----------- | ----------- |
| `mcms`      | —           |
| `vcalendar` | (iCal/vCal) |
| `wmevent`   | —           |
| `custom`    | —           |

### `GBModuleTypeMaps`

| Service  |
| -------- |
| `mcms`   |
| `klm`    |
| `custom` |

**`custom` is on all six.** It is the "point at your own JSON" escape hatch.

## 3. Picking the service

In order:

**1. Did the user name a platform they already publish on?** Use that platform's service. WordPress → `wordpress`, YouTube → `youtube`, Spotify for Podcasters → `anchor`.

**2. Do they have their own API or JSON feed?** → `custom`. Requires the source to expose JSON matching GoodBarber's Content API spec, so say that: it's a real prerequisite, and if the feed doesn't exist yet, someone has to build it.

**3. Will they write the content in GoodBarber?** → `mcms`.

**4. Do they just want content from some public site?** → `rss`, with the caveats below.

### Prefer the dedicated connector over `rss`

When a platform has its own service, use it. WordPress content pulled through `rss` works, but the dedicated connector is reported to support **category filters and comments** where plain RSS does not. Only fall back to `rss` when no dedicated connector exists for that platform.

> *Attribution: the category-filter and comments difference comes from GoodBarber's help documentation on connecting external content sources, via the superseded `app-structure` skill. It is not in the back-office captures. State it as "the dedicated connector generally supports more" rather than as a hard capability claim — and if the difference is load-bearing for the decision, say it's worth confirming rather than confirming it yourself.*

### Two things to tell the user about `rss`

**A feed that resolves is not a feed that works.** Publishers routinely stop updating an RSS endpoint while leaving it online — it keeps returning a valid document containing the last items it ever published. The section builds correctly, populates correctly, and looks broken to end users because every headline is two years old.

**You cannot check this — you have no web access — so do not supply feed URLs.** Never invent one, and never assert that a feed you were told about is live. Ask the user for their URL and put the warning in the section's `notes`: whoever binds the feed should look at the date of the newest item, not just that the URL responds. A dead feed satisfies any "must have N items" expectation just as well as a live one, with dead content. **Dates, not counts.**

**Many publishers syndicate only headline plus summary.** Full articles stay behind a paywall. That's the normal, intended use of a public feed, but it means the section shows teasers that link out rather than readable in-app articles. Set that expectation rather than letting the user discover it.

## 4. Check `custom` before declaring a gap

**This is the rule this skill exists to enforce.**

"A photo section linked to an API with images", "videos from our own backend", "events from our internal system" — all of these read like gaps and none of them are. They are the matched type plus `service: custom`, which is the *`<Type>` custom feeds* family in the catalog.

Before any content-type intent goes to the gap path, confirm:

- [ ] Is the type one of the six? If yes, `custom` exists.
- [ ] Can the user's data be exposed as JSON? If yes or maybe, it's `custom` — not a gap.
- [ ] Only if the data genuinely cannot be a feed of uniform items does the gap path open.

The last one is the real test. `custom` gives you a **read-only feed of uniform items rendered as list-plus-detail**. What it cannot do is anything interactive, per-user, or mutable — a wish list, a calculator, a booking flow. Those aren't feeds and no service will make them one.

When you do route to `custom`, put the prerequisite in the section's `notes`: *"requires a JSON endpoint matching GoodBarber's Content API spec — confirm this exists."* State the prerequisite; don't estimate what it takes to build.

## 5. Type-specific notes

**`Article`** — the workhorse. The catalog's largest family by far, and most "content" intents land here. If the user describes text items with titles, it's `Article`.

**`Sound`** — recorded audio episodes. A **live** radio stream is `GBModuleTypeLive` with `liveradio`, not `Sound`. The distinguishing question is whether there are discrete episodes to list.

**`Video`** — same split: a video library is `Video`, a live stream is `Live` with `livevideo`.

**`Photo`** — a gallery. If the user wants images attached to written posts, that's `Article` with images in the items, not a `Photo` section.

**`Maps`** — geolocated points as a feed, which is why "places of interest", "our store locations", "where to find us" all land here rather than on `Contact`. `Contact` is one address; `Maps` is many points. The `kml` service takes a KML file, which is how existing Google My Maps data gets in.

**`Agenda`** — dated events. `vcalendar` accepts iCal/vCal, so anything already in a calendar system has a path in. If the user describes a schedule that changes constantly, mention that `mcms` means editing each event by hand while `vcalendar` syncs.

## 6. What to put in the plan for each section

- The type and service, with why the service was chosen over the obvious alternative if it wasn't obvious.
- The `sourceBinding` if the service fetches externally — kind, a suggested URL where you can name one, and the note that it's bound server-side.
- **Whether content can be authored in-app.** `mcms` yes; everything else no. This is the single most useful sentence for a non-technical user.
- Any prerequisite: a JSON endpoint for `custom`, an existing account for a connector, a KML file for `kml`.
- A categories note if the description implies browsing by topic — they must be planned before content entry.

---

*Sources: `section-docs/0-section-type-codenames.md`; GoodBarber help — [Connect external content sources for articles](https://www.goodbarber.com/help/publish-and-manage-articles-r94/connect-external-content-sources-for-articles-a19/) and [Create custom content feeds](https://www.goodbarber.com/help/build-custom-content-feeds-r111/create-custom-content-feeds-a287/), both cited via the superseded skill and not re-fetched on 2026-08-13.*
