# App Style, the `{EDITION}` Control, and the Underlying JSON Layer

This report covers two related but distinct layers of the GoodBarber back office: **App Style** (`My App > App style`), the global design system, and **`{EDITION}`**, a control that appears in the top-right corner of nearly every back-office screen and exposes the raw JSON configuration behind whatever is currently on screen. Findings are based on direct inspection of the ReBook back office and GoodBarber's in-product help documentation, accessed 2026-08-11. This report is a companion to `4-structure-backoffice.md` and assumes the section/page/widget vocabulary established there.

## 1. App Style: The Global Design System

GoodBarber's own documentation states this plainly: *"The App Style menu allows you to manage your app's overall design from a single location. All options set in this menu are applied globally to every section of your app."* App Style is reached from **My App > App style**, and is organized into two tiers: four **Essential Design** categories and five **Additional Options**.

Critically, the relationship between App Style and section-level design is **not** a quiet, CSS-like cascade where local overrides simply take precedence. GoodBarber's help documentation carries an explicit warning:

> **Important**: If you modify any option in the App Style menu, any design settings previously customized at the section level will be overridden. The new App Style settings will replace those section-specific designs and will apply to all sections of your app.

In other words, App Style is a **one-way, destructive broadcast**: pushing a global change wipes section-level customizations rather than merely being overridden by them. Section-level design settings (reached per-section via `Modify design`, see `4-structure-backoffice.md` §5) can diverge from the global style *until* the next global style save, at which point they are reset to match. This has direct implications for any automated agent workflow (§9).

### 1.1 Essential Design

- **Colors**: Built around a **color theme** — "a set of complementary colors applied globally across your app." Three ways to obtain one: pick a built-in preset, generate one automatically with the **Magic Palette** (an algorithmic/AI-assisted theme generator), or build one from scratch/by editing an existing palette. Beneath the theme, individual roles can be fine-tuned independently: header title/icon/background color, "primary colors" (a small numbered set — `#333333`, `#0C86D1`, `#666666`, `#FFFFFF` observed — used throughout the app), app background, menu background, enabled/disabled menu-item tint, list separator color, and per-level button text/background colors.
  *Use it / tips*: set the theme first, then fine-tune roles — going straight to per-role edits without a theme baseline produces inconsistent palettes across native vs. web renders, since some roles (e.g., `navBar` per-device background images, see §3) aren't exposed in the quick-access swatches and only surface once a theme exists to derive defaults from.
- **Fonts**: Governed by a **font theme** — three complementary font families applied together (e.g., ReBook's "Old Standard TT" theme pairs a serif display font with "Open Sans" for body text). Typography follows a fixed **eight-level hierarchy** (main title, headings 1–3, and further body/caption levels) so that titles, subtitles, and paragraph content stay visually consistent app-wide. A single **font-size slider** (`A-` to `A+`) proportionally rescales all eight levels at once for accessibility, while each level can still be edited individually (font family, weight, size per breakpoint, line height, letter spacing). Each font resolves to a concrete file, e.g. `/assets/googlefonts/OldStandardTT-Regular.ttf` — fonts are sourced from Google Fonts and self-hosted per app.
  *Tips*: use the global slider for accessibility-driven resizing; touch individual levels only for genuine hierarchy exceptions (e.g., a stat callout), since editing every level by hand defeats the point of a theme.
- **Buttons**: A shared **corner-radius preset** — `Square` / `Rounded` / `Round` — plus a **three-tier button hierarchy**: Level 1 (filled/primary), Level 2 (outlined/secondary), Level 3 (text-only/tertiary, present but unstyled by default in ReBook). This same Square/Rounded/Round triad reappears verbatim under Thumbnails-and-cells and Form fields, confirming "shape" is a single cross-component design token rather than a button-specific setting.
  *Tips*: pick the shape token once, early — it silently governs buttons, thumbnails, and form fields together, so changing it later reshapes the whole app's visual language at once.
- **Form fields**: Shares the Square/Rounded/Round shape token, plus a field **size** (Small/Medium/Large, i.e. row height/padding) and label placement (`Title up` — label above the field — vs `Title in` — floating/inline label).

### 1.2 Additional Options

- **Thumbnails and cells**: The Square/Rounded/Round shape token again (scoped to image thumbnails and list cells), plus **mouseover effects on pictures** — `None`, `Zoom in`, `Zoom out`, `Opacity` — a hover-state affordance relevant to the web/PWA render (irrelevant on native touch devices, but still configured here).
  *Tips*: mouseover effects only matter for the web app; native apps ignore this setting, so don't spend design time tuning it if the app targets native-only distribution.
- **Spacing**: A single **Margins** control exposing four numeric fields (16px on each side by default in ReBook), described as creating "a frame around content elements." This one control writes to (at minimum) three related JSON keys — `gutter`, `gutterDesktop`, `gutterTablet` — confirming spacing is breakpoint-aware even though the UI presents one shared value by default.
- **Haptic feedback and animations**: Contains three genuinely platform-conditional settings, each explicitly labeled: **opening effects in a list** (e.g. "Content appears from the left") is flagged *"only available on native iOS and Android apps"*; **haptic feedback** (vibration on interaction) is likewise native-only; **scroll effects** (elements reveal as the user scrolls) is flagged **PWA only**. This is the one App Style category where the setting's *availability* — not just its value — depends on which build target (native vs. web/PWA) is being configured.
- **Icons**: A large, individually-restylable **functional icon set**, grouped by role: Navigation (menu, back, back-down, close, list-view toggle), Toolbar (overflow menu, comment, share, text size +/-, bookmark add/remove, add-event, purchase), Localisation (route, address, map-view), Time-of-day (all-day, time), Search (search, clear), and more below the fold. These are *chrome* icons (UI affordances), distinct from the small colored icons assigned to individual sections in Structure (e.g., Podcasts' purple speaker icon) — the two icon systems are configured in different places and serve different purposes.
- **Background and separators**: App-wide background **color** plus optional background **image**, with separate uploads for **portrait** and **landscape** orientation; and a single **separator color** used for list dividers, form-field underlines, etc. app-wide.

### 1.3 Themes Library

A separate tile, **Themes Library** (`My App > Themes Library`), presents a full gallery of complete, pre-built visual themes — ReBook's active theme is named "Guet Apens" — each shown with a name, a short color-swatch preview, and (implicitly) a full mockup. Applying a theme is a bulk operation: it writes into the same App Style settings cataloged above (colors, fonts, buttons, shape, spacing, etc.) in a single action, functioning as a fast-start preset layer on top of the same underlying design system rather than a separate mechanism.

## 2. The `{EDITION}` Control

`{EDITION}` appears, consistently positioned top-right, on nearly every back-office screen: the My App landing page, every App Style category page, the top-level Structure screen, and every per-section screen (Settings, `Modify design`, and the list/detail template editors). On some narrower screens it is abbreviated to a bare `{}` icon rather than the full `{EDITION}` label, but it is the same control.

**What it is**: clicking `{EDITION}` does not open a distinct editing *mode* in the sense of a different visual editor — it opens a **live, directly-editable raw JSON tree view** of the configuration node underlying whatever screen you invoked it from. This is functionally the same screen reachable from a section's `···` menu via **Advanced settings** (§2 in `4-structure-backoffice.md`) — `{EDITION}` is simply that same raw-JSON inspector, surfaced contextually everywhere rather than only in one menu.

**What it is not**: it is unrelated to `Modify design`. `Modify design` opens a WYSIWYG template picker and visual-property canvas (color swatches, font pickers, template thumbnails); `{EDITION}` opens the raw data those visual controls write to. They are two different views onto the same underlying object — one for humans editing visually, one for direct data manipulation.

**Scope / granularity**: `{EDITION}`'s scope is fixed at two levels, not one-per-screen as might be expected:
- Invoked from **My App** or any **App Style** category page, it opens the **global design-token subtree** — top-level keys observed include `backgroundColor`, `buttonStyle`, `buttons`, `categories`, `comments`, `cookies`, `designComponents`, `floatingButton`, `gutter`/`gutterDesktop`/`gutterTablet`, `icons`, `margin`, `navBar`, `notFound`, `restrictedContent`, `searchBar`, `separatorColor`/`separatorType`, `shape`, `standbyscreen`, and more. Notably, **no `sections` key is present in this scope** — global style and section/content structure live in separably-scoped subtrees, even though both are wrapped in a root object labeled `gbsettings`.
- Invoked from **anywhere inside a specific section** — its Settings panel, its `Modify design` diagram, or even a specific sub-page's template editor (e.g. the `Sound` detail-page canvas) — it always opens the **same full section object**, `gbsettings.sections.<sectionId>`, regardless of which sub-screen triggered it. It does not narrow further to just the sub-screen you were on; e.g. opening it from the `Sound` page's template editor still shows the entire Podcasts section, including its `list` (feed) config alongside the `detail` (single-item page) config you were actually editing.

This confirms `{EDITION}` is best understood as a **context-aware JSON inspector with exactly two effective scopes** (app-global vs. current-section), not a per-screen or per-widget inspector.

One documentation curiosity worth noting: an older help-article screenshot for the Home page labels this same control "JSON" (with left/right navigation arrows next to it) rather than "EDITION," suggesting the control was renamed at the UI layer at some point while its function stayed the same.

## 3. The JSON Itself

### 3.1 What language is it?

It is **plain JSON** — not CSS, not Swift, not any standardized, publicly-documented format. It is GoodBarber's own **proprietary internal configuration schema**, editable directly through the back office's tree UI (each node has an editable key and, for leaf nodes, an editable value, with a `Save` button at the bottom).

That said, its vocabulary borrows recognizable conventions from a few places:
- **CSS-flavored value strings** for visual properties: colors as hex (`"#00042A"`), or CSS keywords like `"transparent"`, `"solid"`, `"center"`, `"lighter"`. These are string *values*, not CSS syntax — there is no selector/declaration-block structure anywhere in the tree.
- **Native-SDK-flavored key/enum naming** for structural/template properties. The clearest example: the `Sound` detail page's `detail.contentTemplate` key holds the literal value `"GBSoundContentTemplateTypeBanner"` — a PascalCase, `GB`-prefixed identifier that reads exactly like an Objective-C/Swift class or enum-case name from GoodBarber's native iOS/Android rendering SDKs, and maps 1:1 to the "ToolBar Up Banner" option selected in the visual template picker. This strongly suggests the JSON exposed here is not a UI-only abstraction but the **actual configuration payload consumed by GoodBarber's native app runtimes** (and, presumably, an equivalent web renderer), with the back office acting as a structured editor over that payload rather than a separate description of it.

In short: it is GoodBarber's own JSON-based configuration DSL, JSON in syntax, CSS-adjacent in some of its leaf vocabulary, and native-SDK-adjacent in its structural/enum vocabulary.

### 3.2 Structure

The tree is deeply nested and strongly typed by convention (though nothing enforces this beyond the rendering engine that consumes it). Patterns observed:

- **Responsive/per-breakpoint fields**: font objects carry `desktopSize`, `tabletSize`, and a base mobile `size` side by side (e.g. `descFont: { color, desktopSize: 20, fontType: "Old Standard TT", letterSpacing: 0, size: 16, tabletSize: 18, urlFont: "/assets/googlefonts/OldStandardTT-Regular.ttf" }`); the navigation bar carries separate background-image fields per device class (`backgroundImageIpad`, `backgroundImageIphone6`, `backgroundImageIphone6plus`).
- **Content-source pointers, not embedded content**: a section's feed is not stored as literal data in this tree — it's a pointer. `contentSource.url` resolves to an internal REST-style endpoint, `/front/get_items/{appId}/{sectionId}/`, confirming the JSON tree configures *how* a section renders, while the actual items (articles, episodes) are fetched separately at runtime.
- **List/detail split, mirrored in the schema**: exactly matching the UI pattern documented in §5 of `4-structure-backoffice.md`, a content section's object contains both `list` (feed-level settings: `listBackgroundColor`, etc.) and `detail` (single-item page settings: `audioPlayer`, `background`, `border`, `contentTemplate`, `coverBordersEnabled`, `coverRadius`, `equalizerColor`, and more) as sibling keys.
- **Flat scalar settings alongside deep objects at every level**: a single section object mixes simple flags (`id`, `borderColor`, `listBackgroundColor`) directly with deeply nested sub-objects (`contentSource`, `list`, `detail`) at the same nesting depth — there is no strict separation between "simple" and "complex" configuration.

### 3.3 How can it be manipulated?

- **Directly, in place, through the back office itself.** Every leaf node in the tree is an editable text field; the tree can be expanded/collapsed node by node via `+`/`−` toggles, and a `Save` button at the bottom commits changes. No code editor, export/import, or copy-paste-a-blob mode was found — editing is strictly field-by-field within the rendered tree, not via pasting a replacement JSON document.
- **Indirectly, through every normal back-office screen**, which is the intended path — App Style pages, section Settings, and `Modify design` canvases are all just structured forms that read and write into this same tree. A colour picked in the Colors screen and the corresponding hex string in the `{EDITION}` view are the same underlying value, edited through two different interfaces.
- **Risk profile**: because `{EDITION}` writes directly to the live configuration with a single `Save`, it bypasses whatever validation the friendlier form-based screens might apply (dropdowns constrained to valid options, color pickers producing well-formed hex strings, etc.). Free-text editing of a field like `contentTemplate` could plausibly set a value the visual template picker would never offer, with unpredictable rendering results — this was not tested, but is a reasonable inference from the free-text nature of every field observed.

## 4. Summary: Where Each Layer Lives

| Layer                            | Reached from                                 | Scope                                                             | Editing mode                                                 |
| -------------------------------- | -------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------ |
| App Style                        | My App > App style                           | Whole app (all sections)                                          | Visual forms; one-way overrides section-level design on save |
| Section design (`Modify design`) | Structure > section > `···` or click-through | One section (list + detail together)                              | Visual template picker + property forms                      |
| `{EDITION}` (global)             | My App / App Style root                      | `gbsettings` global design subtree (no `sections` key)            | Raw JSON tree, field-by-field                                |
| `{EDITION}` (section)            | Any screen within a section                  | `gbsettings.sections.<id>` (entire section, list+detail together) | Raw JSON tree, field-by-field                                |

## 5. Relevance to the AI-Integration Case Study

Three findings here extend the conclusions of `4-structure-backoffice.md` §9:

1. **The override-not-merge behavior of App Style is a real hazard for an automated agent.** An Implementation Agent that applies section-level customizations first and a global theme second (or vice-versa, carelessly) will silently destroy work. Any agent pipeline that touches both layers needs an explicit ordering rule — almost certainly: apply the global App Style/theme once, early, then layer section-specific design on top, and avoid re-touching App Style afterward without re-applying section overrides.
2. **`{EDITION}`'s JSON is very plausibly the same payload an Implementation Agent would target**, not merely an inspection tool for humans. The presence of native-SDK-style enum values (`GBSoundContentTemplateTypeBanner`) suggests this schema is close to (or identical to) the actual runtime configuration contract — making it a strong candidate for direct programmatic writes rather than driving the visual UI. This reinforces the "pre-structured JSON" design favored for the Description→Implementation Agent handoff: the target schema doesn't need to be invented, and may be able to reuse GoodBarber's own key names directly.
3. **Free-text field editing with no visible validation is a two-edged sword for automation.** It means an agent *can* write arbitrary configuration directly (fast, flexible), but also that nothing in this interface would stop it from producing an invalid or unsupported combination (e.g., a `contentTemplate` value the rendering engine doesn't recognize). Any agent writing directly to this layer should validate against a known-good enum list before saving, since the back office itself does not enforce one at this layer.

---

*Sources: direct inspection of the ReBook back office at `rebook.goodbarber.app/manage/app/appstyle/`, `.../app/colors/`, `.../app/fonts/`, `.../app/design-buttons/`, `.../app/design-fields/`, `.../app/design-thumbnails/`, `.../app/design-spacing/`, `.../app/design-haptics/`, `.../app/design-icons/`, `.../app/design-background/`, `.../design/themes/`, `.../app/design-78648653/`, `.../app/design-78648653-page/`, and the `{EDITION}`/Advanced-settings JSON tree reached from each (2026-08-11); GoodBarber in-product help article "App style: Essential design settings" (help ID 87/317, accessed via the back office's built-in help panel).*
