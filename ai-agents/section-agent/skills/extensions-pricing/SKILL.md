---
name: extensions-pricing
description: Determine whether a GoodBarber capability is free, paid, plan-gated, already installed or experimental, and find extensions that no section type covers. Use whenever a planned section or feature might cost money, whenever a described capability has no matching section type, and before stating any price. Owns the live-lookup policy, the two separate extension stores, the constraint states an extension can be in, and the rule that a price is only ever quoted with the date it was checked. Do NOT use to choose a section type (use section-routing) or to write a specification for a feature that genuinely does not exist (use custom-code-spec).
---

# Extensions and Pricing

## 1. The lookup policy

Three vocabularies, three behaviours. This skill owns the third row, and the reason for the split.

| Vocabulary | Moves | Source of truth | Your behaviour |
|---|---|---|---|
| `GBModuleType*` codenames | barely — a native SDK enum | `section-routing` §2 | decide from the skill; never search, never invent |
| `service` values | slowly — grows with new connectors | `content-sections` §2 | prefer the known list; unlisted platform → look it up, mark `serviceVerified: false` |
| **Extensions and prices** | **fast — the catalog grows, prices change** | **the live store** | **look it up every time; quote nothing from memory** |

Why the asymmetry: picking a type is *classification over a stable closed vocabulary*, and it must be deterministic or the agent can't be tested. Pricing an extension is *lookup over a moving catalog*, and it must be fresh or it's actively misleading. Different problems, different mechanisms.

**Every price you state carries the date you checked it.** `"pricing": {"tier": "paid", "price": "$10/month", "asOf": "2026-08-13"}`. A price without a date is a claim you can't stand behind.

If the store is unreachable: fall back to §5's cached figures, and say so in the report — *"as of 2026-08-13, not re-verified this run."* Never present a cached price as current.

## 2. Two stores, not one

They overlap and are not identical. Query the one matching the app.

| Store | URL | Use for |
|---|---|---|
| Main catalog | `goodbarber.com/extensions/` | standard apps |
| eCommerce collection | `goodbarber.com/extensions/collections/ecommerce/` | Shop-plan apps |

Quoting shop prices to a blog app, or missing a shop-only extension because you searched the main catalog, are both real failure modes. Decide which store applies before searching.

Main catalog categories, as of 2026-08-13: Content · Local Shop · Memberships & Login · Monetization · Notifications · Essentials · Productivity · Tools for Developers, plus industry collections (eCommerce, restaurants, groceries, content creators, newspapers, online courses, radio).

## 3. Constraint states

An extension being listed does not mean it is available to this app. Each state changes what you tell the user.

| State | Meaning | What to say |
|---|---|---|
| **Free** | Available on all plans. Most of the catalog. | Proceed. Still date the claim. |
| **Plan-gated** | Free to use, unlocked from a given tier upward. | Name the required tier before planning around it. |
| **Paid** | A recurring fee, monthly or annual. | Quote the price and the date. Note a promotional rate as promotional. |
| **Installed by default** | Already active without anyone choosing it. | Don't plan an install — plan configuration. |
| **LAB / BETA** | Experimental. | Flag the maturity risk explicitly. `aistudio` (Create with AI) is one of these. |
| **In test until *date*** | A time-boxed trial. | State the expiry — the capability lapses without action. |

**Never name an extension without its state.** Uniform availability is a false assumption and one of the easiest ways to hand someone a plan they can't afford.

### Two lookup traps

**A hit count is not a match.** Store search is fuzzy; searching a capability word returns candidates whose descriptions have nothing to do with it. Read each candidate's own one-line description and confirm it describes the behaviour requested. A search returning nothing relevant is a legitimate finding — report it and move to the gap path.

**Read the pricing line, not the availability badge.** These contradict each other. A listing can show a "Free" chip in search results and "Available in all plans" on the install bar while the detail page reads *"Fees for the Standard and Premium offers. Free with the Pro offer."* **Available means installable, not free.** Open the detail page and quote the full pricing line.

## 4. Section or behaviour?

The structural question this skill answers, and the one that decides which array an item lands in.

Extensions integrate three ways:

**A — as a section.** The extension appears in "+ Add a section" and behaves like a native section. → `sections[]` with a type.

**B — as a sidebar console over sections.** More complex extensions get a top-level sidebar entry, which is a management console over the same section mechanism. Structurally still a section once instantiated. → `sections[]`.

**C — as a config screen, no section.** Installing adds an entry under an existing menu and opens its editor. Nothing appears in Structure. App-wide behaviours that aren't screens take this form. → `extensions[]` with `createsSection: false`.

**Do not assume A.** Onboarding walkthroughs, loyalty programs, discount codes, push, analytics, payment methods, abandoned-cart recovery and stock management are all mechanism C. Planning "install it, then add a section" for these sends someone looking for a section that will never exist.

The tell is usually in the description: if the capability happens *around* the app rather than *as a screen in it*, it's C.

## 5. Known figures — a fallback, not an answer

Captured 2026-08-13. **Verify before quoting.** Present here only so an offline run can say something useful with an honest caveat.

**Free** — the CMS families (Articles, Videos, Podcasts, Photos, Agenda, Map, Contact, About, Comments), Google Material Icons, Google Fonts, Custom Fonts, Genius Palette, Pexels, push notifications, geofencing, iBeacons, custom code tools, statistics and dashboards, all payment methods (Stripe, PayPal, Apple Pay, Klarna, and the rest), and the business integrations (Zapier, Make, Mailchimp, HubSpot, Google Sheets, Slack, Salesforce, and others).

**Paid, roughly by band:**

| Band | Extensions |
|---|---|
| ~$5/mo | App Walkthrough · Time Slots · User Groups · Quick Buy · Buy Again · Fast Checkout · Cart Reminder · Club Card · Stock Management |
| ~$8–15/mo | Appointment Booking · Local Delivery · Loyalty Program · Discount Codes · Abandoned Order |
| ~$20–55/mo | Chat · Live+ · RAG Chatbot ($35–55) |
| ~$25/mo | Product Import/Export |
| ~$49/mo | Memberships |

Two that come up often in structure planning:

- **RAG Chatbot** — `GBModuleTypePlugin` + `rag`. Paid, in the $35–55 band. Any "a chatbot that answers questions about my content" request lands here, and the price is high enough that it must be surfaced immediately rather than at the end.
- **App Walkthrough** — the canonical mechanism C. A first-launch overlay, not a section. "Show users how the app works" routes here, never to `sections[]`.

  Reported constraints, from the walkthrough editor via `ai-output/6-extensions-store.md` (2026-08-11): mobile only, a small fixed maximum number of screens (recorded as 5), and always skippable. **Verify the screen limit before designing to it** — it isn't in either back-office capture, and it's easy to confuse with the unrelated TabBar link cap. Say "a handful of screens, verify the exact limit" rather than asserting a number.

## 6. Dependencies

Some capabilities require another extension first. Planning the dependent one without the prerequisite produces a plan that can't be built.

- Anything **per-user** — synced data, personal lists, saved state across devices — requires **Authentication**.
- Anything **premium-gated** — paid content, subscriber-only sections — requires **Memberships** (~$49/mo).
- A custom-code feature storing data **per user rather than per device** inherits the Authentication requirement. See `custom-code-spec`.

State the prerequisite and its cost alongside the feature, not separately. "A personal reading list" that quietly needs a $49/month extension is not a plan anyone can act on.

## 7. Before emitting anything with a price

- [ ] Correct store queried for this app type — main catalog or eCommerce.
- [ ] Candidate confirmed by reading its own description, not by a search hit.
- [ ] Full pricing line read from the detail page, not the badge.
- [ ] Constraint state stated — free, plan-gated, paid, installed by default, LAB, in test.
- [ ] `asOf` date on every `pricing` object, free ones included.
- [ ] Integration mechanism decided — does this create a section or not?
- [ ] Mechanism C items in `extensions[]` with `createsSection: false`.
- [ ] Dependencies named with their own cost.
- [ ] If the lookup failed, the cached figure is labelled as unverified this run.
- [ ] An unfamiliar extension name was **looked up**, not treated as a gap.

---

*Sources: `ai-output/6-extensions-store.md` and the superseded `app-extensions` skill (constraint states, the badge-vs-pricing-line contradiction, the fuzzy-search caution, and the three integration mechanisms — back-office inspection 2026-08-11); [GoodBarber Extensions](https://www.goodbarber.com/extensions/) and [eCommerce extensions collection](https://www.goodbarber.com/extensions/collections/ecommerce/) for categories, tiers and the §5 figures, accessed 2026-08-13.*
