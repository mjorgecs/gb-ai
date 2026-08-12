---
name: app-structure
description: Plan and modify the structure of a GoodBarber app — which sections exist, what type each section is, how they are ordered in the navigation menu, and how the Home page is assembled from widgets. Use when a request concerns adding, removing, renaming or reordering screens; choosing the right section type for a requested feature; connecting an external content source; configuring the navigation menu; or building the Home landing page. Do NOT use for visual styling — colors, fonts, templates, launch screen (use app-design). Do NOT use to decide whether a capability must be installed before it can be used (use app-extensions).
---

# Structuring a GoodBarber App

## 1. Mental model

A GoodBarber app is **not** a set of hand-coded screens. It is a JSON document describing a set of **sections** plus a navigation ordering over them. Structuring an app means choosing section types and placing them — never authoring screens.

| Term | What it actually is |
|---|---|
| **App** | Top-level project, identified by a numeric `appId`. |
| **Section** | The atomic structural unit — one self-contained feature. Stored as `gbsettings.sections.<sectionId>`, with its own numeric `id`. |
| **Page** | Not a real object. A *view* of a section. Most content sections expose exactly two: a **list** view and a **detail** view, stored as sibling `list` and `detail` keys on the same section object. |
| **Menu** | An ordered, **flat** container deciding which sections appear in primary navigation. Membership is a *placement*, not a property of the section. |
| **Widget** | A composable block used to build **Home** only. Widgets cannot own content — they reference content that already exists elsewhere. |
| **Home** | A special section: a composable landing page assembled from a stack of widgets, not a list/detail pair. |

Section content is **not** stored in the section object. `contentSource.url` points at `/front/get_items/{appId}/{sectionId}/` — the JSON configures *how* a section renders; items are fetched separately at runtime.

Every section exposes the same four-way authoring split. Know which one a request targets before acting:

**Settings** (title, description, type-specific fields) · **Edit the content** (the data) · **Modify design** (visual template — hand to `app-design`) · **Advanced settings / `{EDITION}`** (raw JSON for this section)

**Feed-backed sections drop to three.** Where content comes from an external source (RSS, custom feeds, platform connectors), there is **no "Edit the content"** action — the data is owned by the source, not the app. Changing what appears means changing the feed URL in Settings, not editing items. Don't plan an authoring step that doesn't exist.

## 2. Preflight — do this before creating anything

1. **Read the current structure first.** Never add a section without knowing what already exists. A request often maps onto a section the app already has.
2. **Check the section budget.** The cap is **120 section instances per app** (instances, not distinct types — the same type may be added repeatedly).
3. **Check whether the capability needs installing.** If the required section type is not in the "+ Add a section" catalog, it is an extension question → hand to `app-extensions` **before** continuing.
4. **Plan the whole set of sections before creating any of them.** Home can only reference sections that already exist, so creation order is load-bearing (§6).

## 3. Routing: request pattern → correct section type

This is where structuring most often goes wrong. Match on the *shape of the data*, not on the noun the user used.

| Request pattern | Correct primitive | Why not the obvious alternative |
|---|---|---|
| Editorially-curated feed the owner updates (blog, news, changelog, episodes) | Native content section — `Articles`, `Videos`, `Photos`, `Podcasts`, `Events`, `Map` | — |
| "Pull in content from *\<a public news site / any site with a feed\>*" | `RSS feeds` section | Simplest path, but **no category filters and no comments**. Also **verify the feed is still being updated** — see §3.1. |
| "Pull in content from *\<my WordPress / Medium / Substack / YouTube / Vimeo…\>*" | The **platform-specific connector** for that service | Do **not** use RSS here. The dedicated connector supports category filters and comments; RSS does not. |
| "Pull in content from my own site / a custom backend" | `<Type> custom feeds` (Article / Video / Photo / Event / Map / Podcast) | Requires the source to expose JSON matching GoodBarber's Content API spec. Only choose this if that feed exists or can be built. |
| "Users submit/propose content" | `Submission` or `Form` | A content section is owner-authored; users cannot write to it. |
| "Users save items they like from the app" | `Favorites` / `Bookmark` | Already exists by default in most apps — check before adding. |
| "Users keep a wish list / list of things they *want*" | **Custom Code section** with on-device storage | Two tempting wrong answers, both confirmed wrong by their own store descriptions — see §3.2. |
| Single static page (about, legal, credits) | `About`, `Link`, or a Custom Code section | A content section is the wrong shape for one non-repeating page. |
| Contact details, address, hours | `Contact us` / `Map` | — |
| Onboarding / "show users what the app does" | **Not a section.** → `app-extensions` (App Walkthrough) | This is a first-launch overlay, not a screen in the navigation. |
| Bespoke interactive feature, or data from an arbitrary third-party API | Custom Code section → `app-extensions` first, then place it here | No pre-built type covers it. |
| Cross-section search | `Search` | — |
| Deep link to an external site or app | `Link` | Adds a nav entry without creating a screen. |

**Rule:** prefer a pre-built type over Custom Code whenever one fits. Custom Code is unsupported by GoodBarber's own team and is a maintenance liability — reach for it only when nothing in the catalog matches.

### 3.1 Validating an external feed before wiring it up

**A feed resolving is not a feed working.** Publishers routinely stop updating an RSS endpoint while leaving it online — it keeps returning HTTP 200 with a valid, well-formed document containing the last items it ever published. The section will build correctly, populate correctly, and look completely broken to end users because every headline is months or years old.

Before committing to a feed URL:

1. **Check the date of the newest item**, not just that the URL responds. This is the only check that matters.
2. **Compare it to today's date.** Anything older than the publisher's normal cadence means the feed is abandoned.
3. **If it's stale, say so before building** and offer alternatives: a different feed from the same publisher, a different publisher, or a custom feed against a live source.

Also worth confirming up front: many large publishers put their full articles behind a paywall and syndicate only headline + summary via RSS. That is the normal, intended use of a public feed, but it means the section will show teasers that link out rather than readable in-app articles. Set that expectation rather than letting the user discover it.

**Feed-backed sections and "populate with samples":** a live feed satisfies any "must contain N items" requirement automatically, since the items come from the source. A *stale* feed also appears to satisfy it — with dead content. Check dates, not counts.

### 3.2 Personal user-owned lists — the two decoys

A request for "users can keep their own list of X" attracts two near-miss primitives. Both are real features with real store listings, and both are wrong:

| Decoy | Its own description | Why it fails |
|---|---|---|
| **Bookmark / Favorites** | *"users mark and save the items that interest them most"* | Saves items **already in the app**. A wish list is precisely a list of things that are *not* in the app yet — the direction of reference is reversed. Also usually already installed by default, which makes it look like the intended answer. |
| **Submission** | *"user-generated content integrated into your app"* | The user submits **to the owner** for publication. It's a public contribution pipeline, not a private list the user can read back, reorder or delete. |

The distinguishing question is **who owns and reads the resulting data**:

- Owner authors, users read → content section.
- Users submit, owner publishes → Submission / Form.
- Users author, only that user reads → **no pre-built primitive exists; build a Custom Code section.**

**Storage then forces a second decision, so raise it before building:**

- **On-device** — works immediately, no login, no extra extension. But the list is per-device, doesn't sync, and is lost on uninstall.
- **Per-user account** — syncs and survives reinstalls, but requires the **Authentication** extension and puts a sign-up wall in front of the feature.

Neither is strictly better. State the trade-off and let the user choose rather than defaulting silently.

### 3.3 Swapping a section's source

A content section's source is **not fixed at creation**. Its Settings screen carries a `Source` block with a **Change source** control, which reopens the full source picker:

- **Internal:** the built-in CMS.
- **External:** the platform-specific connectors (WordPress, Blogger, WP.com, Squarespace, Wix, Medium, Substack, the vendor's own CMS), plus **RSS feeds** and **Custom**.

Two consequences worth planning around:

1. **A wrong or dead source is a cheap fix, not a rebuild.** Repoint the existing section — its id, title, description, placement, design and URL slug all survive. Never delete and recreate a section just to change where its content comes from.
2. **That picker is the routing table made concrete.** When unsure which source type a request maps to, open it and read the options rather than guessing — it is the authoritative list for that section type.

After swapping, **re-check the item dates** (§3.1) and **update the section's Description**, which will still describe the old source.

## 4. Creating, ordering, and removing sections

### Create

Target end-state per section:

- **Type** chosen via §3.
- **Title** — max **32 characters**, and see the navigation truncation table in §5. Titles are what users read in the menu; make them nouns, not sentences.
- **Description** — max **200 characters**. Used for SEO/PWA metadata, so write it for a human reader, not as a placeholder.
- **Content** populated (content sections only). A section created and left empty renders as a broken-looking blank feed.
- **Publication status** set — sections carry a draft/published toggle.

Two consequences of creation that must be handled explicitly:

- A new section is **appended to the Menu automatically**, and a navigation link is auto-generated with it. If the section should not be in the navigation, moving it out is a **separate, manual step** (§5).
- The section receives a new numeric `id`; anything referencing it (Home widgets, links) must use that id.

### Order

- Menu order is set by dragging within the Menu list. For bar-style navigation this also decides what falls inside the visible bar vs. the overflow (§5).
- Moving a section between **Menu** and **Other sections** is the same drag interaction — that is how a section exists in the app without occupying a navigation slot.
- Sections can also be inserted at a specific position rather than appended.

### Categories (within a section)

Content sections support a **one-level, section-scoped** taxonomy — do not confuse it with app-level navigation. Plan categories *before* entering content, since they define the filtering users will see and retro-fitting them means re-filing every item.

### Hide vs. Delete

- **Hide** — non-destructive. Section and data persist, stop rendering. Use this for anything seasonal, unfinished, or possibly-wanted-later.
- **Delete** — destructive and irreversible from the UI. Never delete on an ambiguous request; confirm explicitly, and prefer Hide when intent is unclear.

## 5. Navigation

Seven modes, in three families:

**Menu-style** (`Swipe`, `Little Swipe`, `Grid`, `Slate`) — drawer/side-menu. Three zones: **Header** (page title, account shortcut, links), **Main navigation** (the link list, breakable with `Separator` and `Title break`), **Footer** (account, copyright, extra links).

**Bar-style** (`TabBar`, `Floating TabBar`) — bottom bar on native, banner under the header on web/PWA. Two zones: the bar itself and an auto-created **overflow menu**.

> **The slot count is per-template, not a universal 5.** The documented figure for the standard `TabBar` is 5 slots. `Floating TabBar` was observed to have only **4**. The mechanism is the same either way:
>
> - sections **≤ slots** → every section gets its own direct tab;
> - sections **> slots** → the **last slot converts into an overflow entry** (a `•••` item), and *everything that doesn't fit behind it* — which is more than just the extra section.
>
> The step from "exactly full" to "one over" is therefore worse than it looks. On a 4-slot bar, going from 4 sections to 5 drops you from **4 direct tabs to 3**, because the 4th slot is consumed by the overflow control. A previously prominent section silently disappears into a menu.
>
> **Count the app's actual slots before adding a section to a bar-style menu**, and if the addition will cross the threshold, tell the user which existing section is about to be demoted and let them choose what stays visible.

**Edge cases** — `No menu` (one section becomes the whole app) and `Custom code` (navigation authored in raw HTML; see `app-extensions`).

Menu element vocabulary: `Separator`, `Title break`, `Link`, `Shortcut`, `Logo`, `My account`, `Copyright`. Which zones accept which elements depends on the template.

**Title truncation is per-mode and easy to miss.** The section `Title` field allows 32 characters, but the active navigation template may cut the label shorter:

| Mode | Label limit |
|---|---|
| Grid | 13 characters |
| Little Swipe | 12 characters |
| Slate | 20 characters |
| All others (incl. TabBar) | 32 characters |

If a bar-style mode is in use and there are more than 5 primary sections, decide deliberately which 5 belong in the bar — do not let the overflow be determined by creation order.

**Nesting is effectively flat.** The only hierarchy is a content section's intrinsic list→detail pairing. There are no arbitrary multi-level submenus; do not design a structure that assumes them.

## 6. Home

Home aggregates. Its entire purpose is to let a user see a slice of every other section without navigating away, plus surface actions that belong to no single section.

**Widget types:** `Content` (embeds a live feed of an **existing** section) · `Link` · `Social links` · `Separator` · `Custom Code` · `Legal links` · `Text`

Widgets are individually toggleable on/off, and content-referencing widgets can be duplicated.

**Hard ordering constraint:** the `Content` widget can only pick from sections that already exist. **Always create content sections first, assemble Home last.** Violating this produces a Home page with nothing to reference.

Home also carries its own PWA/SEO meta settings and can be disabled entirely, redirecting app launch straight to another section.

## 7. Constraints checklist

- **120** section instances per app.
- Bar-style slot count is **template-specific** (standard TabBar 5, Floating TabBar 4) — crossing it converts the last slot into an overflow and demotes more than one section. Count before adding (§5).
- **32** chars section title (further truncated to 12–20 by Grid / Little Swipe / Slate).
- **200** chars section description.
- Flat menu — no arbitrary nesting.
- Home widgets reference only pre-existing sections.
- Creating a section auto-creates a menu link; removing it from the menu is manual.
- Detail pages have no independent content store — content is inherited from the list item tapped.

## 8. Handoffs

- **A needed section type is missing from the catalog, or the feature is not a screen at all** → `app-extensions` first, then return here to place the result.
- **Section created and populated, now it must look right** → `app-design`.
- **Critical ordering rule when chaining:** global App Style is a destructive broadcast that overwrites section-level design. The safe pipeline is
  `app-extensions (install) → app-structure (create + place) → app-design (global theme) → app-design (per-section) → app-structure (assemble Home)`.

## 9. Verify before reporting done

- [ ] Every requested capability maps to exactly one section, or is explicitly deferred to another skill.
- [ ] No section left empty; content sections populated and published.
- [ ] For feed-backed sections: newest item's **date** checked against today, and any staleness reported to the user.
- [ ] Description filled (it drives SEO/PWA metadata) rather than left blank.
- [ ] Menu contains only what belongs in navigation; the rest moved to "Other sections".
- [ ] Titles fit the active navigation mode's character limit.
- [ ] If bar-style: slot count checked for this specific template, and if adding a section crossed the threshold, the resulting demotions were surfaced to the user rather than left as a surprise.
- [ ] Home assembled after its referenced sections exist.
- [ ] Section count still under 120.

---

*Sources: project reports `ai-output/4-structure-backoffice.md` and `ai-output/6-extensions-store.md` (direct back-office inspection, 2026-08-11); GoodBarber help — [Connect external content sources for articles](https://www.goodbarber.com/help/publish-and-manage-articles-r94/connect-external-content-sources-for-articles-a19/), [Create Custom Feeds](https://www.goodbarber.com/help/build-custom-content-feeds-r111/create-custom-content-feeds-a287/), [RSS Feed extension](https://www.goodbarber.com/extensions/rss/), [Add custom code to your app](https://www.goodbarber.com/help/customize-your-app-with-developer-tools-r14/add-custom-code-to-your-app-a297/).*
