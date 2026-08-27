# App Structure — Campground

A campground information and event management app with weather forecasts, info feeds, event calendar, and camper inquiry forms. Four sections planned.

## Plan

```json
{
  "appId": null,
  "generatedAt": "2026-08-23",
  "summary": "Campground information and event management app with weather, news, calendar, and forms.",
  "sections": [
    {
      "order": 1,
      "name": "Weather",
      "intent": "Current weather forecast for Seattle, displayed to campers on arrival.",
      "status": "undetermined",
      "type": null,
      "typeVerified": false,
      "service": null,
      "serviceVerified": false,
      "catalogEntry": null,
      "template": null,
      "templateVerified": false,
      "notes": "Weather widgets are not in the captured section types. GoodBarber may support weather integration through an extension or Custom Code section, but this is not confirmed in the available tables. Confirm whether a weather connector or plugin exists before committing to a development path."
    },
    {
      "order": 2,
      "name": "Campground Info",
      "intent": "Alerts, rules, news and updates about the campground, managed by owner.",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Articles",
      "template": {
        "list": "GBArticleListTemplateTypeClassic",
        "detail": "GBArticleDetailTemplateTypeClassic"
      },
      "templateVerified": true,
      "notes": "Built-in CMS — the owner writes and publishes posts directly in GoodBarber. The Classic template is appropriate for a simple info feed; it can accommodate titles, summaries, and optional images."
    },
    {
      "order": 3,
      "name": "Events Calendar",
      "intent": "Upcoming campground events, activities and schedule, managed by owner.",
      "status": "matched",
      "type": "GBModuleTypeAgenda",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Events",
      "template": {
        "list": "GBEventListTemplateTypeCondensed",
        "detail": "GBEventContentTemplateTypeClassic"
      },
      "templateVerified": true,
      "notes": "Built-in CMS with date-based organization — owner creates and edits events in GoodBarber. Condensed list template keeps many events scannable; the Classic detail template is the default for event pages."
    },
    {
      "order": 4,
      "name": "Camper Inquiries",
      "intent": "Forms for gathering questions or feedback from campers.",
      "status": "matched",
      "type": "GBModuleTypeForm",
      "typeVerified": true,
      "service": null,
      "serviceVerified": true,
      "catalogEntry": "Form",
      "template": null,
      "templateVerified": false,
      "notes": "Form builder for structured input from campers. Responses are collected and available to the owner for review. This is for inquiries and feedback, not for user-authored content to be published."
    }
  ],
  "extensions": []
}
```

## Before you build

The weather forecast is the one section that requires confirmation. Check whether GoodBarber supports weather integrations (through an extension, a Custom Code plugin, or a third-party weather service connector). If no native or connector-based solution exists, the weather could be embedded as a `GBModuleTypeCustom` web view pointing to a weather service's embedded widget, or implemented via a `GBModuleTypePlugin` using Custom Code.
