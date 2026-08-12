---
name: app-design.
description: 'Style a GoodBarber app — global App Style design tokens (color theme, font theme, shape, spacing, icons, background), pre-built themes, per-section visual templates, the launch/splash screen, and direct edits to the underlying design JSON via the {EDITION} / Advanced Settings inspector. Use when a request concerns how the app looks or feels: "make it modern", branding, palette, typography, rounded vs square, list templates, animations, haptics, splash screen. Do NOT use to decide which screens exist or how navigation is ordered (use app-structure). Do NOT use to install a capability (use app-extensions).'
---

# Styling a GoodBarber App

## 1. The one rule that must be read first

> **App Style is a one-way destructive broadcast, not a CSS cascade.**
> Saving any option in the global App Style menu **overwrites** design settings previously customized at the section level. Section-level design does not "win" over global — it is silently reset.

Therefore the only safe order is:

```
1. Global App Style / theme   ← apply ONCE, early
2. Per-section design         ← layer on top
3. Do not return to step 1 without re-applying step 2
```

If a request requires changing a global token after per-section work exists, state the consequence and either re-apply the section overrides afterwards or get confirmation first. Never silently re-save App Style mid-task.

**Reading is safe; saving is not.** App Style screens (Colors, Fonts) commit only on an explicit **Apply**, which then raises a confirmation stating the change *"will be applied throughout your application and its design will be completely modified."* That sentence is the override warning — treat it as such. Opening a screen to inspect values changes nothing, but an `Apply` clicked out of habit — even with no edits — re-broadcasts and wipes section-level design. Once section work has begun, inspect App Style read-only and navigate away.

**Section design screens behave differently: they auto-save.** A `Modify design` screen has no Apply button — each change commits as you make it, and the preview updates live. So there is no "cancel" safety net at section level, but equally no risk of an accidental global broadcast from there.

**Magic / Genius Palette is an AI feature.** If the task prohibits using the platform's AI tooling, pick a built-in theme or set colors by hand instead.

## 2. Where each layer lives

| Layer | Scope | Editing mode |
|---|---|---|
| **Themes Library** | Whole app — bulk-writes all App Style values at once | Gallery of complete pre-built themes |
| **App Style** (`My App > App style`) | Whole app, every section | Visual forms; overwrites section design on save |
| **Section design** (`Modify design` on a section) | One section — list **and** detail together | Template picker + property forms |
| **Launch Screen** (`My App > Launch Screen`) | Native app startup only | Image uploads or generator wizard |
| **`{EDITION}` — global scope** | `gbsettings` design subtree (**no `sections` key**) | Raw JSON tree, field by field |
| **`{EDITION}` — section scope** | `gbsettings.sections.<id>` (entire section, list+detail) | Raw JSON tree, field by field |

`{EDITION}` (the `{}` control in the top-right of most screens, identical to a section's **Advanced settings**) has exactly **two** effective scopes, not one per screen. Opening it from a detail-page template editor still returns the *whole* section object, `list` config included.

`{EDITION}` is **not** an alternative to `Modify design`. `Modify design` is a WYSIWYG editor; `{EDITION}` is the raw data those controls write to. Same object, two views.

## 3. Routing: request pattern → correct lever

| Request pattern | Correct lever | Notes |
|---|---|---|
| "Make it look modern / better / more professional" (no specifics) | **Themes Library first**, then fine-tune tokens | A complete pre-built theme sets colors, fonts and spacing coherently in one action. Hand-assembling a palette from scratch is slower and produces worse results. Use **Live preview** before committing (§4.1). |
| "Use these brand colors" | App Style > **Colors**: set the theme, *then* fine-tune roles | Never start with per-role swatches — some roles only derive sane defaults once a theme exists. |
| "I don't know what colors to use" | Magic / Genius Palette (algorithmic palette generator) | Generates a complementary set rather than guessing. |
| "Change the fonts" | App Style > **Fonts**: pick a **font theme** (3 complementary families) | Fonts resolve to self-hosted Google Fonts files. |
| "Text is too small / accessibility" | The global **A− / A+ size slider** | Rescales all 8 type levels proportionally. Editing levels by hand defeats the hierarchy. |
| "Rounded corners / softer look" | The shape setting — set it in **all three** places: Buttons, Thumbnails and cells, Form fields | These are **three independent settings**, not one shared token. Changing one leaves the others untouched. See §4.2. |
| "Change the list layout / how articles are displayed" | The section's **`Modify design`** template picker | Section-scoped, not global. List and detail templates are edited independently. |
| "More breathing room / tighter layout" | App Style > **Spacing** (Margins) | One UI control, breakpoint-aware — writes `gutter`, `gutterDesktop`, `gutterTablet`. |
| "Add a background image / change app background" | App Style > **Background and separators** | Separate uploads for portrait and landscape. |
| "Change the back / share / bookmark icons" | App Style > **Icons** (functional chrome icon set) | Distinct from the small per-section icons assigned in structure — different system, different place. |
| "Add animations / make it feel alive" | App Style > **Haptic feedback and animations** | Availability is build-target-dependent — see §5. |
| "Beautiful launch / splash screen" | `My App > Launch Screen` — **not** App Style | Native plans only. See §6. |
| "Change one specific value the UI doesn't expose" | `{EDITION}` raw JSON | Last resort; no validation. See §7. |

## 4. App Style reference

### Essential design

- **Colors** — built on a **color theme** (a complementary set applied globally). Three ways to obtain one: a built-in preset, the **Magic/Genius Palette** generator, or hand-building. Beneath the theme, individual roles are tunable: header title/icon/background, a small numbered set of primary colors, app background, menu background, enabled/disabled menu-item tint, list separator, and per-level button text/background.
- **Fonts** — a **font theme** of three complementary families, over a fixed **eight-level type hierarchy** (Main title, Headings 1–6, Normal). See §4.3 — the font themes are a short, mostly serif-led list, and the per-level controls have important gaps.
- **Buttons** — its own shape setting (§4.2) plus a **three-tier hierarchy**: Level 1 filled/primary, Level 2 outlined/secondary, Level 3 text-only/tertiary. Level 3 renders as bare tinted text; either style it deliberately or leave it unused.
- **Form fields** — its own shape setting (§4.2), plus **size** (Small/Medium/Large) and label placement (`Title up` vs `Title in`).

### Additional options

- **Thumbnails and cells** — its own shape setting (§4.2), scoped to images and list cells, plus **mouseover effects** (`None`, `Zoom in`, `Zoom out`, `Opacity`) — web/PWA only, ignored on native.
- **Spacing** — Margins, four numeric fields forming a frame around content.
- **Haptic feedback and animations** — see §5.
- **Icons** — the functional chrome icon set, grouped by role: Navigation (menu, back, close, list-view toggle), Toolbar (overflow, comment, share, text size, bookmark, add-event, purchase), Localisation, Time-of-day, Search.
- **Background and separators** — app-wide background color and optional image (portrait + landscape uploads), plus a single separator color used for list dividers and field underlines.

### 4.1 Applying a theme safely

Theme application is a bulk write with **no undo**. The flow gives two chances to stop, and both should be used:

1. Selecting a theme opens a dialog offering **Live preview**, **Apply theme**, or Cancel. Always take Live preview first.
2. In Live preview, the **left/right arrows cycle between themes**, not between screens — so this is a side-by-side comparison tool. Use it to sanity-check the shortlist against the app's real content before choosing.
3. Confirming shows a second, red confirmation dialog. Red is the platform's destructive-action styling — it is warning about the section-design overwrite in §1, not about the theme itself.

After applying, **audit what the theme actually wrote** rather than assuming. A theme sets colors and fonts reliably, but may leave other tokens (notably shape, §4.2) at their previous values — so the result can be an inconsistent blend of the old and new design.

### 4.2 Shape — three settings that must be synced by hand

`Square` / `Rounded` / `Round` appears verbatim under **Buttons**, **Thumbnails and cells**, and **Form fields**. Despite identical wording, these are **three independent settings**.

> Verified empirically: setting Buttons to `Rounded` left Thumbnails and Form fields on `Round`. There is no shared token and no cascade.

Treat shape as one *decision* applied in three places:

1. Decide the value once.
2. Set it on all three screens.
3. Re-read all three to confirm — a freshly applied theme can leave them already divergent.

Two related cautions:

- **A theme may not touch shape at all.** Do not assume applying a theme normalized it.
- **Some chrome renders its own radius regardless.** A floating tab bar's active-item pill, for example, keeps its own shape and does not follow any of these three settings. Don't chase it here.

### 4.3 Setting a specific typeface

Font **themes** are a short list and skew serif-display. If the brief names a typeface or a style the themes don't cover (e.g. a system-UI sans throughout), do **not** settle for the nearest theme — set the levels individually.

Each of the eight levels has its own family dropdown, which opens a **searchable picker over the full Google Fonts library**. Two traps:

1. **Changing a level's family resets its weight to Regular 400.** Always re-set the weight immediately after changing the family, on every level you touch. It is silent — nothing warns you.
2. **The global Fonts screen exposes no per-level pixel size.** The only size control there is the proportional **A− / A+ slider**, which rescales all eight levels together. So "large title, normal body" is *not* achievable from App Style.

Per-level pixel sizes **are** editable — but only inside a section's `Modify design` screen, where each text role has its own size slider. Consequence for planning: a display-scale typography change is **section-level work** and must therefore happen *after* all global work (§1), not as part of it.

### 4.4 Colour fields worth knowing

- **"Header Title and Icons" is one combined value.** You cannot give the nav bar a dark title and a tinted action icon — they share a colour. If a tinted icon would force an odd title colour, keep the title legible and put the accent elsewhere (menu, buttons, section-level accents).
- **"Enable menu" is the active navigation item; "Disabled menu" is the inactive one.** For a tinted-active / grey-inactive bar, set Enable to the accent and Disabled to a mid grey.
- Every colour field takes a **typed hex value**, so exact brand or system palettes can be entered directly rather than eyedropped.

## 5. Build-target-conditional settings

The only category where a setting's *availability* — not just its value — depends on the build target:

| Setting | Available on |
|---|---|
| Opening effects in a list | Native iOS/Android **only** |
| Haptic feedback | Native iOS/Android **only** |
| Scroll reveal effects | PWA **only** |
| Mouseover effects on pictures | Web/PWA only (silently ignored on native) |

Establish the app's distribution target before spending effort here. Tuning hover states for a native-only app is wasted work.

## 6. Launch screen

Lives at **`My App > Launch Screen`** — a separate entry, *not* inside App Style. It is the image shown while a **native** iOS/Android app loads (native plans only).

Two paths:

- **Splashscreen tab** — upload prepared images. Minimum sizes: **iOS 1242 × 2688**, **Android 1440 × 2560**, **Tablet 2048 × 1536 landscape**, ~72 dpi. Larger images can be cropped; smaller ones get black padding.
- **Wizard tab** — generate all required formats in the back office from a title, baseline, font/color/effects, and a background color or image. Prefer this when brand assets are not already prepared, then click **Generate**.

Design guidance that materially affects retention: images are **cropped, not distorted**, to fit each device — keep anything important well inside the safe center. Avoid small text near the bottom edge. Optimize file weight; mobile network quality is not constant. Consider signalling that the app is loading rather than showing a static logo alone.

## 7. Editing the design JSON directly

The configuration is **plain JSON** in GoodBarber's own proprietary schema — not CSS, not a public standard. Its vocabulary borrows from two places:

- **CSS-flavored leaf values**: hex colors (`"#00042A"`), keywords like `"transparent"`, `"solid"`, `"center"`, `"lighter"`. These are string values only — there is no selector/declaration structure anywhere.
- **Native-SDK-flavored keys and enums** for structural/template properties, e.g. a detail page's `contentTemplate` holding a PascalCase `GB`-prefixed identifier that maps 1:1 to an option in the visual template picker. This strongly suggests the JSON is the actual payload consumed by the native runtimes, not a UI-only abstraction.

Patterns to expect: per-breakpoint fields side by side (`size` / `tabletSize` / `desktopSize`; per-device navbar background images), the `list`/`detail` split mirrored as sibling keys, and flat scalars mixed with deep objects at the same nesting depth.

**Manipulation is field-by-field only** — expand the tree, edit leaf values, Save. There is no paste-a-blob or import/export mode.

**Risk profile — read before writing here.** `{EDITION}` writes straight to live configuration and **bypasses the validation the form-based screens provide** (constrained dropdowns, well-formed color pickers). Free-text editing a field like `contentTemplate` can set a value the picker would never offer, with unpredictable rendering. Rules:

1. Prefer the visual controls. Use `{EDITION}` only for values the UI does not expose.
2. Validate any enum-like value against a known-good list before saving — nothing at this layer will stop an invalid one.
3. Note that raw JSON access is itself a **toggleable extension** ("Advanced edition"), not a universal built-in. If `{EDITION}` is absent, that is an `app-extensions` question, not a bug.

## 8. Handoffs

- **The request is about which screens exist or menu order** → `app-structure`.
- **`{EDITION}` / raw JSON access is unavailable, or a design-asset library is needed** (custom fonts, icon packs, stock photography, animation files) → `app-extensions`.
- **Ordering when chaining:** run global styling **after** sections exist and **before** any per-section design work.

## 9. Verify before reporting done

- [ ] Global theme applied **before** any per-section design work — not after.
- [ ] Theme previewed via Live preview before committing.
- [ ] Theme's actual output audited, not assumed — every token re-read after application.
- [ ] Shape set explicitly on **all three** screens (Buttons, Thumbnails and cells, Form fields) and re-read to confirm.
- [ ] If a specific typeface was required: every one of the eight levels set, and **each level's weight re-set after** the family change (families reset weight silently).
- [ ] Display-scale type sizing done at section level, not attempted from the global Fonts screen.
- [ ] All three button tiers styled, or tier 3 deliberately unused.
- [ ] Build target confirmed before configuring native-only or PWA-only settings.
- [ ] Launch screen: all required formats present, key content inside the safe crop area.
- [ ] Any raw-JSON edit validated against a known-good value, and justified by the UI not exposing it.
- [ ] No section-level customization silently destroyed by a late App Style save.

---

*Sources: project report `ai-output/5-appstyle-edition-json.md` (direct back-office inspection, 2026-08-11); GoodBarber help — [Customize the launch screen of your app](https://www.goodbarber.com/help/shop/app-style-and-branding-r87/customize-the-launch-screen-of-your-app-a104/), [App style: Essential design](https://www.goodbarber.com/help/shop/app-style-and-branding-r87/app-style-essential-design-a317/), [App style: Additional options](https://www.goodbarber.com/help/app-style-and-branding-r87/app-style-additional-options-a412/), [Add custom code to your app](https://www.goodbarber.com/help/customize-your-app-with-developer-tools-r14/add-custom-code-to-your-app-a297/).*
