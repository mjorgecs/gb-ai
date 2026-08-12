---
name: app-extensions
description: Identify which GoodBarber Extension Store extension a requested capability needs, check its availability constraints (free, plan-gated, paid add-on, already installed, experimental), install it, and instantiate it in the app. Use when a requested feature is not covered by an existing section type — onboarding walkthroughs, memberships and paywalls, authentication, push, monetization, analytics, chat, automation connectors, design-asset libraries, or any custom-coded feature. Use also when a needed control appears missing from the back office, since some core capabilities are themselves toggleable extensions. Do NOT use to place or order screens already available (use app-structure) or to style the app (use app-design).
---

# Extensions: Identify, Install, Instantiate

## 1. Mental model

> **The section catalog is what you can add as a navigable screen. The Extension Store is everything you can add to the app, full stop.**

The section types offered under "+ Add a section" are a **subset** of the Extension Store — specifically its **Content** collection (the integrated CMS). The store carries ~190 extensions in total; the remainder are things that are *not* screens: service integrations, account and permission systems, monetization, notifications, analytics, design-asset libraries, and raw developer primitives.

Consequence: **"there is no section for this" does not mean "the platform cannot do this."** Always check the store before concluding a capability is unsupported or reaching for custom code.

**Categories:** Content · Memberships & Login · Monetization · Notifications · Essentials · Productivity · Tools for developers · Lab

## 2. The three-step procedure

> **The store search is fuzzy — a hit count is not a match.** Searching a capability word can return a dozen results whose descriptions have nothing to do with it (a search for a list-management feature returned CMS, video and AI extensions). Never conclude "something exists" from the result count; **read each candidate's own one-line description** and check it describes the actual behaviour requested. Equally, a search returning nothing relevant is a legitimate finding — report it and move on to building.

### Step 1 — Identify

Ask **"what kind of thing is this?"**, not "what did the user call it?":

| The capability is… | Look in |
|---|---|
| A screen showing owner-authored content | Content — but this is likely already a section type → `app-structure` |
| Something that happens *around* the app rather than as a screen (onboarding, login, paywall, push, ads) | Memberships & Login / Monetization / Notifications |
| A connection to an outside service | Productivity / Essentials |
| A visual asset the app doesn't have (fonts, icons, stock imagery, animations) | Design assets (cross-category) |
| Bespoke behavior no pre-built feature covers | Tools for developers → the Custom Code family |
| A back-office control that seems to be missing | Check installed extensions — it may simply be disabled (§5) |

### Step 2 — Check constraints before promising anything

An extension being listed does **not** mean it is available to this app. Five distinct states exist, and they must be surfaced to the user rather than assumed:

| State | Meaning | What to tell the user |
|---|---|---|
| **Free** | Available on all plans. Majority of the catalog. | Proceed. |
| **Plan-gated free** | Free to use, but unlocked only from a given subscription tier upward. | Name the required tier before proceeding. |
| **Flat annual add-on** | A recurring yearly fee, sometimes shown at a promotional rate. | Quote the price and note the list price if discounted. |
| **Installed by default** | Already active without anyone choosing it. | Do not "install" — verify it is enabled and configure it. |
| **LAB** | Experimental/beta. | Flag the maturity risk before recommending. |
| **In test until \<date\>** | Time-boxed trial currently running. | State the expiry date — the capability lapses without action. |

**Never recommend or invoke an extension without stating its constraint state.** Uniform availability is a false assumption and a common failure mode.

**Read the pricing line, not the availability badge — they can contradict each other.** A store listing may show a bare **"Free"** chip in search results and **"Available in all plans"** on the install bar, while the detail page's full pricing line reads *"Fees for the Standard and Premium offers. Free with the Pro offer."* "Available" means installable, **not** free. Always open the detail page and quote the full pricing line before installing; if it implies a possible charge, get explicit confirmation rather than deciding on the user's behalf.

### Step 3 — Install, then instantiate

Installing is rarely the finish line. Two integration mechanisms exist, and a given extension may use either or both:

**A. Section-based.** The extension appears as a new entry in "+ Add a section" and behaves exactly like a native section — configure, place in the menu, style. Hand off to `app-structure`.

**B. Sidebar console over the same section mechanism.** More complex extensions get their own top-level sidebar entry. Opening it may not present a settings form at all, but an empty state prompting you to add a section. The sidebar entry is a **management console layered on the same section mechanism** — not a parallel system. Structurally it still lives in the app's structure once instantiated.

**C. Direct config screen under an existing menu.** Some extensions are neither sections nor sidebar consoles: installing them adds a new entry under an existing menu (typically `My App`) and drops you straight into its editor. Nothing is added to Structure, and there is no section to create. App-wide behaviours that aren't screens — onboarding overlays, launch-time experiences — take this form.

> **Do not assume mechanism A.** Before planning an "install then add a section" sequence, install and observe where the extension actually lands. Mechanism C needs no instantiation step at all, and planning one wastes a cycle looking for a section that will never exist.

> **The most common failure here:** treating "installed" as "working." Billing-level installation and functional instantiation are separate steps. An extension can appear installed in the management screen while the app contains no instance of it and users see nothing.

Installed extensions are tracked centrally in the store's **Management** screen ("Your extensions"), showing each one's status — an enable/disable toggle for some, a price/trial badge for paid ones, an installed-by-default label for the baseline set — with removal available per row.

## 3. Routing: request pattern → extension family

| Request pattern | Extension family | Notes |
|---|---|---|
| "Show new users how the app works" / onboarding / guided tour | **App Walkthrough** (Memberships & Login) | See §4 — it has specific limits worth knowing before promising a design. |
| "Users need accounts / log in" | Authentication | Prerequisite for anything per-user. |
| "Paid subscriptions / premium content / paywall" | Memberships | Plan-gated. Load-bearing — other extensions depend on subscription state. |
| "Sell individual items" / tips / donations | Monetization (coupons, loyalty/club cards, tipping — several are paid or LAB) | Check pricing state carefully; this category has the most non-free entries. |
| "Show ads" | Advertising networks / internal ad server | — |
| "Send notifications to users" | Notifications | Also drivable conversationally via the MCP integration. |
| "Users chat with each other" / community | Chat, Community, User groups | — |
| "Connect to \<external SaaS\> / automate a workflow" | Zapier, Make, or the public APIs | Prefer an existing connector over custom code. |
| "Track usage / see stats" | Analytics + dashboard extensions | Usually **installed by default** — verify before installing. |
| "Use our brand font / better icons / stock photos / animations" | Design-asset libraries (custom font, icon packs, stock photography, animation files) | Install here, then apply via `app-design`. |
| "A gallery/feature pulling from \<arbitrary third-party API\>" | **Custom Code section** (Tools for developers) | See §5. Nothing pre-built covers an arbitrary API. |
| "A custom block on the home page" | **Custom Code widget** | Fixed height across all form factors — decide the height up front. |
| "A completely custom menu / navigation" | **Custom Code navigation mode** or **Custom Code menu section** | High maintenance cost; prefer a standard navigation mode. |
| "I need a setting the back office doesn't show" | **Advanced edition** | This is the raw-JSON `{EDITION}` inspector — itself an extension (§5). |
| "Mirror content from my existing CMS/site" | The platform-specific connector, or a custom feed | → `app-structure` routing table; these install as sections. |

## 4. App Walkthrough — constraints worth knowing up front

Because "show users what the app does" is a common request and is frequently mis-implemented as a section:

- It is a **first-launch overlay**, not a screen in the navigation. It is displayed **only the first time** a user opens the app after installing. Do not place it in the menu.
- **Mobile only** — the editor states this explicitly. It will not appear on the web app, so don't promise it for a PWA-only project.
- Installs via **mechanism C** (§2): it appears as `My App > Walkthrough` and opens its editor directly. There is no section to add.
- **Maximum 5 screens.** Each takes an **image *or* an animation file**, plus a title and a description.
- Navigation chrome is fixed: a main action button, a pager, and a **Skip** button — users cannot be blocked. The button reads **"Next"** on every step except the last, which reads **"Get started."** Because of that final label, a closing "get started" screen is redundant — spend the budget on content instead.
- **Two templates, and the choice is a legibility decision:**
  - **Immersive** — the image fills the screen and the title/description sit *on top of it*. Text is easily unreadable over busy or light-toned photography. Only viable with dark, low-detail images.
  - **Polaroid** — the image sits in a card with the text below it on the background colour. Legible with any photograph. **Default to this** unless the imagery is specifically chosen for overlay.
- It carries **its own typography and colour settings**, which inherit the app's font family but **not** the app's text colours. Expect to re-set title colours by hand to match the rest of the app.

**Write the copy in the app's own language.** The walkthrough's chrome (Skip / Next / Get started) is auto-localised to the app's locale. Copy written in a different language from that chrome looks broken. Check the rendered buttons in the preview to confirm which language the app is actually running in before writing.

Practical implication: with 5 screens and forced skippability, a walkthrough should cover the app's *core value* and one or two primary actions — not enumerate every section.

## 5. The developer primitives

### The Custom Code family

Four distinct variants — pick the one matching the surface, they are not interchangeable:

| Variant | Surface | Instantiation |
|---|---|---|
| **Custom Code section** | A full screen in the app | Install → a section is added → title it → **`···` menu > Edit the content** opens the code editor |
| **Custom Code widget** | A block on the Home page | Add as a Home widget → **set a fixed height** (identical across PWA desktop and native mobile) → choose whether it scrolls → add code |
| **Custom Code navigation mode** | The app's main menu | Select the custom-code navigation template, then author the menu |
| **Custom Code menu section** | A menu-type section's template | Add a menu section, select the custom-code template, then author it |

All four use standard **HTML / CSS / JS** and interact with the app through GoodBarber's **App API** (available inside the app) — with a separate **Public API** for workflows outside it.

**The editor, concretely.** It is a CodeMirror instance over a single `index.html`, with syntax highlighting, line numbers, a light/dark toggle, a "Download the file" action, and an upload box for additional plugin files (executables are ignored). A Custom Code section is **one screen** — it has no list/detail pair, so the Tree view shows a single node.

Practical notes for authoring:

- **Write one self-contained `index.html`** with inline `<style>` and `<script>`. That is the file the editor opens by default and the simplest thing to maintain.
- **Typing long code into the editor by hand is error-prone** — auto-indent and bracket auto-closing will corrupt it. Compose the file separately and paste or upload it, then read it back to confirm the saved length and a couple of landmark lines.
- **The back-office preview really executes the code**, including outbound `fetch`. That makes it a genuine test surface: verify the rendered result and interactions there rather than assuming.
- Custom Code sections do **not** inherit the app's design tokens automatically. Restate the palette and font stack in CSS if the section should match the rest of the app.

What custom-coded features can do through the App API: store data on-device (offline-capable), associate data per authenticated user, adapt content by subscription status, query geolocation and open native map apps, trigger native sharing and system alerts, detect connectivity, and inherit the app's global App Style automatically — so a custom section can match the rest of the app's typography, colors and spacing without restating them.

**Three cautions before choosing custom code:**

1. **GoodBarber does not debug code it did not write.** This includes embeds and iframes. Custom code is entirely the app owner's maintenance liability. Always prefer a pre-built extension when one fits.
2. **A legacy toolkit exists.** Sections built before the current App API still work and need no migration, but that older interface is no longer extended or documented. Write new work against the current App API.
3. **External API calls carry their own constraints** — keys, CORS, rate limits, and terms of use. Confirm the target API is reachable from a client-side context and that any credential handling is acceptable before committing to the approach.

**Storing per-user data in custom code.** On-device storage needs nothing installed and works without login, but is per-device and lost on uninstall. Anything that must sync across devices or survive a reinstall needs the **Authentication** extension as a prerequisite — check whether it is installed before promising synced data. Guard storage access in `try/catch` and degrade to in-memory with a visible notice, since a webview can have storage disabled.

**Handling API keys in custom code.** Anything in a Custom Code section ships to the client and is readable by any user — a key placed there is **not secret**. That is acceptable for keys that are free, read-only and rate-limited; it is not acceptable for anything billable, writable, or tied to private data, which needs a server-side proxy instead. Say which case applies rather than pasting a key in silently.

When the user will supply the key themselves, make it findable: declare it as a **single named constant at the top of the script**, wrapped in a comment banner that states where to get the key and what changes once it is set. Then tell them the **exact line number**, and verify that line after saving — editors reformat.

Also check what the API does **without** a key. Many free tiers still respond unauthenticated but silently clamp parameters (page size, filters, extra fields). Build so the section works either way, and describe the degraded behaviour rather than letting a capped result look like a bug.

### Advanced edition

The raw configuration inspector (`{EDITION}` / Advanced settings) is **itself an installable, toggleable extension**, not a universal built-in. If raw JSON access is missing from the back office, install or enable it here. Unlike most entries it carries an enable/disable toggle rather than removal only. Once active, use it via `app-design` — and heed the no-validation warning there.

## 6. Baseline expectations

Every app ships with a set of pre-installed extensions nobody explicitly chose — typically covering stock photography, analytics and tag management, SEO metadata, palette generation, statistics dashboards, custom fonts, animation assets, offline support, custom domain, and the MCP integration.

**Check the Management screen before installing anything.** Recommending the installation of something already active is a visible error and wastes a step.

## 7. Scope boundary: building vs. operating

The platform separates these deliberately, and any agent design should preserve the split:

- **Building** — creating new features from a description. Handled by in-platform AI feature generation, scoped to the Custom Code API surface. Good for bespoke small-to-medium interactive widgets that map to no existing section type; **not** a replacement for a CMS section on data-heavy content.
- **Operating** — running an already-built app: CRUD on existing sections' items, push campaigns, analytics. Handled by the MCP integration, with a real permission model (per-module × read-only/read-write). It does **not** create sections or alter structure and design.

Do not assume an operations interface can perform structural work, or vice versa.

## 8. Handoffs

- **Extension installed and it materializes as a section** → `app-structure` to configure, place, and populate it.
- **Extension provides design assets, or raw-JSON access has just been enabled** → `app-design`.
- **The capability turned out to be a plain section type after all** → `app-structure` directly; no installation needed.

## 9. Verify before reporting done

- [ ] Checked the Management screen first — the extension was not already installed or enabled.
- [ ] Constraint state read from the detail page's **full pricing line**, not the search-result chip or the "available in all plans" badge — and stated to the user, with confirmation obtained if a charge is possible.
- [ ] Integration mechanism observed rather than assumed (section / sidebar console / direct config screen).
- [ ] Installation followed by **instantiation where the mechanism requires it** — the capability is actually present in the app, not merely billed.
- [ ] Any user-facing copy written in the app's own language, verified against the auto-localised chrome.
- [ ] Custom code chosen only after confirming no pre-built extension fits, with the maintenance-liability caveat stated.
- [ ] For custom code: correct variant chosen for the surface; widget height fixed if applicable; external API constraints checked.
- [ ] Dependencies satisfied — anything per-user requires authentication; anything premium-gated requires memberships.
- [ ] Downstream skills invoked where the extension needs placement or styling.

---

*Sources: project report `ai-output/6-extensions-store.md` (direct back-office inspection, 2026-08-11) and `notes/goodbarber-mcp-study.md`; GoodBarber help and product pages — [App Walkthrough extension](https://www.goodbarber.com/help/content-general-information-r93/app-walkthrough-extension-a418/), [App Walkthrough](https://www.goodbarber.com/extensions/walkthrough/), [Add custom code to your app](https://www.goodbarber.com/help/customize-your-app-with-developer-tools-r14/add-custom-code-to-your-app-a297/), [Custom Code section](https://www.goodbarber.com/extensions/custom-code-section/), [App API documentation](https://app.goodbarber.dev/v2/documentation/), [Extensions overview](https://www.goodbarber.com/extensions/).*
