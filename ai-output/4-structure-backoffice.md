# App Structure in the GoodBarber Back Office

This report documents how an app's structure is defined and manipulated inside the GoodBarber back office, under **My App > Structure**. All findings come from direct inspection of the ReBook app's back office (`rebook.goodbarber.app/manage/app/content/`) and GoodBarber's own in-product help documentation, accessed on 2026-08-11. The goal is to establish precise, technical vocabulary — section, page, widget, menu — before this vocabulary is reused in the AI-integration case study.

## 1. Core Concepts

GoodBarber does not model an app as a set of "screens" in the generic sense. It models it as a tree of **sections**, arranged by a **navigation menu**, with one special section — **Home** — acting as a composable landing page.

- **App**: the top-level project (ReBook). One app corresponds to one entry in GoodBarber's backend, identified by a numeric `appId` (observed: `4603405`).
- **Section**: the atomic structural unit. A section is a self-contained feature — a content feed, a form, a social-media embed, a chatbot, etc. Every section is stored server-side as a JSON object with its own numeric `id` (e.g., `78648653` for the Podcasts section in ReBook) inside a global settings tree: `gbsettings.sections.<id>`. This was confirmed by opening a section's **Advanced settings**, which exposes a raw JSON-tree editor over the section's live configuration (fields observed: `id`, `contentSource`, `list`, `detail`, `icon`, `defaultThumb`, `border`, `infosTop`, `infosBottom`, etc.).
- **Page**: not a distinct object type in the data model — what the platform calls a "page" is really a *view* of a section. Most content-type sections expose exactly two pages: a **list/index view** (the feed) and a **detail view** (a single item). These are edited separately (see §4).
- **Menu**: the ordered, flat container that determines which sections appear in the app's primary navigation, and in what order.
- **Widget**: a smaller, composable building block used specifically to construct the Home section (see §4.1) and, to a lesser extent, other layout surfaces. Widgets are not sections — they cannot hold their own content, they reference or display content that already exists elsewhere.

Each section's content feed is served from a predictable internal endpoint pattern: `/front/get_items/{appId}/{sectionId}/`. This confirms that "structure" in GoodBarber is fundamentally a JSON document describing a set of sections plus a navigation ordering over them, rather than a collection of independently coded screens — a detail directly relevant to the AI-integration case study (§8).

## 2. The Structure Screen

**My App > Structure** (`/manage/app/content/`) is organized into four zones, always visible regardless of view mode:

1. **Header** — the app's top bar configuration, shared across all sections (not a section itself).
2. **Menu** — the ordered list of sections currently placed in the main navigation. In ReBook this holds three items: `Home`, `Artigos`, `Podcasts`, each preceded by a colored type icon. An inline **"Add a section"** control sits at the end of this list.
3. **Floating Button** — an optional, app-wide overlay control (off by default) that can trigger an action (e.g., open a section, dial a number) from any screen.
4. **Other sections** — a second list, explicitly described in the UI as *"sections used outside of the navigation."* By default this holds four platform-generated utility sections: `Favorites`, `Terms and conditions of sale`, `Privacy policy`, and `Settings`. These exist in the app (and can be linked to from widgets, buttons, or the menu) without occupying a navigation slot. The panel instructs: *"Drag a section to add it directly into or outside of your navigation,"* confirming that menu membership is just a placement, not a property fixed to the section itself.

Two interchangeable views are available for this screen:

- **List** view — a flat, vertically stacked list of sections, closest to a settings table.
- **Tree** view — a visual flowchart. Each section is rendered as a small phone-mockup node; content-type sections show a second, connected node representing their detail page (e.g., `Artigos → Article`, `Podcasts → Sound`). Green `+` buttons appear between nodes, allowing a new section to be inserted at a specific position rather than only appended at the end.

Every section, when opened, exposes a settings menu (via a `···` control) with a consistent set of actions: **Settings**, **Edit the content**, **Modify design**, **Hide**, **Advanced settings**, **See in the preview**, **Delete**. This four-way split — settings vs. content vs. design vs. raw JSON — recurs across every section type and is the platform's central authoring pattern.

## 3. Navigation Architecture

This section is sourced primarily from GoodBarber's own help article, *"Configure and design the navigation menu"* (My App > Structure > Menu), reached from the back office's built-in help panel.

GoodBarber offers **seven navigation modes**, grouped into two families plus two edge cases:

**A. Menu-style templates** (`Swipe`, `Little Swipe`, `Grid`, `Slate`) — drawer/side-menu patterns, opened via a button in the header. Each is divided into three placement zones:
- **Header**: page title, user account shortcut, links, shortcuts.
- **Main navigation**: the primary link list; can be broken up with `Separator` and `Title break` elements.
- **Footer**: account link, copyright notice, additional links/shortcuts.

**B. Bar-style templates** (`TabBar`, `Floating TabBar`) — displayed as a bottom bar on native apps, or as a banner beneath the header on the web app/PWA. Divided into two zones:
- **TabBar**: holds up to **5** direct links.
- **"Others" menu**: automatically created once a 6th link is added — the 5th TabBar slot becomes an overflow entry point into the remaining links. ReBook currently uses this mode (bottom bar: Home, Artigos, Podcasts).

**C. Edge cases**:
- **No menu**: displays no navigation chrome at all; a single designated section becomes the entire app.
- **Custom code**: bypasses the template system entirely — a developer authors the navigation in raw HTML.

Menus are built from a fixed vocabulary of **elements**: `Separator`, `Title break`, `Link` (to a page, action, or external URL), `Shortcut` (a named group of links), `Logo`, `My account` (deep-link to the user's profile), and `Copyright`. Which zones can hold which elements depends on the chosen template.

One easily-overlooked constraint: **section titles are truncated per navigation mode**. Documented limits — Grid: 13 characters, Slate: 20, Little Swipe: 12, all others (including TabBar): 32. A section named beyond this limit will have its label cut off in that particular navigation style, independent of the section's own `Title` field limit (also 32 characters, enforced at the section-settings level).

Finally: *"When you create a new section in your app, a link opening this section is automatically created in your navigation menu"* — section creation and menu-link creation are coupled by default; removing a section from the Menu (dragging it to "Other sections," or deleting it) is a separate, manual step.

## 4. Section Types Catalog

New sections are added from **My App > Structure > "+ ADD A SECTION,"** which opens a searchable catalog (`Find a feature`, sortable, defaulting to "Most popular"). ReBook's app currently reports:

> **7 / 120 sections used — you can still add up to 113 sections.**

This confirms a platform-wide ceiling of **120 section instances per app** (not just 120 distinct *types* — the same type, e.g. multiple `Link` widgets, can likely be added more than once, so the cap governs total section count, not type diversity). The catalog itself is dominated by third-party integrations rather than native building blocks. A representative, categorized sample of what was observed in the catalog (not exhaustive — the full list runs to ~120 entries):

| Category | Examples | Nature |
|---|---|---|
| AI-assisted | `Create with AI` (BETA) | Generates a section's content/layout via prompt |
| Native content | `Articles`, `Photos`, `Videos`, `Map`, `Events`, `Podcasts`, `Form`, `Menu`, `Submission`, `Search`, `About`, `Contact us`, `RSS feeds`, `Link` | First-party, list+detail content sections (see §5) |
| Custom feeds | `Article custom feeds`, `Video custom feeds`, `Photo custom feeds`, `Podcast custom feeds`, `Map custom feeds`, `Event custom feeds` | Pull external/custom data sources into a native template |
| Social platforms | `Facebook`, `Instagram`, `TikTok`, `X (Twitter)`, `Reddit`, `WhatsApp`, `Discord`, `Threads`, `Snapchat` | Embed or deep-link to a social presence |
| CMS / blogging | `WordPress`, `WP.com`, `Blogger`, `Medium`, `Squarespace`, `Substack` | Mirror an existing content platform |
| Audio/video hosting | `YouTube`, `Vimeo`, `Dailymotion`, `Spotify for Podcasters`, `Spreaker`, `Ausha`, `Simplecast`, `Podcast feeds`, `Video Podcast feeds`, `Live Audio`, `Live Video` | Streaming/podcast integrations |
| Commerce | `Shopify`, `Amazon`, `Etsy` | External storefront links |
| Forms / lead-gen | `Typeform`, `Airtable Form`, `JotForm` | Embedded third-party forms |
| Utilities | `Tawk.to` (live chat), `iCal/vCal` (calendar sync), `Flickr` | Miscellaneous integrations |
| GoodBarber's own suite ("WMaker") | `WMaker`, `WMaker TV`, `WM Events`, `WM Photos`, `WM Podcast` | GoodBarber's own hosted-CMS ecosystem |
| System / pre-added | `RAG Chatbot`, `Favorites`, `Settings` | Already present by default; shown greyed with an "Already added" badge |

A separate, larger catalog — the **Extensions Store** (its own sidebar entry, distinct from Structure) — exists for additional paid/installable features beyond this built-in list, implying two tiers of extensibility: the ~120 built-in section types available directly from Structure, and a broader marketplace layered on top.

## 5. Deep Dive: Content Sections (Artigos & Podcasts)

`Artigos` (an `Articles`-type section) and `Podcasts` (a `Podcasts`-type section) both follow the same underlying pattern, confirmed independently for each in their Tree-view diagrams and settings panels. This is GoodBarber's canonical **content section** template.

**Structural anatomy** (Tree view): `Header` → `[Categories]` → `Comments`, feeding into `List of {items}` (edit content | edit design), which itself feeds into a `{Item}` detail page (edit design only).

- **List of articles / List of sounds**: the feed/index view. Uniquely among the section's parts, it has *two* separate editable layers — **Edit the content** (the actual data: individual articles or audio episodes) and **Edit the design** (template and visual styling of the feed).
- **Article / Sound**: the single-item detail page. Only has **Edit the design** — its content is inherited from whichever list item was tapped, it has no independent content store.
- **Categories**: an internal taxonomy for organizing items *within* a section — not to be confused with app-level navigation. Both Artigos and Podcasts exposed a "Section categories" control showing a default category (`Categoria principal`) with an item count (6 articles; 1 podcast episode observed), plus an "Add a category" action. This is a one-level folder system scoped to a single section, separate from the Menu's cross-section ordering.
- **Comments**: a shared config block — `Internal comments` (toggle + display ordering: e.g. "From newest to oldest") or `Disqus comments` (external, toggled independently).
- **Type-specific settings**: e.g. Podcasts exposes a `Play settings` block (`Autoplay`, `Loop`) that Articles does not — confirming that, beyond the shared list/detail/categories/comments skeleton, each section *type* injects its own configuration fields.
- **Publication status**: a section-level draft/published toggle, observed in Artigos' settings.
- **Metadata**: every section carries a `Title` (32-char max) and `Description` (200-char max, used for SEO/PWA metadata per the Home-page documentation).

**When to use this pattern / audience / tips** (synthesized from the UI and GoodBarber's guidance):
- *Use it* for any editorially-curated, repeatedly-updated feed — blogs, news, episodic audio/video, changelogs. It is the wrong pattern for a single static page (use `About`/`Link`/custom code instead) or for content owned by an external CMS the user wants mirrored live (use the corresponding `*custom feeds` or platform-specific integration instead).
- *Audience*: content-driven apps (media, publishing, podcasting, community updates) — matches ReBook's own use case exactly.
- *Tips*: Categories should be planned before content entry, since they define the internal filtering/browsing structure end users will see; comments should be enabled deliberately since they add moderation overhead; the list/detail design split means visual changes to the feed do not require touching the detail page template, and vice versa — useful for iterating quickly without breaking the "reading" page.

## 6. Deep Dive: Home

Home behaves differently from every other section, and GoodBarber's own documentation is explicit about this distinction: *"You build your Home with widgets."* Home is not a content feed with a list/detail pair — it is a **composable landing page** assembled from an ordered stack of widgets.

Confirmed via the Home settings screen, ReBook's Home currently stacks three widgets top to bottom: a `Podcasts` widget, an `Artigos` widget, and a `Newsletter` widget, each individually toggleable (`Off`/`On`) and — for at least the content-referencing widgets — duplicable (a `Duplicate` action was observed, distinct from the section-level context menu in §2, which does not offer duplication).

**The seven available widget types** (from "+ Add a widget"):
- **Content** — embeds a live preview/feed of an *existing* section. Selecting this widget opens a **"Choose a section"** picker listing only sections that already exist elsewhere in the app (Artigos, Podcasts were the two options in ReBook) — Home cannot originate new content, it can only surface content owned by another section.
- **Link** — a manual call-to-action pointing to a page, section, or external URL.
- **Social links** — a row of icons linking to external social profiles.
- **Separator** — a purely visual spacing element.
- **Custom Code** — raw HTML/CSS/JS block for bespoke widgets.
- **Legal links** — shortcut to Terms/Privacy-type pages (ties back to the "Other sections" utility pages from §2).
- **Text** — static rich text.

**When to use it / tips**: Home is the only screen designed to *aggregate* — its entire purpose is to let a user see a slice of every other section without navigating away, plus surface actions (newsletter opt-in, external links) that don't belong to any single content section. Because the Content widget can only reference sections that already exist, Home should be configured *after* the primary content sections are created, not before. The platform also exposes dedicated Home-only settings for PWA/SEO meta tags and an option to disable the Home page entirely, redirecting the app's launch straight to another section.

## 7. Creating, Ordering, and Deleting Sections

**Creating a section**
1. Navigate to **My App > Structure**.
2. Click **"+ ADD A SECTION"** (global button) — or, in Tree view, click a green `+` insertion point to add a section at a specific position in the flow — or use the inline **"Add a section"** link at the end of the Menu list.
3. Search or browse the catalog (§4) and select a type.
4. The section is created, assigned a new numeric `id`, appended to the Menu by default, and a corresponding navigation link is auto-generated.
5. Configure its `Settings` (Title/Description/type-specific fields), then `Edit the content` to populate it, and optionally `Modify design`.

**Ordering sections**
- Within the Menu list, sections can be **drag-and-dropped** to change their order — this directly changes navigation order (and, for TabBar mode, which sections fall inside the visible bar vs. the "Others" overflow, per the 5-link cap in §3).
- The same drag interaction moves a section between the **Menu** (in-navigation) and **Other sections** (out-of-navigation) zones — navigation membership is a placement property, not a fixed attribute of the section.
- Tree view offers the same reordering visually, plus mid-sequence insertion via the green `+` nodes.

**Deleting / hiding a section**
- **Hide** (from the `···` menu) is a non-destructive visibility toggle — the section and its data persist but stop rendering in the app.
- **Delete** (red, from the same menu, and duplicated at the bottom of the section's own Settings panel) is destructive and irreversible from the UI.

## 8. Structural Limits Summary

- **120** total section instances per app; ReBook has used 7, leaving 113.
- **5** direct links per TabBar before overflow into an auto-generated "Others" menu.
- **32-character** default cap on a section's `Title` field; further truncated to 13–20 characters depending on the active navigation template (Grid/Slate/Little Swipe).
- **200-character** cap on a section's `Description` field.
- Menu nesting is effectively **flat**: the only "nesting" visible in Tree view is the intrinsic list→detail pairing of a content section, not arbitrary multi-level sub-menus.
- Home's `Content` widget can only reference sections that already exist — it cannot create new content sources.

## 9. Relevance to the AI-Integration Case Study

Three findings here matter directly for the Description/Implementation Agent architecture discussed elsewhere in this project (`ai-concept-docs/1-structure.md`):

1. **The platform is already JSON-native.** `gbsettings.sections.<id>` is a directly editable, well-typed configuration tree reachable from the UI itself (via "Advanced settings"). This substantially de-risks the "pre-structured schema" approach favored in the Description Agent design — the Implementation Agent's target schema does not need to be invented from scratch; it can map closely onto GoodBarber's existing internal section schema.
2. **Section types are a closed, enumerable catalog (~120 entries).** An agent selecting "what section to add" is a bounded classification problem (pick from a known list), not open-ended code generation — well-suited to constrained LLM output (e.g., function-calling against an enum of section types).
3. **Home's widget model is a natural target for an agent-generated "landing experience."** Since Home can only reference sections that already exist, any agent pipeline must sequence section creation before Home assembly — a concrete ordering constraint the Implementation Agent's task plan needs to respect.

---

*Sources: direct inspection of the ReBook back office at `rebook.goodbarber.app/manage/app/content/`, `.../app/home/`, `.../app/content-add/`, and `.../app/content-<id>-settings-fd/` (2026-08-11); GoodBarber in-product help articles "Configure and design the navigation menu," "Configure and design the Home page of your app," and "Design individual sections" (accessed via the back office's built-in help panel, help IDs 88/251, 87/250, and 89/106).*
