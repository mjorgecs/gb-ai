# App Structure — New York Tour Guide

A tourist companion app for a New York guide: news, a photo gallery, a map of places, and one static info page.
Four sections, all matched — no gaps.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-25",
  "summary": "A companion app for tourists in New York: city news, a photo gallery, a map of points of interest, and an info page the guide maintains.",
  "sections": [
    {
      "order": 1,
      "name": "New York News",
      "intent": "A page with news about New York",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": null,
      "serviceVerified": false,
      "catalogEntry": null,
      "template": {
        "list": "GBArticleListTemplateTypeEnriched",
        "detail": "GBArticleDetailTemplateTypeToolBarUp"
      },
      "templateVerified": true,
      "notes": "The type is settled; the source is not stated. If you write the news yourself, the service is 'mcms' (the only option where content is editable in the app). If you pull it from a publisher, it is 'rss' — feed-backed sections have no 'Edit the content' action, many publishers syndicate headline-plus-summary only, and whoever binds the feed should check the date of the newest item, not just that the URL responds. Templates left at the defaults, which also survive an unreliable image supply better than a grid or an immersive list would."
    },
    {
      "order": 2,
      "name": "Photos of New York",
      "intent": "A photos section linked to an API with images of New York",
      "status": "matched",
      "type": "GBModuleTypePhoto",
      "typeVerified": true,
      "service": "custom",
      "serviceVerified": true,
      "catalogEntry": "Photo custom feeds",
      "template": {
        "list": "GBPhotoListTemplateTypePinterest",
        "detail": null
      },
      "templateVerified": true,
      "notes": "Requires a JSON endpoint matching GoodBarber's Content API spec — confirm this exists, or that the image API can be wrapped in one. The feed URL is bound server-side in the section's settings, not in the section JSON, and content cannot be authored in-app. No detail template family was captured for Photo; that is a gap in my tables, not a statement that none exists."
    },
    {
      "order": 3,
      "name": "Places to See",
      "intent": "A maps page with the location of interesting places",
      "status": "matched",
      "type": "GBModuleTypeMaps",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Map",
      "template": {
        "list": "GBMapsListTemplateTypeEnriched",
        "detail": "GBMapsContentTemplateTypeBanner"
      },
      "templateVerified": true,
      "notes": "'mcms' assumed because you curate the places yourself — if they already live in a Google My Map, the 'kml' service takes the exported KML file instead. Defaults kept; the Enriched list shows each place's address, which is what most people want from a map. Maps also has a third template family (GBMapsDetailTemplateType…) whose purpose is not understood, so nothing was emitted for it. If you later want a slideshow of photos per place, the documented 'Visual' list template covers that."
    },
    {
      "order": 4,
      "name": "Good to Know",
      "intent": "An informative section where I can upload any information",
      "status": "matched",
      "type": "GBModuleTypeAbout",
      "typeVerified": true,
      "service": null,
      "serviceVerified": true,
      "catalogEntry": "About",
      "template": null,
      "templateVerified": false,
      "notes": "One non-repeating page you edit directly — right if the information is a single body of text. If it is really a set of separate tips or guides that grows over time, that is a second GBModuleTypeArticle section with 'mcms' instead. No template vocabulary was captured for this type."
    }
  ],
  "extensions": []
}
```

## Before you build

- Where does the New York news come from — do you write it, or pull it from a publisher's feed? That decision picks the service and whether you can edit posts in the app.
- The image API needs to expose JSON matching GoodBarber's Content API spec; confirm it does, or that something can serve that shape.
- Confirm whether the info page is one page or a growing set of entries.
