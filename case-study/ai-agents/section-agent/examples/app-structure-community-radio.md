# App Structure — Community Radio Station

A listener app for a community radio station: live stream, on-demand archive, schedule, and two intake forms.
Five sections, no gaps.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-23",
  "summary": "Community radio app: live stream, past-show archive, weekly schedule, song requests and volunteer signup.",
  "sections": [
    {
      "order": 1,
      "name": "Listen Live",
      "intent": "Our live stream",
      "status": "matched",
      "type": "GBModuleTypeLive",
      "typeVerified": true,
      "service": "liveradio",
      "serviceVerified": true,
      "catalogEntry": "Live Audio",
      "createRoute": "/manage/app/content-add-liveradio/",
      "createRouteVerified": false,
      "template": null,
      "templateVerified": false,
      "notes": "Continuous stream, so Live rather than Sound. Needs the stream URL from your streaming host. No template vocabulary was captured for Live, so none is named."
    },
    {
      "order": 2,
      "name": "Listen Back",
      "intent": "Past shows people can listen back to",
      "status": "matched",
      "type": "GBModuleTypeSound",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Podcasts",
      "createRoute": "/manage/app/content-add-mcms/",
      "createRouteVerified": false,
      "template": {
        "list": "GBSoundListTemplateTypeClassic",
        "detail": "GBSoundContentTemplateTypeClassic"
      },
      "templateVerified": true,
      "notes": "Discrete episodes, so Sound is the archive companion to the Live section. Service assumes you upload episodes in GoodBarber; if the shows already sit on a podcast host, use `podcast` for a plain RSS feed or the host's own connector (soundcloud, anchor, spreaker, ausha, simplecast) instead — in which case the host owns the items and there is no 'Edit the content' action in the app. Templates left at the defaults."
    },
    {
      "order": 3,
      "name": "Schedule",
      "intent": "Our weekly schedule, which we already keep in Google Calendar",
      "status": "matched",
      "type": "GBModuleTypeAgenda",
      "typeVerified": true,
      "service": "vcalendar",
      "serviceVerified": true,
      "catalogEntry": "iCal/vCal",
      "createRoute": "/manage/app/content-add-vcalendar/",
      "createRouteVerified": false,
      "template": {
        "list": "GBEventListTemplateTypeCondensed",
        "detail": "GBEventContentTemplateTypeClassic"
      },
      "templateVerified": true,
      "notes": "Google Calendar publishes an iCal/ICS address, which is what `vcalendar` consumes — prerequisite is that someone retrieves that URL. Feed-backed: the schedule stays editable in Google Calendar and cannot be edited inside the app, which is the right way round for something you already maintain there. The feed URL is bound server-side in the section's settings, not in the section itself. Condensed is the only captured Event list template and is the default."
    },
    {
      "order": 4,
      "name": "Song Requests",
      "intent": "A way for listeners to send in song requests",
      "status": "matched",
      "type": "GBModuleTypeForm",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Form",
      "createRoute": "/manage/app/content-add-mcms/",
      "createRouteVerified": false,
      "template": null,
      "templateVerified": false,
      "notes": "Form rather than Submit: a request becomes a message to the station, not content published into a section. If you would rather requests appear publicly in the app after review, that is Submit instead."
    },
    {
      "order": 5,
      "name": "Volunteer With Us",
      "intent": "Our existing JotForm volunteer signup",
      "status": "matched",
      "type": "GBModuleTypeCustom",
      "typeVerified": true,
      "service": "jotform",
      "serviceVerified": true,
      "catalogEntry": "JotForm",
      "createRoute": "/manage/app/content-add-jotform/",
      "createRouteVerified": false,
      "template": null,
      "templateVerified": false,
      "notes": "The form already exists on the web, so this is a web view pointed at its URL — one field to fill, not a rebuild. Being a web view, it gets no native app capabilities, and submissions land in JotForm rather than in GoodBarber."
    }
  ],
  "extensions": []
}
```

## Before you build

Three URLs are prerequisites: the live stream address, the Google Calendar ICS link, and the JotForm form URL.
Confirm where the past shows currently live — uploaded to GoodBarber, or already on a podcast host — since that decides the Sound section's service.
