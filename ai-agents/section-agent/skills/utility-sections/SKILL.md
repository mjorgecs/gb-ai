---
name: utility-sections
description: Plan the non-feed GoodBarber sections — static pages, contact details, forms, user submissions, search, QR scanning, menu containers, external links, embedded web views, live streams, social integrations and external storefront links. Use when a described feature is a single page rather than a repeating feed, or when the request names a social network, an embedded third-party tool, a live stream, or a link out of the app. Owns the mandatory disclosure that TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat sections are links rather than embedded feeds, and the distinction between an embedded web view and code running in the app. Do NOT use for feeds of items (use content-sections).
---

# Utility Sections

Everything that isn't a content feed. Mostly one screen, mostly little or no configuration — but three of them mislead users badly enough to need a scripted disclosure.

## 1. Quick reference

| Type                      | What it is                                     | Service                                          |
| ------------------------- | ---------------------------------------------- | ------------------------------------------------ |
| `GBModuleTypeAbout`       | One static page of rich content                | `mcms`                                           |
| `GBModuleTypeContact`     | Contact details — address, phone, hours        | none                                             |
| `GBModuleTypeForm`        | Form builder, structured input from users      | `mcms`                                           |
| `GBModuleTypeSubmit`      | Users propose content for the owner to publish | none                                             |
| `GBModuleTypeSearch`      | Search across the app's content                | none                                             |
| `GBModuleTypeQrcode`      | QR code scanner                                | none                                             |
| `GBModuleTypeNode`        | A menu screen that leads to other sections     | none                                             |
| `GBModuleTypeClickto`     | Deep link to an external site or app           | none                                             |
| `GBModuleTypeFakeclickto` | Branded link-out styled as a native section    | `clickto*`                                       |
| `GBModuleTypeCustom`      | A web view pointed at a URL                    | `typeform` `tawkto` `airtable` `jotform` or none |
| `GBModuleTypePlugin`      | An installed extension or Custom Code          | `aistudio` `rag` or none                         |
| `GBModuleTypeLive`        | Live audio or video stream                     | `liveradio` `livevideo`                          |
| `GBModuleTypeFacebook`    | Facebook integration                           | `facebook` *                                     |
| `GBModuleTypeInstagram`   | Instagram integration                          | `clicktoinstagram` *                             |
| `GBModuleTypeTwitter`     | X (Twitter) integration                        | `clicktotwitter` *                               |
| `GBModuleTypeShop`        | External storefront link                       | `shopify` `amazon` `etsy`                        |
| `GBModuleTypeHome`        | Composable widget landing page                 | not captured †                                   |
| `GBModuleTypeBookmark`    | Favorites — **auto-added**                     | not captured †                                   |
| `GBModuleTypeSettings`    | App settings — **auto-added**                  | not captured †                                   |
| `GBModuleTypeTos`         | Terms / Privacy — **auto-added, ×2**           | `classictos` `classicprivacy`                    |

Known good as of 2026-08-12, and not a closed list.

**\*** The capture lists `facebook`, `clicktoinstagram` and `clicktotwitter` against these three types **as a group**, not one-to-one. The pairing above is the obvious reading and is probably right, but it is inference — emit `serviceVerified: false` for Instagram and X (Twitter).

**†** The service table omits these three types entirely. "Not captured" is not the same as "none" — do not assert either. Emit `"service": null` with `serviceVerified: false`.

## 2. The auto-added four

`Bookmark`, `Settings`, and `Tos` twice (terms of sale, privacy policy) are present in apps without anyone choosing them. They live in the "Other sections" area — in the app but outside navigation.

**Never propose creating them.** If the user asks for a favorites feature or a privacy page, the answer is "already there — it needs configuring and, if it should be in the menu, placing," not a create action. Reference them in the plan with a note that they exist.

## 3. `Fakeclickto` — the mandatory disclosure

Six social platforms produce `GBModuleTypeFakeclickto`:

| Platform | Service |
|---|---|
| TikTok | `clicktotiktok` |
| Reddit | `clicktoreddit` |
| WhatsApp | `clicktowhatsapp` |
| Discord | `clicktodiscord` |
| Threads | `clicktothreads` |
| Snapchat | `clicktosnapchat` |

A `Fakeclickto` section looks like a native section in the catalog and in the menu, and is a **branded link-out** to the external app or a URL. The name is candid about what it is.

**Say this every time.** A user asking for "a TikTok section in my app" is picturing their videos playing in the app. They will get a tile that launches TikTok. Wording that works:

> A TikTok section is available, but it's a link rather than a feed — tapping it opens TikTok rather than playing your videos inside the app. If you want video playing in the app itself, that's a Video section with a YouTube or Vimeo source, or your own video feed.

Then offer the alternative, because there usually is one.

**Facebook, Instagram and X are different** — they have first-class types with their own renderers. Note that Instagram's and X's services are still named `clickto*`, so verify the actual behaviour before promising embedded content there too. Flag it as uncertain rather than asserting either way.

## 4. `Custom` vs `Plugin` — the other expensive mix-up

| | `GBModuleTypeCustom` | `GBModuleTypePlugin` |
|---|---|---|
| Mechanism | A web view pointed at a URL | Code or an extension running in the app |
| Examples | URL · Typeform · Tawk.to · Airtable Form · JotForm | Custom Code · RAG Chatbot · Create with AI |
| Cost to build | A URL field | Writing and maintaining code |

Typeform, Tawk.to, Airtable Form and JotForm are `Custom` **with a preset URL** — nothing more. If the user already has a form, a chat widget, a booking page or a dashboard on the web, `Custom` embeds it in one step.

**Ask "does this already exist on the web?" before reaching for `Plugin`.** Routing to `Plugin` when `Custom` would do turns a URL field into a development project.

The reverse also matters. `Custom` is a web view: it renders an external page and does not get the app's native capabilities. If the feature needs on-device storage, the user's login state, geolocation, or native sharing, `Custom` can't do it and `Plugin` is right.

## 5. Notes on the rest

**`About`** — one static page. Reach for it whenever the content doesn't repeat: an info page, credits, a mission statement, terms that aren't the auto-added legal pages. A content section is the wrong shape for a single page, and a common over-reach when the user says "a page about X".

**`Contact`** — one organisation's details. Several locations is `Maps`, not several `Contact` sections.

**`Form` vs `Submit`** — both take input from users, and they differ in what happens next. `Form` collects structured answers for the owner (enquiries, sign-ups, feedback). `Submit` is a contribution pipeline — the user proposes content that the owner reviews and publishes into a content section. If the user's answer becomes app content, it's `Submit`; if it becomes a message, it's `Form`.

Neither is a private per-user list. That's the gap path — see `section-routing`.

**`Search`** — searches the app's own content. Worth including in any app with several content sections and a lot of items; not worth it in a four-section app.

**`Node`** — a menu screen leading to other sections. This is the platform's only real nesting, and navigation is otherwise flat. Use it when the app has enough sections that the main menu would be unwieldy; mention that no arbitrary multi-level hierarchy exists.

**`Clickto`** — a menu entry that opens an external site or app. Creates no screen. Good for "link to our main website" without building anything.

**`Live`** — `liveradio` for audio, `livevideo` for video. The distinction from `Sound`/`Video` is discrete episodes versus a continuous stream. A radio station usually wants both: `Live` for the stream, `Sound` for the archive.

**`Shop`** — links out to a Shopify, Amazon or Etsy storefront. It is a **link**: no catalog, no cart, no checkout inside the app. Say that, because a user asking for "a shop" is usually picturing one in the app. This agent plans content apps only and has no eCommerce vocabulary — a request for real in-app selling is `"undetermined"`, not a gap, and planning it is outside what you cover.

**`Home`** — a singleton landing page assembled from widgets (Content, Link, Social links, Separator, Custom Code, Legal links, Text). Its Content widget can only reference sections **that already exist**, so if a plan includes Home, say that it's assembled last. Home can also be disabled entirely, launching the app straight into another section.

**`Plugin`** — covers installed extensions and Custom Code both. `rag` is the RAG Chatbot, `aistudio` is Create with AI (BETA — flag the maturity risk), and no service at all means a hand-written Custom Code section.

Name `Plugin` when the user explicitly asks for one of those. **Never reach for it to close a gap, and never describe what the code would do** — no spec, no scope, no feature design. "The platform has no section for this" is a complete answer.

## 6. Before emitting a utility section

- [ ] Not one of the auto-added four being proposed as new.
- [ ] Any `Fakeclickto` section carries the link disclosure in its `notes`.
- [ ] `Custom` was considered before `Plugin` — does the thing already exist on the web?
- [ ] No `Plugin` section was invented to close a gap, and no custom-code spec was written.
- [ ] `Shop` described as a link out; nothing eCommerce planned.
- [ ] `About` used for single pages rather than a content section.
- [ ] `Form` vs `Submit` decided by what happens to the answer.
- [ ] `Live` vs `Sound`/`Video` decided by stream versus episodes.
- [ ] If `Home` is in the plan, it's assembled after the sections it references.

---

*Sources: `section-docs/0-section-type-codenames.md`
