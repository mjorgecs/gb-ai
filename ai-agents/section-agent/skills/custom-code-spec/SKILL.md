---
name: custom-code-spec
description: "Write a developer-ready specification for a GoodBarber Custom Code section when no existing section type or extension covers a described feature. Use only after section-routing has confirmed a genuine gap — no matching type, no custom feed service, and no extension found in the store. Produces a nine-part specification detailed enough to build from without further questions, covering the data model, external API contract, rendering, storage, GoodBarber App API integration, edge cases and acceptance criteria. Owns the constraints of the Custom Code environment: one self-contained index.html, client-side secrets, on-device versus per-user storage, and the maintenance liability."
---

# Custom Code Specification

The gap path. You are here because nothing in the platform covers the feature, and a developer now has to build it.

## 1. Confirm the gap before writing anything

Writing a spec for something that already ships is the most expensive mistake this agent can make. Four checks, all of them:

- [ ] **No type fits.** Checked against the full enum in `section-routing` §2 — matching on data shape, not on the user's noun.
- [ ] **No `custom` feed fits.** If the feature is a read-only list of uniform items and the type is one of the six content types, `service: custom` covers it. See `content-sections` §4. *This is the check that gets skipped.*
- [ ] **No `GBModuleTypeCustom` fits.** If the thing already exists as a web page, form or widget, a web view embeds it in one step. See `utility-sections` §4.
- [ ] **No extension exists.** Searched the correct store, read candidate descriptions rather than counting hits. See `extensions-pricing`.

Only when all four fail is this a gap.

**What `custom` genuinely cannot do**, and so what legitimately lands here: anything **interactive, per-user, or mutable**. A wish list, a calculator, a booking flow, a quiz, a filterable view over a third-party API that doesn't match the Content API spec. The test isn't "is the data external" — it's "is this a read-only feed of uniform items". If no, it's a gap.

**Say the liability out loud when you recommend this.** GoodBarber does not debug code it did not write — including embeds and iframes. Custom code is entirely the app owner's maintenance burden. That sentence belongs in the report, not just in your reasoning.

## 2. What you are specifying

A **Custom Code section**: `GBModuleTypePlugin`, no service.

Constraints that shape every spec:

| | |
|---|---|
| **One screen** | No list/detail pair. Everything happens on one screen; multi-view flows are managed in JavaScript, not by the platform. |
| **One file** | The editor opens a single `index.html`. Write it self-contained, with inline `<style>` and `<script>`. Extra files can be uploaded, but one file is what's maintainable. |
| **Standard web** | HTML, CSS, JavaScript. No build step. |
| **App API** | GoodBarber's in-app JavaScript API is how the section reaches native capability. |
| **Real preview** | The back-office preview actually executes the code, including outbound `fetch` — it's a genuine test surface. |

There are three other Custom Code variants — a **widget** (a fixed-height block on Home), a **navigation mode**, and a **menu section template**. They are not interchangeable with a section. If the feature belongs on the Home page rather than on its own screen, say so and specify the widget instead, noting that its height is fixed and identical across desktop PWA and native mobile.

### What the App API gives you

Worth knowing, because it decides what's feasible: on-device storage (offline-capable), data associated with an authenticated user, adaptation by subscription status, geolocation and opening native map apps, native sharing, system alerts, and connectivity detection.

**Design tokens are contested.** One source says a custom section inherits the app's global App Style automatically; another says tokens are not inherited and the palette must be restated in CSS. Specify defensively: restate the palette and font stack in the CSS, and note that if inheritance works, the restatement is harmless. Do not assert either behaviour as fact.

## 3. The two decisions to force before writing

Both have real cost and neither has a right default. Put them to the user rather than choosing silently.

### Storage: on-device or per-user

| | On-device | Per-user account |
|---|---|---|
| Setup | Nothing. Works immediately. | Requires the **Authentication** extension |
| Login | None | Sign-up wall in front of the feature |
| Sync | No — per device | Yes, across devices |
| Survives reinstall | No | Yes |

For a wish list, a saved-items feature, or anything personal, this is *the* design decision. State the trade-off; let the user pick.

Whichever is chosen: guard storage access in `try/catch` and degrade to in-memory with a visible notice. A webview can have storage disabled, and a silent failure looks like data loss.

### API keys: is this key safe to ship?

Anything in a Custom Code section **ships to the client and is readable by any user**. A key placed there is not secret.

- **Acceptable** for keys that are free, read-only and rate-limited.
- **Not acceptable** for anything billable, writable, or tied to private data — that needs a server-side proxy, which is a bigger project and must be named as such.

Say which case applies. Never specify a key in client code without stating that it's public.

When the user supplies the key: specify it as a **single named constant at the top of the script**, in a comment banner saying where to get it and what changes once set. Also check what the API does **without** a key — many free tiers respond unauthenticated but silently clamp page size or filters. Specify behaviour for both states, so a capped result doesn't look like a bug.

## 4. The specification template

Nine headings, in this order. A developer should be able to build from it without asking a question.

### 1. Purpose

One paragraph: what the section does, who uses it, why nothing pre-built covers it. Name the alternatives that were rejected and why — this is what stops someone rebuilding your reasoning from scratch.

### 2. Screens and flow

Every state the user can be in and every transition between them. Since a Custom Code section is one screen, these are JavaScript view states, not pages. Specify what the user sees **first**, before any data loads.

Minimum states to account for: initial load, loaded with data, loaded empty, error, and any interaction state (adding, editing, confirming).

### 3. Data model

Every entity, every field, every type, and which are required. Give a concrete example object, not just a schema — an example resolves ambiguity that prose doesn't.

```
Item
  id          string, required, unique
  title       string, required, max 120 chars
  imageUrl    string, optional, absolute https URL
  addedAt     ISO 8601 timestamp, required
```

### 4. External contract

If the section calls an API: endpoint, method, authentication, request shape, response shape, and a **real example payload**. Rate limits, CORS behaviour and terms of use — confirm the API is callable from a client-side context, because many aren't.

If there is no external API, say so explicitly and specify local persistence instead. An omitted section reads as an oversight.

### 5. Rendering

The HTML structure — containers, list item markup, controls — and the CSS approach. Specify the loading state, the empty state and the error state as concrete markup, not as afterthoughts; they are what the developer will otherwise skip and what the user will otherwise see.

Restate the palette and font stack here (§2).

### 6. State and persistence

What survives a reload and what doesn't. Where each piece lives — in memory, on device, per user. The storage decision from §3, with its consequence stated: *"the list is per-device and lost on uninstall"* is a sentence the app owner needs to read.

### 7. GoodBarber integration points

How the section is opened (menu entry, deep link, Home widget). Which App API capabilities it uses and what happens when one is unavailable. Whether it needs the user's login state or subscription status — and therefore whether **Authentication** or **Memberships** is a prerequisite, with the cost from `extensions-pricing`.

### 8. Edge cases

Empty result. Network failure. Slow response. Malformed or unexpected data. Storage disabled. Missing API key. Very long text or very large images. Each with the specified behaviour, not just the risk.

### 9. Acceptance criteria

A numbered checklist a developer ticks off. Each item observable — something you could watch someone demonstrate.

```
1. Opening the section with no saved items shows the empty state, not a blank screen.
2. Adding an item persists it; reopening the app shows it still there.
3. Removing an item removes it immediately and after reload.
4. With the device offline, the section renders saved items and shows an offline notice.
5. A malformed API response shows the error state rather than a blank screen.
```

## 5. Reference implementations

Two Custom Code sections already exist in this repo and are the target shape and level of finish:

- `ai-output/gatos-custom-code/index.html` — an external-API-backed section.
- `ai-output/lista-desejos-custom-code/index.html` — a wish list, which is the canonical worked answer for the personal-list gap.

Point at these in the spec. A developer reading a real file learns the conventions faster than from any description.

## 6. Before emitting a spec

- [ ] All four gap checks in §1 done — particularly the `custom` feed check.
- [ ] The maintenance liability stated in the report body.
- [ ] `alternatives[]` present too — a gap answer needs both halves, never just the spec.
- [ ] Correct variant chosen: section, widget, navigation mode or menu template.
- [ ] Storage decision surfaced as a choice with its trade-off, not decided silently.
- [ ] If an API key is involved: stated as public, and the free/read-only test applied.
- [ ] Behaviour specified both with and without a key, if the API works either way.
- [ ] All nine headings present. An empty one says "not applicable and why", never nothing.
- [ ] A concrete example object in the data model, and a real example payload in the contract.
- [ ] Loading, empty and error states specified as markup.
- [ ] Prerequisites named with cost — Authentication for synced data, Memberships for gated content.
- [ ] Acceptance criteria observable, not aspirational.

---

*Sources: the superseded `app-extensions` skill (Custom Code variants, the CodeMirror single-`index.html` editor, App API capabilities, the client-side-secret and storage cautions, the maintenance-liability rule — back-office inspection 2026-08-11, `ai-output/6-extensions-store.md`); GoodBarber help — [Add custom code to your app](https://www.goodbarber.com/help/customize-your-app-with-developer-tools-r14/add-custom-code-to-your-app-a297/) and [App API documentation](https://app.goodbarber.dev/v2/documentation/), both cited via the superseded skill and not re-fetched on 2026-08-13.*
