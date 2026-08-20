
# `GB…TemplateType*` — the template catalog in the iOS runtime

Extracted from `classic-05-2026` on 2026-08-20. Companion to `module-type-enum-ios-runtime.md`.

## 0. How template names are built

Same obfuscation trick as the section types, but with **two** helpers:

```objc
// WeetJare/BGConstants.h:87
GExplode()  →  "GB"        // @"fGlBn"  minus f, l, n

// WeetJare/BGConstants.h:1487
TExplode()  →  "Template"  // @"Ttaemeremenpshortlettaaentstringe"
                           // minus ta, mere, en, short, et, string
```

So the source never contains the literal. It writes:

```objc
[NSString stringWithFormat:@"%@ArticleDetail%@TypeToolBarUp", GExplode(), TExplode()]
```

which resolves at runtime to **`GBArticleDetailTemplateTypeToolBarUp`**.

**Grep pattern that finds them all:** `stringWithFormat:@"%@[A-Za-z0-9]*%@Type[A-Za-z0-9]*"`

Every family has a `<Family>TypeWithString()` parser next to its `typedef enum`, and every parser also accepts a bare lowercase legacy word (`"classic"`, `"grid"`, …) — identical three-alias design to `SectionTypeWithString()`.

## 1. The naming grammar

```
GB  +  <Family>  +  Template  +  Type  +  <Variant>
        │                               │
        │                               └── Classic, Grid, ToolBarUp, VisualCard…
        └── Article, Video, Photo… suffixed by the SLOT it fills
```

The **slot suffix** is the part that matters and is easy to miss:

|Suffix|Slot it fills|
|---|---|
|`…List`|the section's index screen|
|`…Detail`|the item screen's _chrome_ — toolbar position, swipe behaviour|
|`…Content`|the item screen's _body_ — header image, layout of the text|

`Article`, `Video` and `Sound` are the only types with all three slots. That is why one article section carries three independent template fields, not one.

## 2. Templates by section type

Counts are distinct variants. `Enum` is the `typedef enum` the parser returns.

### `GBModuleTypeArticle` — 29 templates

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBArticleListTemplateType…`|`ArticleListType` (`BGConstants.h:1537`)|17|Classic · ClassicUne · Grid · UneGrid · Visuels · SlideShow · MinimalColor · MinimalPhotos · Checkerboard · Immersive · Enriched · Condensed · VisualCard · VisualCardCondensed · GridVisualCard · VisualCardGridVisualCard · ImmersiveStorySlideCondensed|
|`GBArticleDetailTemplateType…`|`ToolbarType` (`:1587`)|7|Classic · ToolBarUp · ToolBarSlide · ToolBarSlideGrenadine · ToolBarAndroid · ToolBarSwipe · ToolBarInsideUp|
|`GBArticleContentTemplateType…`|`ArticleContentType` (`:1643`)|5|Classic · Banner · BannerNoNavBar · BannerInfos · ClassicGrenadine|

### `GBModuleTypeVideo` — 18

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBVideoListTemplateType…`|`VideoListType` (`:1733`)|11|Classic · ClassicUne · Grid · UneGrid · Visuels · SlideShow · MinimalColor · MinimalPhotos · Enriched · VisualCard · VisualCardCondensed|
|`GBVideoDetailTemplateType…`|`ToolbarType` (`:1587`)|7|Classic · ToolBarUp · ToolBarSlide · ToolBarSlideGrenadine · ToolBarAndroid · ToolBarSwipe · ToolBarInsideUp|

`VideoList` is `ArticleList` minus 6 variants — the two share their parser branch at `BGConstants.h:1738-1758`.

### `GBModuleTypeSound` — 14

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBSoundDetailTemplateType…`|`ToolbarType` (`:1587`)|7|Classic · ToolBarUp · ToolBarSlide · ToolBarSlideGrenadine · ToolBarAndroid · ToolBarSwipe · ToolBarInsideUp|
|`GBSoundListTemplateType…`|`SoundsListType` (`:2064`)|4|Classic · SoundCloud · GrenadinePodcast · Enriched|
|`GBSoundContentTemplateType…`|`SoundsContentType` (`:2103`)|3|Classic · Banner · ClassicGrenadine|

### `GBModuleTypePhoto` — 10

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBPhotoListTemplateType…`|`PhotoListType` (`:1778`)|10|Classic · List · Visuels · Instagram · Pinterest · Flickr · Fullsize · Square · Edgetoedge · VisualCard|

`Instagram` and `Flickr` here are **layout names**, not data sources.

### `GBModuleTypeMaps` — 15

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBMapsListTemplateType…`|`MapsListType` (`:1863`)|9|Single · Multi · MultiDistant · Classic · Grid · Visual · SplitView · Enriched · SplitEnriched|
|`GBMapsContentTemplateType…`|`MapsContentType` (`:1895`)|4|Classic · Banner · HTML · ClassicGrenadine|
|`GBMapsDetailTemplateTypeClassic`|—|1|Classic|
|`GBMapDistantListTemplateTypeClassic`|`MapsListType`|1|Classic (alias of `MultiDistant`)|

### `GBModuleTypeAgenda` — 9

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBEventContentTemplateType…`|`EventsContentType` (`:1978`)|4|Classic · Banner · BannerCustom · Cover|
|`GBAgendaListTemplateType…`|`EventsListType` (`:1930`)|4|Classic · OldClassic · Expandable · Map|
|`GBEventListTemplateTypeCondensed`|`EventsListType`|1|Condensed|

Note the split: the **list** family is spelled `Agenda…`, the **content** family `Event…`. Same section type.

### `GBModuleTypeNode` — 11

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBNodeListTemplateType…`|`NodeListType` (`:2421`)|11|Classic · Visuels · VisuelsColor · UneGrid · UneGridColor · Grid · GridColor · List · ListColor · Scratch · SlideShow|

The `…Color` variants are separate constants that collapse onto the same enum member (`BGConstants.h:2428-2434`) — the colour flag is read elsewhere.

### `GBModuleTypeChat` — 6

|Family|n|Variants|Source|
|---|---|---|---|
|`GBChatListTemplateType…`|3|Square · Rounded · NoPhoto|`SettingsManager+ChatSection.m:67-71`|
|`GBChatDetailTemplateType…`|3|Square · Rounded · NoPhoto|`SettingsManager+ChatSection.m:80-84`|

### `GBModuleTypeLoyaltycards` — 5

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBLoyaltyListTemplateType…`|`LoyaltyCardsListType` (`:2270`)|3|Square · Rounded · Progress|
|`GBRewardListTemplateType…`|— (`:2320`)|2|Classic · Minimal|

### `GBModuleTypeCouponing` — 5

|Family|n|Variants|Source|
|---|---|---|---|
|`GBCouponListTemplateType…`|3|Visual · Classic · Minimal|`SettingsManager+CouponingSection.h:20-24`|
|`GBCouponingContentTemplateType…`|2|Banner · Minimal|`SettingsManager+CouponingSection.h:40-42`|

### `GBModuleTypeBookmark` — 4

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBBookmarkListTemplateType…`|`BookmarksListType` (`:2002`)|4|ClassicOld · Distant · Download · Classic|

### `GBModuleTypeTwitter` — 4

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBTwitterListTemplateType…`|`TwitterListType` (`:1815`)|4|Classic · Banner · Photo · Profile|

### `GBModuleTypeLive` — 4

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBLiveListTemplateType…`|`LiveListType` (`:2153`)|4|RadioClassic · VideoClassic · Classic · Plus|

### `GBModuleTypeTos` — 4

|Family|n|Variants|Source|
|---|---|---|---|
|`GBtosTemplateType…`|2|Tos · Privacy|`Section Tos/SettingsManager+TermsSection.h:23-25`|
|`GBCommercetosTemplateType…`|2|Tos · Privacy|same lines|

Lowercase `tos` in the family position — the only family that isn't CamelCase.

### `GBModuleTypeUserslist` — 3

|Family|n|Variants|Source|
|---|---|---|---|
|`GBUserslistTemplateType…`|2|Classic · Grid|`BGConstants.h:2239-2241`|
|`GBUserListContentTemplateType`|1|_(no suffix)_|`BGConstants.h:2256`|

### `GBModuleTypeAbout` / `Contact` / `Facebook` — 2 each

|Family|Enum|n|Variants|
|---|---|---|---|
|`GBAboutListTemplateType…`|— (`:2220`)|2|BannerImage · BannerImageAndTitle|
|`GBContactListTemplateType…`|— (`:2200`)|2|Classic · Button|
|`GBFacebookListTemplateType…`|`FacebookListType` (`:1838`)|2|Classic · ClassicOld|

### Single-template types — 1 each

|Codename|Enum|Section type|
|---|---|---|
|`GBCustomListTemplateTypeClassic`|`CustomListType` (`:2536`)|`Custom`|
|`GBShopListTemplateTypeClassic`|— (`:2544`)|`Shop`|
|`GBSubmitListTemplateTypeClassic`|`SubmitListType` (`:2045`)|`Submit`|
|`GBSettingsListTemplateTypeClassic`|`SettingsListType` (`:2123`)|`Settings`|

`GBPluginTemplateTypeClassic` exists too, but `PluginListTypeWithString()` (`:2141`) **ignores its argument entirely** and always returns Classic — a plugin section has no template choice.

## 4. Totals

||Count|
|---|---|
|Families (`<X>TemplateType`)|46|
|Distinct template constants|**210**|
|Section types that own at least one|24 of 31|

Types with **no** template family: `Form`, `Search`, `Qrcode`, `Clickto`, `Profile`, `ProfileAdvanced`, `NotFound`.

## 5. Declared in the default JSON but never parsed

`WeetJare/Settings/initials_settings.json` ships these codenames, and no `…WithString()` function accepts them. They fall through to a default:

`GBFormListTemplateTypeClassic` · `GBProfileTemplateTypeClassic` · `GBPluginTemplateTypeClassic` · `GBAgendaDetailTemplateTypeToolbarUp` · `GBSettingsDetailTemplateTypeClassic` · `GBSubmitDetailTemplateTypeClassic` · `GBTwitterDetailTemplateTypeClassic` · `GBMapListTemplateTypeClassic` · `GBBookmarkTemplateType{Condensed,Enriched,VisualCard}` · `GBInfosTemplate` · `GBWidgetTemplate` · `GBLoyaltyGiftsListTemplate`

Note `GBAgendaDetailTemplateTypeToolbarUp` — lowercase `b` in _Toolbar_, unlike every parsed `ToolBarUp`. Placeholders, not live values.

## 6. Traps

- **`Sound` list is `SoundList`, but its enum is `SoundsListType`** (plural). Same for `Maps`/`MapsList` vs `MapDistantList` (singular). Family spelling is not derivable from the section type — it must be looked up.
- **`Agenda` vs `Event`** — one section type, two family prefixes.
- **`…Color` variants are not separate layouts.** `NodeListTemplateTypeGrid` and `…GridColor` return the same enum member.
- **A section carries up to three template fields**, one per slot. Emitting only a `List` template leaves Detail and Content at their defaults.
- **`ArticleDetail`, `VideoDetail` and `SoundDetail` share one enum** (`ToolbarType`) with identical variants. Three codename prefixes, one behaviour.

## 7. Files used

|File|What it gave|
|---|---|
|`WeetJare/BGConstants.h`|`TExplode()` (l.1487) and 36 of the 46 families with their enums (l.1508-2596)|
|`WeetJare/SettingsManager+Widgets.h`|`WidgetContent` (26), `WidgetNavigation` (12), `WidgetNewsletter` (l.156-238)|
|`WeetJare/SettingsManager+ChatSection.m`|`ChatList`, `ChatDetail` (l.67-84)|
|`WeetJare/SettingsManager+CouponingSection.h`|`CouponList`, `CouponingContent` (l.20-42)|
|`WeetJare/Section Tos/SettingsManager+TermsSection.h`|`tos`, `Commercetos` (l.23-25)|
|`WeetJare/SettingsManager+LoginView.h`|`LoginTemplate` enum (l.95)|
|`WeetJare/SettingsManager+NodeSection.m`|Node template reads (l.300, 319, 338, 350, 839)|
|`WeetJare/SettingsManager.m`|Minimal-template special case (l.7664-7666)|
|`WeetJare/InternalLinksManager.m`|Confirms enum names in use (l.123, 219-247)|
|`WeetJare/SectionNodeSlideShow.m`|`GBNodeListTemplateTypeSlideShow` as a design path (l.170)|
|`WeetJare/Settings/initials_settings.json`|Shipped defaults + the 13 unparsed codenames of §5|
|`WeetJare/WeetTonsorem-Prefix.pch`|Confirms no `GB` prefix macro — the prefix is only ever runtime-built|

## 8. Sources

- Codebase: `/Users/goodbarber/Downloads/classic-05-2026`, read 2026-08-20
- Section type enum: `ai-output/module-type-enum-ios-runtime.md`, same date