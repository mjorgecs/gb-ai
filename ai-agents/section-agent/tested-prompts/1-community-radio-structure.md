# App Structure — Community Radio Station

*Generated 2026-08-13 by the App Structure Agent. This is a plan of actions, not a document to paste into an app.*

---
# User's Prompt

*I run a community radio station. The app needs our live stream, past shows people can listen back to, our weekly schedule which we already keep in Google Calendar, a way for listeners to send in song requests, and our existing JotForm volunteer signup.*

---

## Summary

A listener app for a community radio station: the live stream, an archive of past shows to listen back to, the weekly schedule already kept in Google Calendar, a song-request form, and the station's existing JotForm volunteer signup.

**Five sections. No gaps. Nothing paid — total added cost $0/month as of 2026-08-13.** Three of the five need a source connected after creation.

One thing to read before building: **the schedule section will not display recurring events**, and a weekly radio schedule in Google Calendar is almost certainly built from recurring events. See section 3 — it's the only part of this plan with real risk in it.

## Decomposition

Five intents, stated before anything was decided so you can correct the split:

| # | Intent | Screen or behaviour? |
|---|---|---|
| 1 | Listen to the station live | Screen |
| 2 | Listen back to past shows | Screen |
| 3 | See the weekly schedule | Screen |
| 4 | Send in a song request | Screen |
| 5 | Sign up as a volunteer (existing JotForm) | Screen |

All five are screens, so all five go to `sections[]` and nothing lands in `extensions[]`. Two splits worth confirming:

- **Live stream and past shows are two sections, not one.** The platform draws a hard line between a continuous stream and a list of discrete episodes; they are different types with different players.
- **Song requests and the volunteer signup are two sections**, even though both are "a form", because one is built in GoodBarber and the other already exists on the web. Different types entirely — see sections 4 and 5.

## Sections

### 1. Live — `GBModuleTypeLive` + `liveradio`

The station's live stream. `Live` rather than `Sound` because the distinguishing question is stream versus discrete episodes, and this is a continuous broadcast with no items to list.

- **Free.** The Live Audio extension is listed at *For Content apps | Free* (checked 2026-08-13).
- **Source binding:** your stream URL, pasted into the section's Settings after creation. This is a separate server-side step and not part of the section itself.
- Playback continues in the background while the listener uses other apps, and the section has a scheduling function that can restrict the stream to certain hours — useful if you only broadcast part of the day.
- **Optional, not included in this plan:** *Live +* at **$10/month** (checked 2026-08-13) adds now-playing metadata (track, artist, artwork) on M3U streams, a history of the last 5 songs, social sharing of the current track, a sleep timer and a fully customisable player. Named here because a community station usually wants the now-playing display eventually and the free section does not have it — but you asked to keep it minimal, so it stays out of the plan and out of the cost.

### 2. Past shows — `GBModuleTypeSound` + `podcast`

The listen-back archive. `Sound` is the audio-feed type; `podcast` is the service for any podcast RSS feed, which every podcast host emits.

- **Free** (checked 2026-08-13 — the whole podcast connector family is free).
- **Source binding:** your podcast host's RSS feed URL, bound in Settings after creation.
- **Which host is it?** You said the shows live on a podcast host but didn't name it. If it's **Spotify for Podcasters (Anchor), Spreaker, Ausha or Simplecast**, use that host's dedicated connector instead of the generic feed — the dedicated connectors are the better route where one exists. Any other host, the generic `podcast` feed is correct and works. Tell me the host and I'll pin the service exactly.
- **You will not be able to edit episodes inside the app.** A connector-backed section has no "Edit the content" action — the host owns the episodes, and the app only reads them. You publish on the host, and the app follows. If you'd rather upload episodes directly into GoodBarber, that's the `mcms` service instead, and it's the only option that lets you author in-app.
- Before committing, check the **date of the newest episode in the feed**, not that the URL loads. A host that stopped updating still returns a perfectly valid feed full of old shows, and the section will look built while reading as abandoned.
- If listeners should browse by show rather than scrolling one long list, plan **categories before you connect the feed** — they're scoped to the section, and retro-fitting them means re-filing every episode.

### 3. Schedule — `GBModuleTypeAgenda` + `vcalendar`

The weekly schedule, synced from the Google Calendar you already keep. `Agenda` is the dated-events type and `vcalendar` takes an iCal/vCal feed, which is exactly what Google Calendar publishes.

- **Free** (checked 2026-08-13).
- **Source binding:** your calendar's iCal address, pasted into Settings. In Google Calendar this is under the calendar's *Settings and sharing* → *Integrate calendar* → the public or secret address in iCal format (`.ics`). The public address requires the calendar to be public; the secret address works on a private calendar but should be treated as a password.
- Creating a calendar section also generates an Event widget on the app's home page.

> **⚠️ Read this before building the schedule section.**
>
> GoodBarber's documentation states plainly: *"GoodBarber apps don't display past or recurrent events, this applies to all sources."* (checked 2026-08-13, stated on two separate help pages.)
>
> A weekly radio schedule is the textbook case of recurring events — "Jazz Hour, every Tuesday 8pm" is one recurring entry in Google Calendar, not 52 separate ones. **If your calendar is built that way, this section will come up empty**, and it will do so silently: the feed connects, the section builds, and no shows appear.
>
> Three ways out, cheapest first:
>
> 1. **Check first.** Open the iCal feed and look for `RRULE:` lines. If there are none — every show is entered as its own dated event — `vcalendar` works as-is and you can ignore the rest of this box.
> 2. **Expand the recurrences at the source.** Generate a feed from the Google Calendar API with `singleEvents=true`, which flattens each recurring show into individual dated occurrences, and reshape the output as JSON matching GoodBarber's Content API spec. That's `GBModuleTypeAgenda` + **`custom`** instead of `vcalendar` — same type, same section, different service, still free. It needs a small endpoint built and kept running, so it's real work, but it's the option that keeps Google Calendar as the single source of truth.
> 3. **Give up the sync.** `GBModuleTypeAgenda` + `mcms` means entering each week's shows by hand in GoodBarber. Free and immediate, but it's double entry forever, and for a volunteer-run station that usually means the app schedule drifts out of date within a month.
>
> A fourth option worth naming because stations often want it: if the weekly grid is genuinely fixed — same shows, same slots, every week — then it isn't a calendar at all, it's a **static page** (`GBModuleTypeAbout` + `mcms`), edited when the grid changes and never otherwise. That sidesteps the recurrence problem entirely at the cost of losing per-date accuracy for one-off specials.
>
> Past events are also hidden, which is the correct behaviour here — the schedule shows what's coming, not what already aired.

### 4. Song requests — `GBModuleTypeForm` + `mcms`

A form listeners fill in to request a track. `Form` rather than `Submit` because you said requests should reach the station privately: `Form` collects structured answers for the owner, while `Submit` is a contribution pipeline where the user's input gets reviewed and published as app content. Your answers become messages, not content.

- **Free** (checked 2026-08-13).
- Built in GoodBarber's form builder — no external service, no source binding.
- Suggested fields: song title, artist, an optional dedication or message, the requester's name, and optionally which show it's for. Keep it short; every extra field costs you requests.
- Worth deciding up front: **who receives these, and how**. A volunteer-run station that routes requests to one person's inbox tends to lose them when that person is away.

*If you later want requests to appear publicly in the app — a "most requested this week" list, or dedications shown to everyone — that's a different type (`GBModuleTypeSubmit`), and it's a change of section rather than a setting.*

### 5. Volunteer signup — `GBModuleTypeCustom` + `jotform`

Your existing JotForm, embedded in the app. This is `Custom` — a web view pointed at a URL — with JotForm as a preset. It is **not** custom code and needs nothing built.

- **Free** (checked 2026-08-13).
- **Source binding:** the URL of your existing JotForm. Nothing gets rebuilt; submissions keep landing in your JotForm account exactly as they do now.
- **What a web view means in practice:** the form renders as a web page inside the app rather than as a native screen, so it will look like your JotForm rather than like the rest of the app, and it needs a connection to load. It also doesn't get the app's native capabilities — no on-device storage, no access to the app's login state.
- *Deliberately not rebuilt as a `Form` section.* You already have this form and its responses live in JotForm; embedding it is a URL field, whereas rebuilding it would split volunteer submissions across two systems. If you'd rather have one native-looking form and are willing to move where responses land, `Form` + `mcms` is the alternative.

## Extensions

**None required.** All five intents are screens, and every connector they need is free.

Two things already in the app that you don't create and shouldn't plan for: **Favorites**, **Settings** and the two legal pages (**terms** and **privacy**) are auto-added — they exist in the "Other sections" area outside navigation, and if you want any of them in the menu, that's placement and configuration, not creation.

Named but not planned: **Live +** ($10/month, checked 2026-08-13) — see section 1. **Push notifications** are free and are a behaviour rather than a section, so if you later want to alert listeners when you go live, it adds nothing to this structure.

## Gaps

**None.** Every intent matched an existing type and service. Recorded here because the checks that could have produced false gaps were run explicitly:

- The schedule's recurrence problem is **not** a gap — `custom` on the `Agenda` type covers it, which is Step 4 of the ladder and the step most likely to be skipped.
- The volunteer form is **not** a gap and **not** custom code — it already exists on the web, which is precisely what `GBModuleTypeCustom` is for.
- Song requests are **not** a gap — `Form` is a native type, and the request is a straightforward collection of structured input.

## Validation

Checked against the routing checklist:

- All five `type` values are verbatim strings from the captured enum. Nothing invented.
- Every `service` key present; none null in this plan, since all five types take a service.
- Three externally-fetching sections (`liveradio`, `podcast`, `vcalendar`) each carry a `sourceBinding` marked as a separate provisioning step.
- Every `pricing` object carries `asOf: 2026-08-13`, free ones included, and every figure was read from the extension's own detail page rather than a search badge or from memory.
- Both connector-backed sections state in prose that content cannot be authored in-app.
- No `Fakeclickto` section in this plan, so no link disclosure applies.
- `Home` not proposed; `Bookmark`, `Settings` and `Tos` referenced as existing, never created.
- Section count reported (5), not capped. Apps do carry a per-app instance cap the back office reports at runtime; five is nowhere near any plausible limit, and no number is asserted here.

**Warnings carried forward:**

1. **`vcalendar` and recurring events** — the highest-risk item in this plan. Verify the iCal feed's contents before building, per section 3.
2. **Podcast host not named** — `podcast` (generic feed) is correct for any host, but if it's Spotify for Podcasters, Spreaker, Ausha or Simplecast, the dedicated connector is the better route. `serviceVerified` stays `true` either way; both are in the known-good list.
3. **`createRoute` values are inferred.** They follow the `/manage/app/content-add-<service>/` pattern but were not observed for these four services, so all four carry `createRouteVerified: false`. The Song requests section uses `mcms`, which serves eight different tiles — one URL cannot provision eight types — so it correctly gets `createRoute: null`.
4. **`typeVerified: true` throughout.** No `Commerce*` types in this plan, which is where inference normally lives.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-13",
  "summary": "Listener app for a community radio station: live stream, show archive, weekly schedule, song requests and an existing volunteer form.",
  "sections": [
    {
      "order": 1,
      "name": "Live",
      "intent": "Listen to the station's live broadcast",
      "status": "matched",
      "type": "GBModuleTypeLive",
      "typeVerified": true,
      "service": "liveradio",
      "serviceVerified": true,
      "catalogEntry": "Live Audio",
      "createRoute": "/manage/app/content-add-liveradio/",
      "createRouteVerified": false,
      "sourceBinding": {
        "required": true,
        "kind": "streamUrl",
        "suggested": null,
        "note": "Station's live audio stream URL, bound server-side in section Settings. M3U streams carry the metadata Live+ would display."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Live rather than Sound — a continuous stream, not discrete episodes. Background playback; built-in scheduling can restrict the stream to broadcast hours. Live+ ($10/mo) adds now-playing metadata and is deliberately not in this plan."
    },
    {
      "order": 2,
      "name": "Past shows",
      "intent": "Listen back to previously broadcast shows",
      "status": "matched",
      "type": "GBModuleTypeSound",
      "typeVerified": true,
      "service": "podcast",
      "serviceVerified": true,
      "catalogEntry": "Podcast feeds",
      "createRoute": "/manage/app/content-add-podcast/",
      "createRouteVerified": false,
      "sourceBinding": {
        "required": true,
        "kind": "feedUrl",
        "suggested": null,
        "note": "Podcast host's RSS feed URL. Check the newest episode's date, not just that the URL resolves."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Feed-backed — no in-app episode editing; the host owns the items. If the host is Spotify for Podcasters, Spreaker, Ausha or Simplecast, switch to anchor/spreaker/ausha/simplecast respectively. mcms if episodes should be uploaded into GoodBarber instead. Plan categories before connecting if listeners should browse by show."
    },
    {
      "order": 3,
      "name": "Schedule",
      "intent": "See the weekly programme schedule, kept in Google Calendar",
      "status": "matched",
      "type": "GBModuleTypeAgenda",
      "typeVerified": true,
      "service": "vcalendar",
      "serviceVerified": true,
      "catalogEntry": "iCal/vCal",
      "createRoute": "/manage/app/content-add-vcalendar/",
      "createRouteVerified": false,
      "sourceBinding": {
        "required": true,
        "kind": "icalUrl",
        "suggested": "https://calendar.google.com/calendar/ical/<calendar-id>/public/basic.ics",
        "note": "Google Calendar's iCal address (Settings and sharing → Integrate calendar). Secret address works on a private calendar; treat it as a credential."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "BLOCKING RISK: GoodBarber apps do not display recurrent events, from any source (goodbarber.com help, checked 2026-08-13). A weekly schedule built from recurring calendar entries will render empty. Inspect the feed for RRULE lines first. Fallback: same type with service 'custom', fed by a Google Calendar API export using singleEvents=true reshaped to GoodBarber's Content API spec — still free, but an endpoint must be built and maintained. Second fallback: mcms, hand-entered, no sync. Past events are also hidden, which is desired here."
    },
    {
      "order": 4,
      "name": "Song requests",
      "intent": "Listeners send song requests privately to the station",
      "status": "matched",
      "type": "GBModuleTypeForm",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Form",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Form rather than Submit — answers reach the station as messages, they do not become published app content. Suggested fields: song, artist, dedication, requester name, optional show. createRoute null because mcms serves eight tiles and no single provisioning URL exists. Decide who receives submissions before launch."
    },
    {
      "order": 5,
      "name": "Volunteer with us",
      "intent": "Embed the station's existing JotForm volunteer signup",
      "status": "matched",
      "type": "GBModuleTypeCustom",
      "typeVerified": true,
      "service": "jotform",
      "serviceVerified": true,
      "catalogEntry": "JotForm",
      "createRoute": "/manage/app/content-add-jotform/",
      "createRouteVerified": false,
      "sourceBinding": {
        "required": true,
        "kind": "formUrl",
        "suggested": null,
        "note": "URL of the existing JotForm. Responses continue to land in the JotForm account; nothing is rebuilt."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Custom, not Plugin — the form already exists on the web, so this is a web view with a preset URL, not code. Renders as a web page rather than a native screen, requires a connection, and gets no native capabilities. Alternative if a native look matters more than keeping responses in JotForm: Form + mcms, rebuilt."
    }
  ],
  "extensions": [],
  "validation": {
    "sectionCount": 5,
    "warnings": [
      "Schedule: recurrent events are not displayed by any GoodBarber calendar source. Verify the Google Calendar iCal feed for RRULE entries before building; fall back to Agenda + custom (singleEvents=true export) if the schedule recurs.",
      "Past shows: podcast host not named. Generic 'podcast' feed service is correct for any host, but a dedicated connector (anchor, spreaker, ausha, simplecast) is preferred if it applies.",
      "All createRoute values follow the documented pattern but were not observed; createRouteVerified is false throughout. Song requests correctly carries null (mcms serves eight tiles).",
      "Live+ ($10/mo, asOf 2026-08-13) named but excluded at the user's request to keep the plan minimal."
    ]
  }
}
```

## Sources

- section-docs/0-section-type-codenames.md` — type enum, catalog mapping and service tables, back-office capture 2026-08-12.
- [GoodBarber Extensions](https://www.goodbarber.com/extensions/) — connector inventory and pricing lines, accessed 2026-08-13.
- [Live Audio extension](https://www.goodbarber.com/extensions/live-audio/) — "For Content apps | Free", background playback, broadcast scheduling, accessed 2026-08-13.
- [Live + extension](https://www.goodbarber.com/extensions/live/) — "For Content apps | $10/month", metadata, history, sharing, sleep mode, accessed 2026-08-13.
- [Content extensions category](https://www.goodbarber.com/extensions/categories/content/) — iCal/vCal, CMS Agenda and Custom events feed all listed free, accessed 2026-08-13.
- [Events: iCal/vCal, WM Events, etc.](https://www.goodbarber.com/help/calendar-r41/events-ical-vcal-wm-events-etc-a21/) — feed URL configuration and the past/recurrent events limitation, accessed 2026-08-13.
- [iCal/vCal calendar section](https://www.goodbarber.com/help/shop/calendar-sections-r144/ical-vcal-calendar-section-a21/) — same limitation stated independently, plus the auto-generated Event home widget, accessed 2026-08-13.
