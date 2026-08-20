# `service` — what the iOS runtime actually knows

Extracted from `classic-05-2026` on 2026-08-20. Compare against §2 of `content-sections/SKILL.md` ("The service tables", captured 2026-08-12).

## 0. The headline

**The runtime is almost entirely service-blind.** Of the ~26 distinct service strings the back office offers, the iOS app recognises **10**, and it branches on the section-level `service` field in only **four** places in 7,831 files.

This is not a gap — it is the architecture working as designed. The skill says it plainly:

```
[WordPress]──┐
[RSS]────────┼─→ server-side `service` adapter ─→ /front/get_items/… ─→ native app
[mcms CMS]───┘        (normalises to one item schema)      (identical for all)
```

The code confirms it from the other side: there is no WordPress parser, no RSS parser, no Substack anything. Items arrive pre-normalised. **`type` × `template` is what the binary consumes; `service` is a server-side concern that mostly never reaches it.**

## 1. Two different fields, easy to confuse

||`service`|`subtype`|
|---|---|---|
|Scope|the **section**|one **item**|
|JSON path|`gbsettings.sections.<id>.service`|on each item from `/front/get_items/…`|
|Read in|4 call sites|`ContentItem.m:55`, `Article.m:27`, `Video.m:19`, `Photo.m:26`, `Sound.m:36`, `Event.m:16`, `Comment.m:17`|
|Purpose|a handful of layout/base-URL decisions|pick the right renderer for _this_ item|

The `subtype` enums are where most service names survive into the app — and they exist only because a YouTube item and a Vimeo item need different players, not because the app fetches from either.

## 2. The service table, by `GBModuleType`

`Recognised` = a string the Obj-C source compares against. `Observed` = a value present in `WeetJare/Settings/initials_settings.json`, the shipped default config.

### `GBModuleTypeArticle`

|Service|Recognised|Where|Note|
|---|---|---|---|
|`wmaker`|✅|`BGConstants.h:1391` → `ArticleSubtypeWM`|item subtype|
|`wordpress`|✅|`BGConstants.h:1393` → `ArticleSubtypeWP`|item subtype|
|`tumblr`|✅|`BGConstants.h:1395` → `ArticleSubtypeTumblr`|**not in the skill's list** — legacy connector|
|`mcms`|observed|`initials_settings.json`|no branch; falls to `ArticleSubtypeUnknown`|
|`wmarticle`|observed|`initials_settings.json`|ditto|
|`wordpressdotcom` `rss` `substack` `medium` `squarespace` `blogger` `custom`|❌|—|invisible to the app|

Enum: `ArticleSubtype` (`BGConstants.h:1381`) — 3 known + `Unknown`.

### `GBModuleTypeVideo`

|Service|Recognised|Where|
|---|---|---|
|`wmaker`|✅|`BGConstants.h:1415` → `VideoSubtypeWM`|
|`youtube`|✅|`:1417` → `VideoSubtypeYouTube`|
|`dailymotion`|✅|`:1419` → `VideoSubtypeDailyMotion`|
|`rss`|✅|`:1421` → `VideoSubtypeRSS`|
|`videopodcast`|✅|`:1423` → `VideoSubtypePodcast`|
|`tiktok`|✅|`:1425` → `VideoSubtypeTikTok` — **not in the skill's list**|
|`vimeo`|observed|`initials_settings.json`|
|`wmvideo` `custom` `mcms`|❌|—|

Enum: `VideoSubtype` (`:1402`) — 6 known + `Unknown`. The only family matched **case-insensitively** (`[string lowercaseString]`); every other parser is case-sensitive.

### `GBModuleTypePhoto`

|Service|Recognised|Where|
|---|---|---|
|`wmaker`|✅|`BGConstants.h:1442` → `PhotoSubtypeWM`|
|`flickr`|✅|`:1444` → `PhotoSubtypeFlickr` — **marked `// Unused` in the enum**|
|`instagram`|✅|`:1446` → `PhotoSubtypeInstagram`, accepts both `"instagram"` and `"Instagram"`|
|`wmphoto` `custom` `mcms`|❌|—|

Enum: `PhotoSubtype` (`:1432`) — 3 known + `Unknown`.

### `GBModuleTypeSound`

| Service                                                              | Recognised | Where                                                                                                   |
| -------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------- |
| `podcast`                                                            | ✅          | `BGConstants.h:1462` → `SoundSubtypePodcast`                                                            |
| `soundcloud`                                                         | ✅          | `:1464` → `SoundSubtypeSoundCloud`; also drives `ContentItemTypeSoundCloudArtist` (`ContentItem.m:134`) |
| `anchor` `spreaker` `ausha` `simplecast` `wmpodcast` `custom` `mcms` | ❌          | —                                                                                                       |

Enum: `SoundSubtype` (`:1453`). **Unmatched input returns `Podcast`, not `Unknown`** — the only parser whose fallback is a real value.

A `SoundsListTypeWithStringAndService()` that would have branched on `soundcloud` sits **commented out** at `BGConstants.h:2084-2096`.

### `GBModuleTypeAgenda`

|Service|Recognised|Where|
|---|---|---|
|`mcms`|✅|`BGConstants.h:1479` → `EventSubtypeMCMS`|
|`facebookevents`|observed|`initials_settings.json` — **not in the skill's list**|
|`vcalendar` `wmevent` `custom`|❌|—|

Enum: `EventSubtype` (`:1471`) — 1 known + `Unknown`. The thinnest of the five.

### `GBModuleTypeMaps`

**No subtype enum at all.** `kml` appears only as a bundled test-fixture file extension (`SettingsManager+MapSection.m:395-401`), never as a service string. Map points arrive fully normalised.

### `GBModuleTypeLive` — the one type where `service` genuinely drives behaviour

|Service|Effect|
|---|---|
|`livevideo`|`LiveListTypeVideoClassic`|
|`liveradio`|`LiveListTypeRadioClassic`|
|`liveplus`|`LiveListTypeRadioPlus` — **not in the skill's list**|

`LiveListTypeWithStringAndService()` at `BGConstants.h:2156-2173` is the only function in the codebase that takes `service` as a first-class argument. One template (`GBLiveListTemplateTypeClassic`) resolves to three different layouts depending on it.

### `GBModuleTypeCustom`

|Service|Effect|
|---|---|
|`airtable`|web-view base URL forced to `https://airtable.com/` — `SettingsManager+CustomSection.m:73-79`|

Every other `Custom` service falls through to the section's own configured URL.

### `GBModuleTypeSubmit` — `service` means something else entirely

`SubmitServiceType` (`BGConstants.h:2022`) takes `"article"` / `"photo"` / `"video"` — **what kind of content users may submit**, not where data comes from. Same field name, different vocabulary. Don't validate it against the connector list.

### `GBModuleTypeTos` — `service` holds a template string

`SettingsManager+TermsSection.m:21` reads `sectionObject["service"]` and passes it to `TermsSectionTypeWithString()`, which expects `GBtosTemplateTypeTos` / `…Privacy`. The `service` key is reused as a discriminator. Another false friend.

### `GBModuleTypeHome` (widgets)

`SettingsManager+Widgets.m:1975` checks only whether `service` **exists**, to decide a default shape. The value is never read.

### Types with no service at all

`Node` · `Plugin` · `Profile` · `Settings` · `About` · `Form` · `Contact` · `Search` · `Qrcode` · `Clickto` · `Bookmark` · `Chat` · `Userslist` · `Shop` · `Facebook` · `Twitter` · `Loyaltycards` · `Couponing`

Caveat: the shipped default config gives **`About` and `Form`** a `service: mcms` even though no code reads it. Presence of the key is not evidence the runtime uses it.

## 3. Everything observed in the shipped default config

`WeetJare/Settings/initials_settings.json`, 30 sections:

|Section type (as written in the JSON)|service|
|---|---|
|`GBSectionTypeArticle`|`mcms`, `wmarticle`|
|`GBSectionTypeVideo`|`vimeo`|
|`GBSectionTypePhoto`|`flickr`|
|`GBSectionTypeSound`|`podcast`, `soundcloud`|
|`GBSectionTypeAgenda`|`facebookevents`|
|`GBSectionTypeMaps`|`mcms`|
|`GBSectionTypeAbout`|`mcms`|
|`GBSectionTypeForm`|`mcms`|
|`GBSectionTypeLive`|`liveradio`|
|`GBSectionTypeFacebook`|`facebook`|
|`GBSectionTypeTwitter`|`twitter`|
|`GBSectionTypeCustom` `Map` `Node` `Plugin` `Profile` `Settings` `Submit`|_(absent)_|

**Note the prefix: `GBSectionType…`, not `GBModuleType…`.** The shipped defaults use the legacy alias that `SectionTypeWithString()` also accepts. Both spellings are live; a validator must accept either.

## 4. Delta vs the skill's tables

**In the skill, invisible to the runtime — 16 of 26:**

`wordpressdotcom` · `substack` · `medium` · `squarespace` · `blogger` · `wmarticle`* · `anchor` · `spreaker` · `ausha` · `simplecast` · `wmpodcast` · `wmvideo` · `wmphoto` · `vcalendar` · `wmevent` · `kml` · `custom`

* present in the default config but matched by no branch.

**`custom` never appears as a service anywhere in the codebase.** This is the strongest confirmation of the skill's §4 argument: a `custom` feed is indistinguishable from an `mcms` feed by the time it reaches the app.

**In the runtime, missing from the skill — 5:**

|Service|Type|Note|
|---|---|---|
|`tumblr`|`Article`|legacy; likely retired from the back office|
|`tiktok`|`Video`|a _video subtype_, distinct from the `Fakeclickto` TikTok link tile|
|`facebookevents`|`Agenda`|in the shipped defaults|
|`liveplus`|`Live`|third live variant|
|`airtable`|`Custom`|the only service that changes a `Custom` section's behaviour|

`tiktok` deserves care: the skill routes "a TikTok section" to `Fakeclickto` (a link-out). But `VideoSubtypeTikTok` exists, meaning TikTok items _can_ render natively inside a `Video` feed. Two different features sharing one brand name.

## 5. What this means for the routing agent

- **Never validate a service against the iOS source.** Absence proves nothing — 16 perfectly valid services have no code presence by design.
- **`service` is not one vocabulary.** It is a connector name on content types, a content-kind on `Submit`, a template name on `Tos`, and a presence-flag on widgets. Validate per type, exactly as the skill's §8 checklist already requires.
- **`Live` is the exception worth remembering.** It is the one place where getting the service wrong changes what the user sees, because template and service jointly determine the layout.
- **Both `GBModuleType…` and `GBSectionType…` are live.** The runtime accepts both; the shipped config uses the latter.

## 6. Files used

|File|What it gave|
|---|---|
|`WeetJare/BGConstants.h`|all five `*Subtype` enums and parsers (l.1381-1484); `SubmitServiceType` (l.2022); `LiveListTypeWithStringAndService` (l.2156); the commented-out SoundCloud branch (l.2084)|
|`WeetJare/Settings/initials_settings.json`|the 30-section shipped default config — the only place real `service` values appear together|
|`WeetJare/SettingsManager+CustomSection.m`|the `airtable` branch (l.73-79)|
|`WeetJare/Section Tos/SettingsManager+TermsSection.m` / `.h`|`service` reused as a template discriminator (l.21 / l.20-29)|
|`WeetJare/SettingsManager+Widgets.m`|presence-only `service` check (l.1975)|
|`WeetJare/ContentItem.m`|`subtype` key (l.55); SoundCloud artist special case (l.134)|
|`WeetJare/Article.m` · `Video.m` · `Photo.m` · `Sound.m` · `Event.m` · `Comment.m`|per-item `subtype` key declarations|
|`WeetJare/SettingsManager+PhotoSection.m`|`instagram` settings sub-object (l.26)|
|`WeetJare/SettingsManager+MapSection.m`|`kml` as a bundled fixture, not a service (l.395-401)|
|`WeetJare/JSONSettings.h`|`service` key constants for Sounds (l.328) and Live (l.353)|

## 7. Sources

- Codebase: `/Users/goodbarber/Downloads/classic-05-2026`, read 2026-08-20
- Back-office service tables: `content-sections/SKILL.md` §2, captured 2026-08-12
- Companion notes: `ai-output/module-type-enum-ios-runtime.md`, `ai-output/template-catalog-ios-runtime.md`