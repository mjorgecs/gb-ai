# Example 02 — Wish list (genuine gap)

**What this example tests:** the gap path, end to end. Both halves required — near-miss alternatives *and* a full custom-code specification. Also tests that the agent doesn't take either of the two decoys.

## Input

> I run a small ceramics studio. I want an app where people can browse our pieces, and where each person can build their own wish list of pieces they'd like — adding and removing things, and coming back to it later.

## Must get right

- Two intents: browse (matched) and wish list (gap).
- Browse → `GBModuleTypePhoto` or `GBModuleTypeArticle` + `mcms`. Either defensible; the reasoning must be stated.
- Wish list → **gap**, with `alternatives[]` *and* `customCode{}`. One without the other is a failure.
- The storage decision surfaced as a user choice with its trade-off, not decided silently.
- The maintenance liability stated.

- **All four gap checks visible in the output**: no type, no `custom` feed, no `GBModuleTypeCustom` web view, and an empty store search. The store search is the one that gets skipped.
- `GBModuleTypeBookmark` offered as a real first option, not dismissed. The wanted items *are* in the app here, so Favorites may well be enough.

## Must not do

- Declare the gap without searching the extension store. An unfamiliar capability is a lookup before it is a gap.
- Assert `Bookmark` limitations that aren't in the source docs — no invented claims about reordering, notes or authorability.
- Route it to `GBModuleTypeSubmit`. That submits to the owner for publication.
- Skip the `custom` feed check before declaring the gap.
- Choose on-device or per-user storage without asking.
- Put a Custom Code **widget** anywhere except Home — widgets are a Home-page surface.

---

# App Structure — Ceramics Studio

## Summary

A catalogue app for a ceramics studio, with a personal wish list each visitor builds for themselves.

Two intents. One matches an existing section; one has no section type in the platform and needs a Custom Code section.

## Sections

### 1. Pieces — `GBModuleTypePhoto` + `mcms`

The studio's catalogue. `Photo` rather than `Article` because ceramics are browsed visually — the image is the item, and the description supports it.

*If each piece needs substantial written material — process, materials, provenance — `Article` with images is the better shape. The two are equally easy to build; the question is whether people read or look.*

- The studio authors pieces in the built-in CMS.
- Plan categories before entering pieces if browsing by range or type matters (tableware, vases, one-offs).

### 2. Wish list — **no section type exists**

#### Why this is a gap

The distinguishing question for any list feature is **who owns and reads the data**. Here, each visitor authors a list only they read. The platform has types for the other two cases and not for this one:

| Near miss | What it actually does | Why it might fall short |
|---|---|---|
| `GBModuleTypeBookmark` (Favorites) | Lets users mark items **already in the app** and read them back later | **Genuinely a candidate here** — the pieces *are* in the app, so the reference direction works. It's auto-added, so it costs nothing and needs no build. What it gives is the platform's own favourites behaviour; whether that covers "adding and removing things and coming back later" is a question for the studio, not something to assume either way. |
| `GBModuleTypeSubmit` | Users propose content for the **owner** to review and publish | A contribution pipeline. What the user submits goes to the studio, not into a private list. Wrong direction. |
| `GBModuleTypePhoto` + `custom` | A feed from your own JSON | Read-only and identical for every user. A custom feed can't be written to from the app, so it can't hold a personal list. Checked and ruled out. |
| Extension store | — | Searched both the main catalog and the Memberships & Login category on 2026-08-13. Nothing offers a user-authored private list. Authentication supports per-user data but provides no list feature of its own. |

#### The recommendation, in order

1. **Try `GBModuleTypeBookmark` first.** It's already installed, it costs nothing, and it may simply be the answer. Ask the studio to look at what Favorites actually does with their catalogue before commissioning anything.
2. **If it isn't enough**, this is a real gap and needs a Custom Code section — spec below.

An honest note on step 1: this plan does not assert what Favorites can and can't do. The back-office captures behind this agent record only that it exists and is auto-added. Rather than guess at its limits, the studio should look — five minutes of clicking beats a paragraph of inference.

**Before committing to custom code:** GoodBarber does not debug code it did not write. A Custom Code section is entirely the studio's maintenance liability, and that is the reason to exhaust step 1 first.

#### Decision required before building

**Where does the list live?** No default is right; the studio picks.

| | On-device | Per-user account |
|---|---|---|
| Setup | Nothing to install | Requires the **Authentication** extension |
| Barrier for visitors | None — works immediately | Sign-up before the feature works at all |
| Across devices | No — phone and tablet keep separate lists | Yes |
| Survives reinstall | No | Yes |

For a studio catalogue where most visitors browse once, **on-device is likely right** — a sign-up wall in front of a wish list loses more people than the sync gains. The spec below assumes on-device and notes where per-user would differ.

---

## Gaps

### Custom code — Wish list {#custom-code-wish-list}

**Section type:** `GBModuleTypePlugin`, no service. One screen, one self-contained `index.html`.

#### 1. Purpose

A personal wish list. Visitors browsing the studio's catalogue mark pieces they'd like, and return later to a list they can review, reorder and prune. The list is private to that person and never seen by the studio.

Nothing pre-built covers it once `Bookmark` has been ruled out by the studio: `Submit` sends content to the owner rather than keeping it private, a `custom` feed is read-only, and a store search on 2026-08-13 found no extension offering a user-authored private list. Users authoring data only they read has no section type.

*This spec is conditional on step 1 above. If Favorites turns out to be sufficient, none of it is needed.*

#### 2. Screens and flow

One screen with four states, managed in JavaScript.

- **Loading** — shown while reading storage. Should be brief; a spinner is acceptable but a skeleton list is better.
- **Empty** — no saved pieces. Shows a short line explaining how to add one and a link into the Pieces section. **This is the first thing most users see and it must not be a blank screen.**
- **Populated** — the list of saved pieces, newest first, each with a remove control.
- **Error** — storage unavailable. Explains that the list can't be saved on this device, and continues to work in memory for the session.

Adding happens from the Pieces section, not here. The route is a **deep link into this section carrying the piece id** — it requires no change to the Pieces section and no additional surface.

*Note on what isn't available: a Custom Code **widget** would be a nicer add control, but widgets are a **Home-page** surface. There is no documented way to place one on a content section's detail view, so an in-place "add" button on each piece is not specified here. If the studio wants one, that needs confirming against the platform before it's promised.*

#### 3. Data model

```
WishItem
  id          string, required, unique   — the piece's id from the catalogue
  title       string, required, max 120  — piece name, copied at add time
  imageUrl    string, optional           — absolute https URL to the thumbnail
  addedAt     string, required           — ISO 8601 timestamp
```

Example:

```json
{
  "id": "vase-cobalt-014",
  "title": "Cobalt tall vase",
  "imageUrl": "https://cdn.example.com/pieces/vase-cobalt-014-thumb.jpg",
  "addedAt": "2026-08-13T14:22:05Z"
}
```

Stored as a JSON array under a single key, `ceramics.wishlist.v1`. The `v1` suffix is deliberate — it allows a future format change without corrupting existing lists.

Title and image are **copied at add time**, not looked up. The list must render offline and must not break when a piece is withdrawn from the catalogue.

#### 4. External contract

**None.** The section makes no network calls. Everything it renders was copied into storage when the item was added.

This is a deliberate simplification and it has a consequence worth stating: if a piece's name or photo changes in the catalogue, saved entries keep the old values. For a studio catalogue that is acceptable. If it isn't, the section would need to re-fetch each piece by id from a Content API endpoint, and that is a materially bigger build.

#### 5. Rendering

```html
<div id="wishlist">
  <header class="wl-header">
    <h1>My wish list</h1>
    <span class="wl-count" aria-live="polite"></span>
  </header>

  <div class="wl-state wl-loading">…skeleton rows…</div>

  <div class="wl-state wl-empty" hidden>
    <p>Nothing saved yet.</p>
    <p class="wl-hint">Browse the pieces and tap the heart on anything you like.</p>
    <a class="wl-cta" href="#pieces">Browse pieces</a>
  </div>

  <ul class="wl-list" hidden>
    <!-- <li class="wl-item" data-id="…">
           <img class="wl-thumb" src="…" alt="">
           <div class="wl-meta">
             <span class="wl-title">…</span>
             <time class="wl-added">…</time>
           </div>
           <button class="wl-remove" aria-label="Remove …">×</button>
         </li> -->
  </ul>

  <div class="wl-state wl-error" hidden>
    <p>This device won't let the app save your list.</p>
    <p class="wl-hint">You can still use it for now, but it won't be here next time.</p>
  </div>
</div>
```

Exactly one `.wl-state` or `.wl-list` visible at a time.

**Restate the design tokens in CSS.** Sources disagree on whether a Custom Code section inherits the app's global App Style; restating the palette and font stack costs nothing and guarantees the section matches:

```css
:root {
  --wl-bg:      #FFFFFF;   /* match the app's background */
  --wl-fg:      #1A1A1A;   /* body text */
  --wl-muted:   #6B6B6B;   /* timestamps, hints */
  --wl-accent:  #2F5D50;   /* the studio's accent */
  --wl-font:    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
```

Thumbnails at a fixed aspect ratio with `object-fit: cover`, so a mixed-size catalogue still renders as an even list. Rows at least 44px tall for touch. Remove buttons need a visible focus state.

#### 6. State and persistence

- **In memory:** the current array, the active view state.
- **On device:** the array, serialised to JSON under `ceramics.wishlist.v1`.
- **Nowhere else.** No server, no account.

Every storage access wrapped in `try/catch`. On failure, fall back to an in-memory array and show the error state's notice — the section stays usable for the session and the user knows why it won't persist. A silent failure reads as data loss.

Write on every mutation, not on a timer. A webview can be killed at any moment.

**Consequence the studio must be told, in these words:** the list is per device and is lost if the app is uninstalled. Someone who saves pieces on their phone will not see them on their tablet. Switching to per-user storage requires the Authentication extension and puts a sign-up in front of the feature.

#### 7. GoodBarber integration points

- **Opened from** a menu entry, and from the empty state's link back to Pieces.
- **Adding** via deep link carrying the piece id, title and image URL (flow (a) in §2). Parse from the URL, validate, append, then render.
- **App API used:** on-device storage only. Nothing else is required, which is what keeps this buildable without Authentication.
- **Not used:** login state, subscription status, geolocation, native sharing. If the studio later wants sync, the change is per-user storage plus the Authentication extension — and the data model above ports unchanged.
- **Prerequisites:** none as specified. Per-user storage would add Authentication.

#### 8. Edge cases

| Case | Behaviour |
|---|---|
| Storage disabled or throws | Error state notice; in-memory list; section stays usable |
| Stored JSON is malformed | Discard, log to console, start empty. Never let a parse error blank the screen |
| Duplicate add (same id) | Silently ignore; do not create a second row |
| Missing or broken `imageUrl` | Render a neutral placeholder tile. Never a broken-image icon |
| Very long title | Clamp to two lines with ellipsis; full title in the `title` attribute |
| Piece withdrawn from the catalogue | Entry still renders — title and image were copied. This is intended |
| Deep link with a missing or malformed id | Ignore the add, render the current list, no error dialog |
| Large list (100+) | Render all; rows are cheap. Revisit only if it becomes slow in practice |
| Offline | Fully functional. There are no network calls |

#### 9. Acceptance criteria

1. Opening the section with nothing saved shows the empty state with a working link to Pieces — not a blank screen.
2. Adding a piece from the catalogue makes it appear at the top of the list.
3. Closing the app entirely and reopening it shows the same list.
4. Removing a piece removes it immediately, and it is still gone after a reload.
5. Adding the same piece twice results in one row.
6. With the device in airplane mode, the section renders the full list normally.
7. A piece with no image renders a placeholder tile, not a broken image.
8. With storage disabled in the webview, the section shows the notice and still works for the session.
9. Corrupting the stored value by hand results in an empty list, not a broken screen.
10. Fonts and colours match the surrounding app.

---

## Validation

- All four gap checks done and visible: no type, no `custom` feed, no `GBModuleTypeCustom` web view, empty store search on 2026-08-13.
- The gap carries **both** `alternatives[]` and `customCode{}`.
- `Bookmark` offered as a real first option with its cost (zero) stated, rather than dismissed on invented limitations.
- Storage surfaced as a decision, not chosen silently.
- Maintenance liability stated.
- `createRoute: null` on the Custom Code entry — Custom Code has no service, so no route can be derived from the tile pattern.
- No Custom Code widget placed outside Home.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-13",
  "summary": "Catalogue app for a ceramics studio with a personal wish list.",
  "sections": [
    {
      "order": 1,
      "name": "Pieces",
      "intent": "Browse the studio's catalogue",
      "status": "matched",
      "type": "GBModuleTypePhoto",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Photos",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Photo over Article because pieces are browsed visually. Switch to Article if each piece carries substantial written material."
    },
    {
      "order": 2,
      "name": "Wish list",
      "intent": "Each visitor builds a private list of pieces they'd like",
      "status": "gap",
      "type": null,
      "service": null,
      "alternatives": [
        {
          "type": "GBModuleTypeBookmark",
          "shortfall": "TRY THIS FIRST — auto-added, zero cost, and the pieces are in the app so the reference direction works. Whether the platform's own Favorites behaviour covers 'add, remove, come back later' was not asserted here; the studio should look before commissioning a build."
        },
        {
          "type": "GBModuleTypeSubmit",
          "shortfall": "Sends content to the owner for publication. A contribution pipeline, not a private list."
        },
        {
          "type": "GBModuleTypePhoto",
          "service": "custom",
          "shortfall": "Read-only and identical for every user. A custom feed cannot be written to from the app."
        }
      ],
      "storeSearch": {
        "searched": ["main catalog", "Memberships & Login"],
        "asOf": "2026-08-13",
        "result": "No extension offers a user-authored private list. Authentication supports per-user data but provides no list feature."
      },
      "customCode": {
        "type": "GBModuleTypePlugin",
        "service": null,
        "createRoute": null,
        "createRouteVerified": false,
        "specSection": "#custom-code-wish-list"
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "CONDITIONAL — build only if GBModuleTypeBookmark proves insufficient. On-device storage assumed; per-user sync would require the Authentication extension and a sign-up wall."
    }
  ],
  "extensions": [],
  "validation": {
    "sectionCount": 2,
    "warnings": [
      "GBModuleTypeBookmark should be evaluated before any build — it is already installed and may be sufficient. This plan does not assert its limits.",
      "Wish list storage location is a pending decision — on-device (assumed) vs per-user via Authentication.",
      "Custom Code is the studio's maintenance liability; GoodBarber does not support code it did not write.",
      "An in-place add button on each piece is not specified — Custom Code widgets are a Home-page surface only."
    ]
  }
}
```

## Sources

- `section-docs/0-section-type-codenames.md` — type enum and the `custom` service, back-office capture 2026-08-12.
- GoodBarber help — [Add custom code to your app](https://www.goodbarber.com/help/customize-your-app-with-developer-tools-r14/add-custom-code-to-your-app-a297/), cited via the superseded `app-structure` skill, not re-fetched 2026-08-13.
- Extension store search — [GoodBarber Extensions](https://www.goodbarber.com/extensions/), 2026-08-13.
