# Example 01 — Tour guide app

**What this example tests:** the happy path, and one trap inside it. Every intent matches an existing section. The trap is the photos intent, which reads like a gap and is not one.

## Input

> I am a tour guide in New York and I'd like to build an app to be used by the tourists. The app must have a page with news about New York, a photos section linked to an api with images of New York, a maps page with the location of interesting places and an informative section where I can upload any information.

## Must get right

- Four intents, four sections. No gaps.
- **Photos → `GBModuleTypePhoto` + `custom`.** Declaring a gap here is a failure. This is the `custom` service, the *Photo custom feeds* family.
- News → `Article` + `rss`, with the staleness caveat and the "no in-app editing" caveat.
- "Informative section where I can upload any information" → `Article` + `mcms`, because the user is authoring. Not `About` — "any information" over time implies repeating items.
- `sourceBinding` on both feed-backed sections, marked as a separate step.

## Must not do

- Route Photos to custom code.
- Suggest editing the RSS feed's articles inside GoodBarber.
- Assert a section-count limit.

---

# App Structure — New York Tour Guide

## Summary

A companion app for tourists on guided tours of New York: city news, a photo gallery from an existing image API, a map of points of interest, and an information section the guide maintains.

Four sections, all free. Two need a data source connected after creation.

## Sections

### 1. News — `GBModuleTypeArticle` + `rss`

City news pulled from a publisher. `Article` is the type for any feed of written items; `rss` is the service for a public feed where no dedicated connector exists.

- **Content is not editable in the app.** The feed owns the items — there is no "Edit the content" action on a connector-backed section. The guide curates by choosing the feed, not by writing posts.
- **Check the feed is alive before committing.** A publisher that stopped updating still returns a valid document full of old items; the section will look built and read as broken. Check the newest item's date against today.
- Many publishers syndicate headline plus summary only, with full articles behind a paywall. Expect teasers that link out.
- Suggested source: `https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml` — verify it's current before use.

*If the guide would rather write short city updates by hand, switch this to `mcms`. The source is swappable later without rebuilding the section.*

### 2. Photos — `GBModuleTypePhoto` + `custom`

A gallery fed by an existing image API. This is the *Photo custom feeds* family — `custom` exists on all six content types and is exactly the "point at your own data" case.

- **Prerequisite:** the API must expose JSON matching GoodBarber's Content API spec. If it doesn't yet, that adapter is the work — a thin endpoint reshaping the existing API's response.
- Not editable in the app; the feed owns the images.

### 3. Map — `GBModuleTypeMaps` + `mcms`

Points of interest with locations. `mcms` because the guide curates the list personally — that's the whole value of a guide's app.

- Plan categories before entering points if tourists should browse by theme (museums, food, viewpoints). Categories are section-scoped and retro-fitting them means re-filing every entry.
- If the locations already exist in Google My Maps, the `kml` service imports them instead.

### 4. Information — `GBModuleTypeArticle` + `mcms`

The guide's own notes: practical tips, meeting points, what to bring. `Article` with the built-in CMS, because the guide writes and updates these.

*Chosen over `About` deliberately: `About` is one static page. "Any information" over time is a growing set of items, which is a feed.*

## Extensions

None. Every intent is a section, and all four are free.

## Gaps

None.

## Validation

- All four types are verbatim from the enum.
- Both feed-backed services carry a `sourceBinding`.
- `custom` was checked before any gap could be declared — it matched, so no gap exists.
- Every price dated.
- No connector-backed section presented as in-app editable.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-13",
  "summary": "Companion app for tourists on guided tours of New York.",
  "sections": [
    {
      "order": 1,
      "name": "News",
      "intent": "News about New York from a publisher",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": "rss",
      "serviceVerified": true,
      "catalogEntry": "RSS feeds",
      "createRoute": "/manage/app/content-add-rss/",
      "createRouteVerified": true,
      "sourceBinding": {
        "required": true,
        "kind": "feedUrl",
        "suggested": "https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml",
        "note": "Bound server-side in section Settings. Verify the newest item's date before committing."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Feed-backed — no in-app content editing. Switch to mcms if the guide wants to write updates."
    },
    {
      "order": 2,
      "name": "Photos",
      "intent": "Gallery fed by an existing image API",
      "status": "matched",
      "type": "GBModuleTypePhoto",
      "typeVerified": true,
      "service": "custom",
      "serviceVerified": true,
      "catalogEntry": "Photo custom feeds",
      "createRoute": null,
      "createRouteVerified": false,
      "sourceBinding": {
        "required": true,
        "kind": "customFeedUrl",
        "suggested": null,
        "note": "Requires JSON matching GoodBarber's Content API spec. Budget an adapter if the API doesn't already emit it."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Not a gap — this is the custom feed service on the Photo type."
    },
    {
      "order": 3,
      "name": "Map",
      "intent": "Locations of interesting places",
      "status": "matched",
      "type": "GBModuleTypeMaps",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Map",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Guide-curated. Plan categories before entering points. kml service available if locations exist in Google My Maps."
    },
    {
      "order": 4,
      "name": "Information",
      "intent": "Guide's own notes and practical information",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Articles",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Article rather than About — 'any information' over time is a feed, not one static page."
    }
  ],
  "extensions": [],
  "validation": { "sectionCount": 4, "warnings": [] }
}
```

## Sources

- `ai-output/7-section-type-codenames.md` — type enum and service tables, back-office capture 2026-08-12.
- `ai-output/4-structure-backoffice.md` — list/detail model and categories, 2026-08-11.
