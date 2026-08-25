# App Structure — New York Tour Guide

A tour guide app serving tourists with news, photos, locations and information about New York. Four sections planned.

## Plan

```json
{
  "appId": null,
  "generatedAt": "2026-08-25",
  "summary": "A tour guide app for tourists visiting New York, featuring news updates, image galleries, location maps, and informational content.",
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
      "notes": "You will author the content inside GoodBarber. Enriched list template shows the date and other metadata alongside each headline."
    },
    {
      "order": 2,
      "name": "Photos",
      "intent": "Gallery of images of New York pulled from an external API",
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
      "templateVerified": false,
      "notes": "Uses your own API — requires a JSON endpoint matching GoodBarber's Content API spec, with an image field for each item. Photo detail template family was not captured. Pinterest template (the default) works well for galleries of mixed aspect ratios."
    },
    {
      "order": 3,
      "name": "Locations",
      "intent": "Map showing places of interest and tourist attractions in New York",
      "status": "matched",
      "type": "GBModuleTypeMaps",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Map",
      "template": {
        "list": "GBMapsListTemplateTypeEnriched",
        "content": "GBMapsContentTemplateTypeBanner",
        "detail": null
      },
      "templateVerified": true,
      "notes": "You will add locations inside GoodBarber. Enriched list shows addresses on each place card; Banner content template displays the location image prominently. A third Maps detail template family exists but its purpose is unclear and is not used here."
    },
    {
      "order": 4,
      "name": "Information",
      "intent": "Informational and reference content the guide can update",
      "status": "matched",
      "type": "GBModuleTypeAbout",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "About",
      "template": null,
      "templateVerified": false,
      "notes": "A single static page where you can upload text, images and any other reference material. No template vocabulary was captured for this type."
    }
  ],
  "extensions": []
}
```

## Before you build

The Photos section requires a JSON API endpoint. Confirm that your image source exposes items as JSON matching GoodBarber's Content API specification — field names, structure, and that each item carries an image field. If the API does not yet exist, someone will need to build it.
