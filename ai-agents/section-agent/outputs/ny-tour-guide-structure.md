# App Structure — New York Tour Guide

A mobile app for tourists visiting New York with news updates, a photo gallery of NYC landmarks, an interactive map of points of interest, and informational pages. Four matched sections.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-25",
  "summary": "Tourist guide app for New York featuring news, photos, map locations, and information pages.",
  "sections": [
    {
      "order": 1,
      "name": "News",
      "intent": "News and updates about New York for tourists",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Articles",
      "template": {
        "list": "GBArticleListTemplateTypeEnriched",
        "detail": "GBArticleDetailTemplateTypeToolBarUp"
      },
      "templateVerified": true,
      "notes": "Content authored directly in GoodBarber. Enriched template shows author and publication details, suitable for editorial news updates."
    },
    {
      "order": 2,
      "name": "Photos",
      "intent": "Gallery of images of New York landmarks and attractions",
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
      "notes": "Connected to your API. Requires a JSON endpoint matching GoodBarber's Content API spec. Photo detail template was not captured. Pinterest template shows mixed aspect ratios for a varied image collection."
    },
    {
      "order": 3,
      "name": "Interesting Places",
      "intent": "Map of locations and points of interest in New York",
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
      "notes": "Locations authored in GoodBarber. Enriched list shows addresses inline; Banner detail displays location imagery. A third Maps detail family exists but is undocumented."
    },
    {
      "order": 4,
      "name": "Information",
      "intent": "Informational pages the guide author can upload",
      "status": "matched",
      "type": "GBModuleTypeAbout",
      "typeVerified": true,
      "service": null,
      "serviceVerified": true,
      "catalogEntry": "About",
      "template": null,
      "templateVerified": false,
      "notes": "Static pages carry no service and no captured template vocabulary. One page per section; create additional About sections for multiple info pages."
    }
  ],
  "extensions": []
}
```

## Before you build

Your API photo feed requires a JSON endpoint exposing images in GoodBarber's Content API format — confirm this exists or plan to build it first. Create multiple Information sections if you need more than one info page (each About section holds one page).
