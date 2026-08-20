
# `GBModuleType*` — as implemented in the iOS runtime

Extracted from `classic-05-2026` on 2026-08-20. Compare against §2 of `section-routing/SKILL.md` (captured from the back office on 2026-08-12).

## 0. Why the codebase writes `%@ModuleTypeX`

The literal `GBModuleTypeArticle` never appears in source. It is assembled at runtime:

```objc
// WeetJare/BGConstants.h:87-91
CG_INLINE NSString *GExplode(void)
{
    return [[[@"fGlBn" stringByReplacingOccurrencesOfString:@"f" withString:@""]
              stringByReplacingOccurrencesOfString:@"l" withString:@""]
              stringByReplacingOccurrencesOfString:@"n" withString:@""];
}
```

`"fGlBn"` minus `f`, `l`, `n` → **`"GB"`**. So `[NSString stringWithFormat:@"%@ModuleTypeArticle", GExplode()]` == `"GBModuleTypeArticle"`.

This is light obfuscation to keep the brand string out of the binary's literal table. Every type below is matched this way.

## 1. The parser

One function does all string → enum resolution: `SectionTypeWithString()` at `WeetJare/BGConstants.h:1194-1266`. Each branch accepts **three** aliases:

1. `GBModuleType<X>` — the current back-office codename
2. `GBSectionType<X>` — a legacy codename, same set
3. a bare lowercase word (`"article"`, `"video"`, …) — the oldest form

Unmatched input returns `SectionTypeUnknown` (`NSIntegerMax`), not a crash.

## 2. The table

`Enum` = the `SectionType` constant returned. `Value` = its integer, from `typedef NS_ENUM(NSUInteger, SectionType)` at `BGConstants.h:1142-1180`.

| Codename (`GB…`)              | Enum returned                    | Value | Role in the runtime                                                                                           |
| ----------------------------- | -------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------- |
| `GBModuleTypeArticle`         | `SectionTypeArticle`             | 0     | Text/article feed                                                                                             |
| `GBModuleTypeVideo`           | `SectionTypeVideo`               | 1     | Video feed                                                                                                    |
| `GBModuleTypePhoto`           | `SectionTypePhoto`               | 2     | Image gallery                                                                                                 |
| `GBModuleTypeSound`           | `SectionTypeSon`                 | 3     | Audio / podcast feed (enum keeps the French _son_)                                                            |
| `GBModuleTypeCustom`          | `SectionTypeCustom`              | 4     | Embedded web view                                                                                             |
| `GBModuleTypeTwitter`         | `SectionTypeTwitter`             | 5     | X (Twitter)                                                                                                   |
| `GBModuleTypeMap`             | `SectionTypeMap`                 | 6     | Geolocated points — **alias**                                                                                 |
| `GBModuleTypeMapdistant`      | `SectionTypeMap`                 | 6     | Same renderer, remote source — **alias**                                                                      |
| `GBModuleTypeMaps`            | `SectionTypeMap`                 | 6     | The name the back office emits — **alias**                                                                    |
| `GBModuleTypeFacebook`        | `SectionTypeFacebook`            | 7     | Facebook                                                                                                      |
| `GBModuleTypeAgenda`          | `SectionTypeEvent`               | 8     | Events / calendar (legacy word `"event"`)                                                                     |
| `GBModuleTypeBookmark`        | `SectionTypeBookmarks`           | 9     | Favorites (auto-added)                                                                                        |
| `GBModuleTypeSubmit`          | `SectionTypeSubmit`              | 10    | User content submission                                                                                       |
| `GBModuleTypeSettings`        | `SectionTypeSettings`            | 11    | App settings (auto-added)                                                                                     |
| `GBModuleTypePlugin`          | `SectionTypePlugin`              | 12    | Extension / Custom Code                                                                                       |
| `GBModuleTypeLive`            | `SectionTypeLive`                | 13    | Live audio / video stream                                                                                     |
| `GBModuleTypeContact`         | `SectionTypeContact`             | 14    | Contact details page                                                                                          |
| `GBModuleTypeAbout`           | `SectionTypeAbout`               | 15    | Single static page                                                                                            |
| `GBModuleTypeShop`            | `SectionTypeShop`                | 16    | External storefront                                                                                           |
| `GBModuleTypeForm`            | `SectionTypeForm`                | 17    | Form builder                                                                                                  |
| `GBModuleTypeQrcode`          | `SectionTypeQRCode`              | 18    | QR scanner                                                                                                    |
| `GBModuleTypeLoyalty`         | `SectionTypeLoyaltyCards`        | 19    | Loyalty cards — **alias**                                                                                     |
| `GBModuleTypeLoyaltycards`    | `SectionTypeLoyaltyCards`        | 19    | Loyalty cards — **alias**                                                                                     |
| `GBModuleTypeCouponing`       | `SectionTypeCouponing`           | 20    | Coupons / vouchers                                                                                            |
| `GBModuleTypeHome`            | `SectionTypeHome`                | 21    | Widget landing page (singleton)                                                                               |
| `GBModuleTypeSearch`          | `SectionTypeSearch`              | 22    | Cross-section search                                                                                          |
| `GBModuleTypeTos`             | `SectionTypeTerms`               | 23    | Legal page (auto-added, ×2)                                                                                   |
| `GBModuleTypeNode`            | `SectionTypeNode`                | 50    | Menu / sub-section container                                                                                  |
| `GBModuleTypeProfile`         | `SectionTypeUserProfile`         | 60    | User account / profile                                                                                        |
| `GBModuleTypeUserslist`       | `SectionTypeUserList`            | 61    | Directory of app users                                                                                        |
| `GBModuleTypeChat`            | `SectionTypeChat`                | 62    | User-to-user messaging                                                                                        |
| `GBModuleTypeProfileAdvanced` | `SectionTypeUserProfileAdvanced` | 63    | Extended profile — **alias**                                                                                  |
| `GBModuleTypeProfileadvanced` | `SectionTypeUserProfileAdvanced` | 63    | Lowercase-`a` spelling — **alias**                                                                            |
| `GBModuleTypeClickto`         | `SectionTypeClickToAction`       | 101   | Deep link / external link (meta section)                                                                      |
| `GBModuleTypeNotFound`        | `SectionTypeNotFound`            | 404   | Fallback screen — **alias**                                                                                   |
| `GBModuleType404`             | `SectionTypeNotFound`            | 404   | Fallback screen — **alias**                                                                                   |
| `GBModuleTypeCustomUrl`       | _(none)_                         | —     | **Not a section type.** Template discriminator inside a `Custom` section — `SectionCustomViewController.m:29` |

**37 accepted literals → 31 distinct section types**, plus one non-section literal (`CustomUrl`).

Enum members with no string form: `SectionTypeMetaSection` (100, a range boundary — see `SectionIsMetaSection()` at `BGConstants.h:1183-1192`) and `SectionTypeUnknown`.

## 3. Delta vs the back-office enum (skill §2)

### In the back office, absent from the iOS runtime — 5

|Codename|Consequence|
|---|---|
|`GBModuleTypeFakeclickto`|→ `SectionTypeUnknown`. Consistent with the skill's own note that it is a **link**: the server most likely rewrites it to `Clickto` before the config reaches the app.|
|`GBModuleTypeInstagram`|"Instagram" appears 174× in sources but never as a module type — it is an auth/share provider, not a section renderer.|
|`GBModuleTypeCommerce`|"Commerce" appears 152× but no `SectionTypeCommerce` exists.|
|`GBModuleTypeCommercealias`|idem|
|`GBModuleTypeCommercecollectionslist`|idem|

The `Commerce*` family is almost certainly served by a **different runtime**, not this Obj-C shell. Worth confirming before any plan emits those codenames for an iOS target.

### In the iOS runtime, absent from the skill — 9 new types

`Chat` (62) · `Userslist` (61) · `ProfileAdvanced` (63) · `Loyaltycards` (19) · `Couponing` (20) · `Map` / `Mapdistant` (6, aliases of `Maps`) · `NotFound` / `404` (404) · `CustomUrl` (not a section)

The skill's "thirty codenames" is the **catalog** vocabulary — what a user can add today. The runtime vocabulary is larger because it must also parse legacy configs and system screens that have no catalog tile.

### Practical takeaways for the routing agent

- **Aliasing is real.** `Maps`/`Map`/`Mapdistant`, `Loyalty`/`Loyaltycards`, `ProfileAdvanced`/`Profileadvanced`, `NotFound`/`404` all collapse. A validator that compares codename strings will report false mismatches.
- **The three-alias parser is a compatibility ramp**, not dead code. Old apps ship `"article"`; the current back office ships `GBModuleTypeArticle`.
- `GBModuleTypeSound` → `SectionTypeSon` and `GBModuleTypeAgenda` → `SectionTypeEvent` are the two places where the codename and the enum name diverge. Grepping the enum name to find a type will miss them.

## 4. Unrelated names (do not confuse)

`ModuleTypeChatList` and `ModuleTypeChatDetail` (`SettingsManager+ChatSection.h:29,36`) are **template** enums for rendering a Chat section. They share the `ModuleType` substring but are not section types.

## 5. Files used

|File|What it gave|
|---|---|
|`WeetJare/BGConstants.h`|`GExplode()` (l.87), the `SectionType` enum (l.1142), and `SectionTypeWithString()` (l.1194) — **the single source of truth**|
|`WeetJare/SectionCustomViewController.m`|`GBModuleTypeCustomUrl` (l.29)|
|`WeetJare/SettingsManager+SearchSection.h`|Confirms the six searchable content types (l.23-53)|
|`WeetJare/SettingsManager+ChatSection.h`|`ModuleTypeChatList` / `ModuleTypeChatDetail` (l.29,36) — false positives|
|`WeetJare/SettingsManager+ChatSection.m`|idem|
|`WeetJare/ChatDetailContentView.h`|idem|
|`WeetJare/ChatMessageCell.m`|idem|
|`WeetJare/ChatClassicCell.h`|idem|
|`WeetJare/ChatSearchCell.m`|idem|

Search performed: `grep -rEoh "[A-Za-z@%]*ModuleType[A-Za-z]+"` across the whole tree (7,831 files), all extensions. The nine files above are the complete set of hits.

## 6. Sources

- Codebase: `/Users/goodbarber/Downloads/classic-05-2026`, read 2026-08-20
- Back-office enum: `section-routing/SKILL.md` §2, captured 2026-08-12