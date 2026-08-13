# App Structure — Campground

*Generated 2026-08-13 by the App Structure Agent. This is a plan of actions, not a document to paste into an app.*

---
# User's Prompt

*I manage a campground. The app needs a page with the weather forecast for Seattle (U.S.), a page where I can post information about the campground (alerts, rules, news, etc.), a calendar for scheduling events, and forms for asking campers questions.*

---

## Summary

A camper-facing app for a campground: the Seattle forecast, a noticeboard the manager posts to, an events calendar, and a form for asking campers questions.

**Four sections, one extension. No gaps. Nothing paid — total added cost $0/month as of 2026-08-13.** Only one section needs an external source connected after creation.

Two things to read before building:

1. **The weather page is the only section here that isn't a native GoodBarber feature.** There is a first-party Weather extension, but it is a LAB item and the store page says plainly *"This feature is not yet available in GoodBarber"* (checked 2026-08-13). The plan routes around it with an embedded web view, which needs no code — see section 3, which also names the two other routes and why they weren't chosen.
2. **The events calendar will not display recurring events.** A campground calendar is usually full of them — bingo every Friday, quiet hours every night. See section 2; it is the highest-risk item in this plan and it fails silently.

## Decomposition

Four intents, stated before anything was decided so you can correct the split:

| # | Intent | Screen or behaviour? |
|---|---|---|
| 1 | Read the weather forecast for Seattle | Screen |
| 2 | Read campground information the manager posts — alerts, rules, news | Screen |
| 3 | See what events are scheduled | Screen |
| 4 | Answer questions the manager asks | Screen |

All four are screens, so all four go to `sections[]`. Three splits worth confirming, because each one could reasonably have gone the other way:

- **"Alerts, rules, news, etc." is one section, not three.** They share a shape — dated written posts, written by you, read by campers — so they are one `Article` section with three *categories*, not three sections. The exception is worth naming: if your **rules never change**, they aren't news, they're a static page, and that's a separate `About` section. See section 1.
- **Alerts are also a behaviour, not only a screen.** Posting a burn-ban notice to a section only reaches campers who open the app. Push notifications are free and add nothing to the structure — see Extensions.
- **"Forms" is plural in your description; this plan starts with one.** GoodBarber's form builder is one form per section, so three different questionnaires are three sections. One is planned here — say the word and I'll expand it. See section 4.

## Sections

### 1. Campground info — `GBModuleTypeArticle` + `mcms`

The noticeboard: alerts, rules, news, anything you want campers to read. `Article` is the type for a feed of written items with titles, and `mcms` is GoodBarber's own CMS.

- **Free** (checked 2026-08-13 — CMS Articles is listed *Free* in the Content category).
- **No source to connect.** You write the posts in the back office; nothing external is involved.
- **`mcms` is the only service that lets you write posts inside GoodBarber.** Every other service for this type — WordPress, RSS, Substack and the rest — is a connector, and a connector-backed section has no "Edit the content" action because the external service owns the items. You said you want to post information yourself, so `mcms` is the answer, and this is the one decision in the plan with no trade-off in it.
- **Plan the categories before you enter any content.** Categories are a one-level taxonomy scoped to this section, and retro-fitting them means re-filing every post. Suggested: **Alerts · Rules · News**, exactly the split in your description. Add *Facilities* if you expect posts about the laundry, the dump station and the wifi.
- Comments are an optional block on this type, toggled independently. A campground noticeboard with comments open is a moderation job — worth deciding deliberately rather than discovering.

*If your rules are genuinely static — the same text year after year — consider putting them in a separate `GBModuleTypeAbout` section instead of a category here. `About` is one non-repeating page and is free. It reads better than a rules post sinking down a dated feed, and campers can find it in the menu. This is a judgement call about your rules, not a platform constraint, so it stays out of the plan and out of the JSON.*

### 2. What's on — `GBModuleTypeAgenda` + `mcms`

The events calendar. `Agenda` is the dated-events type; `mcms` because you said you want to *schedule* events, which means authoring them, not syncing a calendar you already keep.

- **Free** (checked 2026-08-13 — CMS Agenda is listed *Free*).
- **No source to connect.** Each event is entered in the back office.
- Creating a calendar section also generates an Event widget on the app's home page.
- **If you already keep the schedule in Google Calendar, say so** — `vcalendar` takes an iCal feed and the calendar becomes the single source of truth instead of double entry. Same type, same section, different service, still free. It does not escape the warning below.

> **⚠️ Read this before building the calendar.**
>
> GoodBarber's documentation states: *"Warning: we don't display past or recurrent events, this applies to all sources."* (checked 2026-08-13.) **All sources** means `mcms` too — this is not a connector limitation you can dodge by typing events in by hand.
>
> A campground calendar is close to a worst case for this. "Campfire every Saturday at 8", "pancake breakfast every Sunday", "quiet hours nightly" are recurring by nature, and the platform has no repeat function that will show them. If you create one entry and expect it to appear every week, **the section will render empty and give you no error**.
>
> Two ways to live with it:
>
> 1. **Enter each occurrence as its own dated event.** Twelve Saturday campfires means twelve entries. Tedious, free, and works today. For a seasonal campground with a defined open season this is usually tolerable — you do it once at the start of the season.
> 2. **Generate the occurrences outside GoodBarber.** Keep the schedule in Google Calendar with its repeat rules, export it through the Google Calendar API with `singleEvents=true` — which flattens each recurring event into individual dated occurrences — and reshape that output as JSON matching GoodBarber's Content API spec. That's `GBModuleTypeAgenda` + **`custom`**, still free as a section, but it means a small endpoint someone builds and keeps running.
>
> A third option if your weekly rhythm is genuinely fixed: the repeating part isn't a calendar at all, it's a **static page** ("What happens each week at the campground"), and the `Agenda` section carries only the one-off events — the live band, the holiday weekend cookout. That's the cheapest honest answer for most campgrounds, and it costs nothing to combine with option 1.
>
> Past events being hidden is correct behaviour here — campers want what's coming, not what they missed.

### 3. Seattle weather — `GBModuleTypeCustom`, no service

A page showing the Seattle forecast, as a web view pointed at a hosted forecast page or weather widget. `Custom` is the web-view type: you give it a URL and it renders that page inside the app.

- **Free** (checked 2026-08-13 — the URL/web-view section carries no charge).
- **Source binding:** the URL below, pasted into Settings after creation. Separate server-side step, not part of the section.

**The URL to use:**

```
https://forecast.weather.gov/MapClick.php?lat=47.6062&lon=-122.3321
```

That is the US National Weather Service forecast for downtown Seattle. Verified loading on 2026-08-13: current conditions from Boeing Field plus an 8-day outlook, responsive viewport, no login and no cookie wall.

It is the recommended choice for one reason that outranks how it looks — **it is a US federal government work, so there is no licence to read, no attribution to display, and no commercial-use clause to fall foul of.** Every other free weather source on the web has at least one of those, and a campground is a commercial business. NWS also has no rate limit that a page view can trip, and it will not disappear or start charging.

**Point it at your actual campground, not downtown Seattle.** Change the two numbers to your site's coordinates and the forecast becomes local — NWS resolves any US lat/lon to its nearest forecast grid point:

```
https://forecast.weather.gov/MapClick.php?lat=<your latitude>&lon=<your longitude>
```

Right-click your campground in Google Maps and the first item in the menu is the coordinate pair, in the order this URL wants them. Keep four decimal places; more is ignored. If campers travel in from the city, a second `Custom` section pointed at the downtown Seattle URL costs nothing — two web views, two URLs.

*The trade-off, stated plainly:* it is a government page, so campers get NWS site navigation and NWS styling above the forecast. It reads as functional rather than designed.

**The prettier option, with a real catch.** meteoblue publishes a standalone widget URL that needs no hosting and no code — verified on 2026-08-13 rendering a 7-day Seattle forecast in Fahrenheit and mph, current conditions on top, hourly rows beneath:

```
https://www.meteoblue.com/en/weather/widget/three/seattle_united-states-of-america_5809844?geoloc=fixed&nocurrent=0&noforecast=0&days=7&tempunit=FAHRENHEIT&windunit=MILE_PER_HOUR&layout=image
```

Drop `tempunit` and `windunit` and it defaults to Celsius, which is not what your campers want. It looks considerably better than the NWS page in a phone-width frame.

**But read the licence before you ship it.** meteoblue's free widget is for non-commercial use, and their own definition draws the line at fewer than 100 daily visitors or 50 daily data requests — a hotel or company site covering a handful of locations sits inside that. A campground app in peak season plausibly does not. Commercial users are told to order business services rather than use the free widget, and non-commercial use requires a direct link back to meteoblue from the page. If you use it, count your daily opens honestly, keep the link back, and treat exceeding the threshold as a bill rather than a technicality.

Given a choice between a plainer page with no legal exposure and a nicer one with a threshold to monitor, the plan takes the plain one.

**Why this rather than the other three routes.** Weather is the one intent here with no native section type, so it went through the full lookup before landing:

| Route | Verdict |
|---|---|
| A native section type | **None exists.** There is no weather type in the platform's vocabulary, and I won't invent a constant that looks like one. |
| **The first-party Weather extension** | **Exists, but you can't have it.** [goodbarber.com/extensions/weather/](https://www.goodbarber.com/extensions/weather/) describes exactly what you asked for — "Display weather data for the city of your choice", in a section or on the Home page — and then says: *"This feature is not yet available in GoodBarber."* It's a LAB item with a register-your-interest form. Register on that page; if it ships, it is strictly better than everything below, and swapping to it later is a section change, not a rebuild. |
| **An embedded web view** ← chosen | Works today, needs no code, costs nothing. Caveats below. |
| A Custom Code section | Possible and better-looking, but it's a development project with a maintenance liability and a data-licensing problem. See the sub-section after next. |

**What a web view means in practice.** The page renders as a web page inside the app: it will look like the weather provider, not like the rest of your app, it needs a connection to load, and it gets none of the app's native capabilities. For a forecast page that is mostly acceptable — nobody expects the weather to work offline — but campers will notice the visual seam.

**Two things to check before you pick a provider**, neither of which is obvious:

- **Does the licence cover a mobile app?** Most free weather-widget licences are written for *websites*. A widget embedded in an app webview is a grey area with several providers, and a campground is a commercial business, which rules out any "free for non-commercial use" tier. Read the terms for the specific case rather than the marketing page.
- **Does the page work in a narrow frame with no navigation?** Pick a provider whose embed is designed to be framed. A full desktop weather site inside a phone-width webview is a bad screen.

Seattle is at roughly `47.6062, -122.3321`; most providers key the widget on a city name or coordinates, so it is a one-time configuration and the section then needs no maintenance at all.

**If the seam bothers you: the Custom Code route, and its real costs.** A `GBModuleTypePlugin` Custom Code section — one self-contained `index.html` calling a weather API and rendering the forecast in your app's own palette — would look native, and GoodBarber publishes [a worked weather-by-geolocation plugin example](https://www.goodbarber.com/help/examples-and-tutorials-r110/plugin-example-weather-by-geolocation-a279/) to start from. It is deliberately **not** the recommendation, for three reasons that are worth having in writing:

1. **GoodBarber does not debug code it did not write.** A Custom Code section is entirely your maintenance burden, forever, including when the weather API changes.
2. **The obvious free API doesn't work from a Custom Code section.** The US National Weather Service API (`api.weather.gov`) needs no key and is public domain, which makes it the natural choice — but it **sends no `Access-Control-Allow-Origin` header**, so a browser cannot call it, and the recommended `User-Agent` header triggers a preflight the API rejects. Client-side use needs a server-side proxy, which is a second thing to build and host. This is exactly the check that gets skipped, and it would have been found at implementation time rather than planning time.
3. **The alternatives have a licensing catch.** Open-Meteo needs no key and is CORS-friendly, but its free tier is *"for non-commercial use"* — a campground is not that. OpenWeatherMap has a commercial-usable free tier, but the key ships inside the section and is readable by any user; that's acceptable only because such keys are free, read-only and rate-limited, and it must be understood as public rather than secret.

None of that makes custom code wrong. It makes it a project with a budget, and you should choose it deliberately or not at all. If you want it, ask and I'll write the full specification.

### 4. Ask the campers — `GBModuleTypeForm` + `mcms`

A form campers fill in to answer your questions. `Form` rather than `Submit` because of what happens to the answer: `Form` collects structured responses that come back to you as messages, while `Submit` is a contribution pipeline where a camper's input gets reviewed and published as content in the app. You're asking questions, not collecting posts.

- **Free** (checked 2026-08-13 — Form is listed *Free*).
- Built in GoodBarber's own form builder. No external service, no source binding, nothing to connect.
- **One form per section.** If you want a check-in questionnaire, a maintenance request and an end-of-stay feedback form, that's three `Form` sections, all free. Starting with one and splitting later is cheap; cramming three unrelated questionnaires into one form is how response rates die.
- Decide **who receives submissions** before launch, and make it a shared inbox rather than one person's. Seasonal staffing and a single recipient is a reliable way to lose a month of answers.

*If you'd rather campers post things other campers can see — trail conditions, photos, a lost-and-found — that's `GBModuleTypeSubmit`, a different type and a change of section rather than a setting. Named here because "forms for campers" often turns out to mean this halfway through.*

## Extensions

**One, and it's free.**

**Push Notifications** — *Free* (checked 2026-08-13). This is a behaviour, not a screen: it creates no section and changes nothing about the structure above. It is in the plan because **your alerts requirement is only half-served by section 1**. A gate-closure or burn-ban notice posted to the info section reaches campers who happen to open the app; a push reaches the ones who don't. Post it and push it. Automatic Push is also free and can fire whenever you publish a new article, which is worth configuring once and then forgetting.

Two adjacent free things, named so you don't plan around them: **Geofencing** and **iBeacons** are both free, and a campground is one of the few businesses where geofencing is genuinely useful — a welcome message when a camper arrives on site. Out of scope for what you asked, mentioned once.

Already in your app and not to be created: **Favorites**, **Settings** and the two legal pages (**terms** and **privacy**) are auto-added. They sit in the "Other sections" area outside navigation; putting any of them in the menu is placement, not creation.

## Gaps

**None** — but the weather page came within one step of the gap path, and the reason it stopped is the substance of this plan.

The gap path opens only when four checks all fail. For weather:

- [x] **No type fits.** Correct — there is no weather type. This alone is *not* a gap.
- [x] **No `custom` feed fits.** Correct, and worth stating: a forecast is nearly a feed of uniform items, so `Agenda` or `Article` + `custom` could technically render "Thursday, 22°, sunny" as list items. It would look like a blog post about the weather rather than a forecast, and it still needs the endpoint from the sub-section below. Rejected on quality, not on possibility.
- [ ] **No `GBModuleTypeCustom` fits.** ← **fails here.** A forecast page for Seattle plainly already exists on the web, and embedding an existing web page is precisely what the web-view type is for.
- [ ] **No extension exists.** ← also fails, in a qualified way: the Weather extension exists but is not yet released.

Two checks failing is two more than a gap allows. Writing a custom-code specification here would have turned a URL field into a development project — so the specification is offered as an option in section 3 rather than presented as a necessity.

The other three intents matched native types with no ambiguity worth recording.

## Validation

Checked against the routing checklist:

- All four `type` values are verbatim strings from the captured enum. Nothing invented — in particular, no weather codename was coined.
- Every `service` key present. Three are `mcms`; the weather section carries an explicit `null`, which is a decision, not an omission — the web-view type takes no service when it points at a plain URL.
- One externally-fetching section (the weather web view) carries a `sourceBinding` marked as a separate provisioning step. The other three are `mcms` and have no external source to bind.
- Every `pricing` object carries `asOf: 2026-08-13`, free ones included, and every figure was read from the extension's own page rather than from memory.
- The `mcms` disclosure is stated in reverse where it matters: section 1 says explicitly that `mcms` is what *permits* in-app authoring and that every connector would forbid it.
- No `Fakeclickto` section in this plan, so no link disclosure applies. The web view carries its own disclosure instead — it is not a native screen.
- `Custom` was checked before `Plugin`, and it won. The maintenance liability is stated in prose anyway, because the Plugin option is named.
- `Home` not proposed; `Bookmark`, `Settings` and `Tos` referenced as existing, never created.
- Behaviour with no screen (push) is in `extensions[]` with `createsSection: false`, not in `sections[]`.
- Section count reported (4), not capped. Apps carry a per-app instance cap the back office reports at runtime; four is nowhere near any plausible limit, and no number is asserted here.

**Warnings carried forward:**

1. **Recurring events are not displayed, from any source** — the highest-risk item in this plan, and the one most likely to be discovered after launch. Section 2.
2. **The Weather extension is a LAB item and unavailable.** The plan does not depend on it. Register interest; re-check before building, since a release between now and then would change the recommendation.
3. **Weather provider chosen and its terms checked.** The plan uses the NWS forecast URL, verified loading 2026-08-13, precisely because a US government work carries no licence, attribution or commercial-use clause to breach. The prettier meteoblue alternative is named in section 3 with its non-commercial threshold and link-back requirement stated, so choosing it is a decision rather than an accident. Neither provider's terms address a mobile-app webview explicitly; for NWS this is moot, for meteoblue it is one more reason the plan doesn't default to it.
4. **All four `createRoute` values are `null`.** Three sections use `mcms`, which serves eight different catalog tiles — one URL cannot provision eight types, so no route can be derived. The weather section takes no service, so the `/manage/app/content-add-<service>/` pattern has nothing to key on. Emitting a route that can't be derived is worse than emitting none; all four carry `createRouteVerified: false`.
5. **`typeVerified: true` throughout.** No `Commerce*` types in this plan, which is where inference normally lives.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-13",
  "summary": "Camper-facing app for a campground: Seattle forecast, a manager-authored noticeboard, an events calendar and a question form.",
  "sections": [
    {
      "order": 1,
      "name": "Campground info",
      "intent": "Manager posts alerts, rules and news for campers to read",
      "status": "matched",
      "type": "GBModuleTypeArticle",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Articles",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "mcms is the only service on this type that permits authoring inside GoodBarber; every connector is read-only because the external service owns the items. Plan categories before entering content — suggested Alerts / Rules / News, optionally Facilities — since they are scoped to the section and retro-fitting means re-filing every post. Comments are an optional block and imply moderation. createRoute null because mcms serves eight tiles and no single provisioning URL exists. If the rules are static, consider a separate GBModuleTypeAbout page instead of a category."
    },
    {
      "order": 2,
      "name": "What's on",
      "intent": "Campers see the schedule of campground events",
      "status": "matched",
      "type": "GBModuleTypeAgenda",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Events",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "BLOCKING RISK: GoodBarber does not display past or recurrent events, and the documentation states this applies to all sources — mcms included (goodbarber.com help, checked 2026-08-13). Weekly campground events must be entered as individual dated occurrences or they will not appear, and the section fails silently. Alternative if the schedule is already in Google Calendar: same type with service 'vcalendar' (free), which does not escape the recurrence limit. Alternative that does: same type with service 'custom', fed by a Google Calendar API export using singleEvents=true reshaped to the Content API spec — free as a section, but an endpoint must be built and maintained. Creating this section also generates an Event widget on Home."
    },
    {
      "order": 3,
      "name": "Seattle weather",
      "intent": "Campers read the weather forecast for Seattle",
      "status": "matched",
      "type": "GBModuleTypeCustom",
      "typeVerified": true,
      "service": null,
      "serviceVerified": true,
      "catalogEntry": "URL",
      "createRoute": null,
      "createRouteVerified": false,
      "sourceBinding": {
        "required": true,
        "kind": "pageUrl",
        "suggested": "https://forecast.weather.gov/MapClick.php?lat=47.6062&lon=-122.3321",
        "note": "US National Weather Service forecast for downtown Seattle, bound server-side in section Settings. Verified loading 2026-08-13: current conditions plus 8-day outlook, responsive viewport, no login or cookie wall. Chosen because it is a US federal government work — no licence, no attribution requirement and no commercial-use clause, which no other free source offers. Swap lat/lon for the campground's own coordinates to make the forecast local; four decimal places max. Alternative with better presentation: meteoblue's standalone widget URL (https://www.meteoblue.com/en/weather/widget/three/seattle_united-states-of-america_5809844?geoloc=fixed&nocurrent=0&noforecast=0&days=7&tempunit=FAHRENHEIT&windunit=MILE_PER_HOUR&layout=image), verified rendering 7 days in Fahrenheit and mph — but its free tier is non-commercial, bounded at roughly 100 daily visitors or 50 daily requests, and requires a link back to meteoblue."
      },
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "No weather type exists in the enum and none was invented. GoodBarber's first-party Weather extension matches this intent exactly but its store page reads 'This feature is not yet available in GoodBarber' — a LAB item, checked 2026-08-13; register interest and re-check before building, as it would supersede this section. Custom, not Plugin: the page already exists on the web, so this is a web view with a URL field rather than code. Renders as a web page rather than a native screen, needs a connection, gets no native capabilities. Custom Code alternative rejected as default, not as impossible: api.weather.gov sends no Access-Control-Allow-Origin header and cannot be called client-side without a proxy; Open-Meteo's free tier is non-commercial and a campground is not; OpenWeatherMap's key would ship publicly in the section, acceptable only because it is free, read-only and rate-limited. GoodBarber does not debug code it did not write."
    },
    {
      "order": 4,
      "name": "Ask the campers",
      "intent": "Manager asks campers questions and receives their answers",
      "status": "matched",
      "type": "GBModuleTypeForm",
      "typeVerified": true,
      "service": "mcms",
      "serviceVerified": true,
      "catalogEntry": "Form",
      "createRoute": null,
      "createRouteVerified": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Form rather than Submit — answers return to the manager as messages and do not become published app content. One form per section: additional questionnaires are additional Form sections, each free. createRoute null because mcms serves eight tiles. Decide the recipient before launch and prefer a shared inbox to an individual's. If campers should post content other campers can see, that is GBModuleTypeSubmit and a different section."
    }
  ],
  "extensions": [
    {
      "name": "Push Notifications",
      "createsSection": false,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "note": "A behaviour, not a screen. Included because alerts posted to section 1 only reach campers who open the app. Automatic Push (also free) can fire on each new article published."
    }
  ],
  "validation": {
    "sectionCount": 4,
    "warnings": [
      "Calendar: recurrent and past events are not displayed by any GoodBarber calendar source, mcms included. Weekly campground events must be entered as individual dated occurrences, or generated externally via Agenda + custom. The section renders empty with no error if this is missed.",
      "The first-party Weather extension exists but is a LAB item marked 'not yet available in GoodBarber' (checked 2026-08-13). The plan does not depend on it; re-check before building.",
      "Weather provider terms were deliberately not verified because no provider was chosen. Commercial use and in-app embedding are the two clauses to read; several free weather-widget licences cover websites only.",
      "All four createRoute values are null: three sections use mcms (eight tiles, no single provisioning URL) and the weather section takes no service, so the /manage/app/content-add-<service>/ pattern has nothing to key on. createRouteVerified is false throughout.",
      "No custom-code specification was written. The gap path requires all four checks to fail; GBModuleTypeCustom fits and the Weather extension exists-but-unreleased, so two checks passed. The Custom Code route is named as a costed option in section 3 instead."
    ]
  }
}
```

## Sources

- `ai-output/7-section-type-codenames.md` — type enum, catalog mapping and service tables, back-office capture 2026-08-12.
- `ai-output/4-structure-backoffice.md` — list/detail model, categories, section creation, per-app cap, 2026-08-11.
- [GoodBarber Extensions](https://www.goodbarber.com/extensions/) — extension inventory and pricing lines; Form, Push Notifications, Automatic Push, Geofencing and iBeacons all listed free, accessed 2026-08-13.
- [Content extensions category](https://www.goodbarber.com/extensions/categories/content/) — CMS Articles, CMS Agenda, CMS About, iCal/vCal and the custom feed family all listed *Free*; no Weather extension present, accessed 2026-08-13.
- [Weather extension (LAB)](https://www.goodbarber.com/extensions/weather/) — "Display weather data for the city of your choice", in a section or on Home; *"This feature is not yet available in GoodBarber."* Accessed 2026-08-13.
- [Events: iCal/vCal, WM Events, etc.](https://www.goodbarber.com/help/calendar-r41/events-ical-vcal-wm-events-etc-a21/) — *"Warning: we don't display past or recurrent events, this applies to all sources."* Feed URL configuration and Content API requirement for custom feeds, accessed 2026-08-13.
- [Plugin example: Weather by Geolocation](https://www.goodbarber.com/help/examples-and-tutorials-r110/plugin-example-weather-by-geolocation-a279/) — worked Custom Code weather plugin using the App API's `gbGetLocation` and `gbRequest`, accessed 2026-08-13.
- [NWS forecast — downtown Seattle](https://forecast.weather.gov/MapClick.php?lat=47.6062&lon=-122.3321) — the URL bound to section 3; current conditions plus 8-day outlook, responsive, no login, accessed 2026-08-13.
- [meteoblue weather widget — Seattle](https://www.meteoblue.com/en/weather/widget/three/seattle_united-states-of-america_5809844) — standalone widget URL, verified rendering 7 days in Fahrenheit and mph with the unit parameters applied, accessed 2026-08-13.
- [meteoblue — commercial / non-commercial use](https://content.meteoblue.com/en/about-us/legal/commercial-non-commercial-use) — free widgets are non-commercial only, bounded at fewer than 100 daily visitors or 50 daily data requests, and require a direct link back to meteoblue; commercial users must order business services. Accessed 2026-08-13.
- [api.weather.gov general FAQs](https://weather-gov.github.io/api/general-faqs) — no API key required, `User-Agent` header expected, `/points/{lat},{lon}` forecast flow, accessed 2026-08-13.
- [weather-gov/api discussion #312](https://github.com/weather-gov/api/discussions/312) — no `Access-Control-Allow-Origin` header; custom `User-Agent` triggers a preflight the API rejects; client-side use requires a proxy, accessed 2026-08-13.
- [Open-Meteo pricing](https://open-meteo.com/en/pricing) — *"The free API is for non-commercial use, rate-limited to 10,000 calls/day, and carries no uptime guarantee"*; CC BY 4.0 attribution, accessed 2026-08-13.
