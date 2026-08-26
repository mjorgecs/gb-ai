# The App Structure Agent

## Description

The introduction closed by announcing that the remainder of the report would examine the **Hybrid Approach** — an agent that assembles pre-tested components and is additionally authorised to generate custom code when the component library falls short. The prototype built for this project does not do the second half. It is a **strict assembler**: it selects from closed vocabularies, and where nothing fits it says so in one line and stops.

This chapter documents that agent — what it is, how it is structured, why the prototype narrowed to the assembler position, and what that narrowing costs.

### The assembler approach

Under the assembler model — the second of the three integration scenarios set out in the introduction, and the one the established no-code platforms occupy in practice [^1] — the agent never writes a component. Its entire job is **interpretation followed by selection**: read a natural-language description, decompose it into discrete feature intents, and match each intent against a fixed catalogue of things the platform already builds and already tests.

What makes this tractable in GoodBarber's case is that a section is not one choice out of a hundred catalogue tiles. It is **three orthogonal choices**, each drawn from its own vocabulary:

| Axis | The question it answers | Consumed by | Owned by |
| --- | --- | --- | --- |
| `type` | What shape is this data, and how is it rendered? | the native app | `section-routing` |
| `service` | Where does the data come from? | the server | `content-sections` |
| `template` | How is it drawn? | the design layer | `template-choices` |

**The agent produces a plan, not the app.** The section JSON in a live app is a presentation contract whose structural fields are read-only. The agent's output is consequently a **plan of actions**: an ordered list of sections, each with the type, service and template it needs.

```
user's description
        │
        ▼
┌───────────────────────┐
│  App Structure Agent  │  ← the prototype: interprets and selects
└───────────────────────┘
        │  structure plan (JSON): sections[] + extensions[]
        ▼
┌───────────────────────┐
│  Implementation Step  │  ← out of scope: manipulates the JSON in the live app
└───────────────────────┘
		|  and inserts the new sections/extensions.
        ▼
  back office / live app
```

Restricting the prototype to planning is what makes it *evaluable*. A structure plan can be checked against the platform's real catalogue and reproduced by hand in the back office.

### The agent's structure

The agent is assembled from three layers, separated by **how often each one changes** rather than by subject matter.

| Layer | File | What it holds | When it is in context |
| --- | --- | --- | --- |
| Project file | `CLAUDE.md` | Scope, ground rules, layout, and the procedure for editing a skill. Addressed to whoever maintains the agent. | Always |
| System prompt | `SYSTEM-PROMPT.md` | Role, the four hard limits, the decision ladder, the uncertainty model, house style. | Always |
| Skills | `skills/*/SKILL.md` | The catalogue itself — types, services, templates, disclosures, validation. | On demand |

The split exists because the three layers have different lifetimes. The ground rules change when the *project's* scope changes, the ladder changes when the *reasoning* is found to be wrong, and the tables change every time GoodBarber ships a new feature. Keeping the fast-moving material in files that are loaded only when needed means the catalogue can grow without the always-resident context growing with it.

**The four hard limits** are stated in the system prompt as invariants rather than preferences: no prices, content apps only (no eCommerce), no custom-code specifications, and no web access. The last one is the strongest: the skills are the entire world the agent knows. It cannot browse, so it cannot silently repair a gap in its own tables with a plausible guess from the open web.

**The decision ladder** runs once per feature intent. Each step exists because skipping it produces a specific, known wrong answer.

| Step | Decision                                                       | What it does                                                                                                                                                                                                                                  |
| ---- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0    | Decompose the description into discrete intents                | Interprets the user input: "a page with news and photos" is divided into two sections (news + photos).                                                                                                                                        |
| 1    | Screen, or behaviour?                                          | Decides either the user's requirements are screen sections (e.g.: `GBModuleTypePhoto` -> `sections[]`) or behaviors (e.g.: Push notifications -> `extensions[]`).                                                                             |
| 2    | Assign exactly one `GBModuleType*`                             | Uses the tables from the `section-routing` skill to assign one `GBModuleType*`.                                                                                                                                                               |
| 3    | Assign the `service`                                           | Uses the tables from the `content-sections` skill to assign the `service` (e.g.: mcms).                                                                                                                                                       |
| 4    | Check `custom` before assuming that the section does not exist | Suggests the `custom` service when the section does not exist and the user can access the URL of the desired service (e.g.: a "weather section", which does not exist, can be a `custom` section connected to a weather forecast web viewer). |
| 5    | Gap path — one line plus alternatives                          | When there is no matching extension, marks the requirement as `gap` or `undetermined` and suggests alternatives (equivalent extensions).                                                                                                      |
| 6    | Choose the template                                            | Uses the tables from the `template-choices` skill to assign the correct template.                                                                                                                                                             |
| 7    | Validate, then emit                                            | Validates all the prevoius steps.                                                                                                                                                                                                             |

**Uncertainty is a first-class output.** Every section carries one of three statuses, and the third is the one that makes the closed-world design honest:

| Status | Meaning |
| --- | --- |
| `matched` | A type was found. |
| `gap` | The platform genuinely has no shape for this — it is not a feed, a page, a form or a link. |
| `undetermined` | It may well exist — a newer connector, an extension the tables do not cover — but the agent cannot confirm it and will not guess. |

Alongside the status, four boolean flags (`typeVerified`, `serviceVerified`, `templateVerified`, `createRouteVerified`) mark every individual claim as observed or inferred.

### Context tools: the skills

#### How a skill is structured

A skill is a directory containing a `SKILL.md` file that opens with YAML frontmatter carrying two required fields — `name` and `description` [^3]. That small header is the whole routing mechanism, and it works through **progressive disclosure**, which loads context in three stages [^4]:

1. **Metadata.** At startup, only each skill's name and description are pre-loaded into the system prompt — enough for the agent to know *when* a skill applies without paying for its contents.
2. **Body.** If the agent judges a skill relevant to the decision in front of it, it reads the full `SKILL.md` into context.
3. **Referenced files.** A skill too large for one file can point at bundled files, loaded only if the task reaches them.

Two consequences shape how this agent's skills are written. First, the `description` field is not documentation, it is a **router**: the project file therefore requires that skill descriptions stay mutually distinct, because two skills that describe themselves similarly will either both trigger or neither will. Each of the four descriptions accordingly ends with an explicit *Do NOT use for…* clause pointing at its neighbour. Second, the system prompt tells the agent which skill is the entry point and instructs it not to read the others speculatively — progressive disclosure only saves tokens if the agent actually defers.

#### The four skills

| Skill              | Loaded when                                             | Owns                                                                                                                                                                               |
| ------------------ | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `section-routing`  | Every request — the entry point                         | The closed `GBModuleType*` enum, the catalogue-name→type map, the intent→type table, the condensed ladder, the output schema, the validation checklist                             |
| `content-sections` | The intent is a repeating feed of items                 | The six list-plus-detail types (`Article`, `Photo`, `Video`, `Sound`, `Maps`, `Agenda`), their service tables, the shared list/detail/categories model, and the `custom` feed rule |
| `utility-sections` | The intent is a single page, a link, a form or a stream | Static pages, contact, forms, submissions, search, QR, menus, web views, live streams, social types, the auto-added four, and the `Fakeclickto` disclosure                         |
| `template-choices` | A template is anything other than the default           | The two-slot list/detail model, the family prefixes per type, the default table, and the description signals that justify a deviation                                              |

**The number of skills is not fixed.** Four is the current answer, not a designed constant — the split follows _where the decisions are_, so it tracks the catalogue rather than the type enum. Any part of the platform that develops a genuinely distinct decision earns a skill of its own: the widgets that compose a `GBModuleTypeHome` landing page are the obvious next candidate, since assembling a home screen out of widgets is a different question from routing an intent to a section, and answering it inside `section-routing` would mean loading widget guidance on every request that has nothing to do with the home screen. The reverse holds too — a skill that stops carrying a decision of its own is folded back into its neighbor. What is fixed is the rule governing the split, and the two boundaries it has to stay between. **One skill** would load every type, every service and every template on every request; most of it is irrelevant to any single app, and long context is exactly where the model's ability to recall and reason accurately begins to degrade — _context rot_ [^5]. **One skill per type** would put thirty near-identical descriptions in the router, so routing would trigger unreliably, and a four-section app would pull in four skills. Splitting on decisions rather than on subject matter is what keeps a growing catalogue away from both, and it is what the existing four already reflect: `GBModuleTypeArticle` has ten services and needs a page of guidance, while `GBModuleTypeQrcode` has none and needs one line.

---

## Why the shift from hybrid to assembler?

The hybrid model promises more than the assembler does, and the introduction argued for it. The prototype nevertheless gave up its generative half. Four reasons justify that, and each one carries a cost.

### It is simpler to build

An assembler needs to explain far less to the model. It does not need a code-generation contract, a sandbox, a review path for generated components, or a policy for what happens when generated code fails in production. The interaction with the user reduces to interpreting requirements and matching them against tables.

- **Advantage:** Correctness is verifiable rather than merely plausible. Every claim in the output is either a verbatim table entry or an explicitly flagged inference, so a reviewer can audit a plan without running it.
- **Disadvantage:** The agent's ceiling is the catalogue's ceiling. Any requirement the component library does not cover is answered with a one-line gap, no matter how well the agent understood the intent.

### It works directly with the platform

The output is a JSON object expressed in the platform's own vocabulary — real `GBModuleType*` codenames, real service identifiers, real template codenames. It slots into the existing app structure rather than describing a parallel one.

The plan is also **reproducible by hand**: a user can follow it in the back office, section by section, and end up with the app it describes. That is what makes the prototype demonstrable without any platform integration existing yet.

- **Advantage:** Nothing has to be re-engineered to consume the output. The plan is already in the platform's terms, so the integration question is *where to apply it*, not *how to translate it*.
- **Disadvantage:** The vocabularies are captured from a live back office at a point in time, so a renamed codename or a restructured provisioning route silently invalidates the tables, and the agent has no way to detect that it has gone stale.

### Design stays on the user's side

Design is the characteristic least affected by this approach, and deliberately so. The agent selects sections, services and templates; it does not choose colours, fonts, headers or navigation styling. GoodBarber already applies a global **App Style** across every page of the app, and every new section arrives with a working default design that the owner can then override per section [^7].

The prototype leans on that. `template-choices` enforces a **default-first rule** — the default template is the answer unless the description gives a positive reason to leave it, and a deviation costs a line in `notes` quoting the phrase that justified it.

- **Advantage:** The division of labour is clean and matches the platform's own model — the agent resolves *which services the app needs*, the user keeps the aesthetic decisions, and the first draft is never visually wrong in a way the user cannot fix trivially.
- **Disadvantage:** A user who described a *look* rather than a *function* gets less than they asked for. Design is a large part of what people mean by "build me an app", and an agent that consistently returns the default may read as unresponsive to the description it was given.

### It consumes fewer tokens

Because the vocabularies are fixed and the output is a short JSON object, the reasoning is a series of narrow lookups rather than open-ended generation. 

- **Advantage:** Lower cost per run and faster responses, with a smaller context in which the model is measurably more accurate [^5].
- **Disadvantage:** Terseness is enforced by rule, not by judgement. A caveat that genuinely warranted a paragraph gets a sentence in `notes`, and a non-expert user may need exactly the explanation the budget removed.

---

## Challenges

Three difficulties remain open. Each is stated with the mitigation the prototype actually adopted, or with an explicit statement that it was left unaddressed.

### Detailed and contextualised information

The agent can only match a requirement against something it can describe. Sections are the easy part — they were captured from a live back office — but **extensions, services and templates are documented unevenly**. Template descriptions in particular are mostly inferred from their codenames rather than observed, three template families have known irregularities (the detail family is called `Detail` on some types and `Content` on others; `Maps` has both; `Photo` has no captured detail family at all), and the Extensions store carries far more capability than the section catalogue exposes.

*Mitigation adopted.* Uncertainty is made visible instead of being resolved by guessing. Every table states the date it was known good and declares itself non-exhaustive; the `templateVerified` flag marks any template chosen on a reading of its name; irregularities are recorded as irregularities rather than smoothed into a false pattern; and the `undetermined` status exists so that *"this may exist but I cannot confirm it"* never has to masquerade as either a match or a gap.

*What remains unaddressed.* The extension catalogue is not covered at all. An app whose central requirement is served by an extension will receive an `undetermined`, which is honest but not useful.

### Keeping the structure accessible to the user

The plan is written in the platform's internal vocabulary — `GBModuleTypeFakeclickto`, `serviceVerified`, `GBArticleListTemplateTypeEnriched`. That is what makes it executable and what makes it verifiable, and it is also unreadable to the non-expert user the tooling is ultimately for. A user who cannot read the plan cannot correct it, and an uncorrected first draft is one the user abandons.

*Mitigation adopted.* Two mechanisms. First, every section carries an **`intent` field written in the user's own terms**, one line, placed beside the codenames — so the decomposition made in Step 0 is visible and correctable without the reader needing to know what a `GBModuleType*` is. Second, the system prompt requires the agent to **ask before it emits**: open questions are resolved in conversation with the user and never left in the finished document, because the value of a plan depends directly on the specificity of the description behind it, and most users describe their apps briefly and vaguely [^8].

*What remains unaddressed.* The plan is still a JSON block. Rendering it as something a non-technical user reads comfortably is a presentation problem this prototype does not attempt.

### Maintaining the context window

This is the structural challenge of the assembler model. The agent's competence is a snapshot: the enum was captured on a specific date, the service tables the same. GoodBarber ships connectors, extensions and templates continuously, and a table that silently falls behind produces an agent that confidently declares gaps where the platform has since grown a capability. Left alone, the failure mode is not a visible error but a slow, invisible narrowing of what the agent believes the platform can do.

*Mitigation adopted.* Three partial defences. Counts are never treated as limits — the skills record them as *"known as of <date>"* snapshots, and the agent is forbidden from refusing a plan on the basis of a number it does not actually know. Growth is absorbed by **adding a table row, not a rule**, so the catalogue can expand without the prompt becoming the brittle accumulation of edge cases that chapter *Context* warns against [^5]. And the failure direction is chosen deliberately: an unknown capability degrades to `undetermined`, so an out-of-date agent says *less* rather than something wrong.

*What remains unaddressed.* None of this refreshes the tables. Doing so requires **scheduled re-capture** of the back office enum, the service lists and the extension store, together with a diff against the current skills — a maintenance process, not a prompt. Until that exists, the agent's accuracy has a half-life, and how long that half-life is has not been measured.

---

## What this chapter does not settle

Three questions are deliberately left to later work: whether the agent's plans are *correct* at scale, which requires the evaluation set that does not yet exist; where the JSON plan would be consumed inside the real platform and what server-side validation it would need; and whether the assembler's ceiling is low enough, in practice, to justify reopening the hybrid model's generative half for the cases the catalogue cannot reach.

---

## Sources

[^1]: Brown, M. (2026). _10 Best No-Code AI App Builders in 2026: Tested + Compared._ Zite. [https://www.zite.com/blog/no-code-ai-app-builder](https://www.zite.com/blog/no-code-ai-app-builder)

[^2]: GoodBarber. (2026). _Understand app sections and structure._ GoodBarber Help Center, last updated July 2026. [https://www.goodbarber.com/help/organize-your-content-r93/understand-app-sections-and-structure-a34/](https://www.goodbarber.com/help/organize-your-content-r93/understand-app-sections-and-structure-a34/) — the section families, the connector model, and the documented 120-section per-app limit. Accessed 2026-08-26.

[^3]: Anthropic. (2026). _Agent Skills._ Claude Platform Documentation. [https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

[^4]: Anthropic. (2026). _Equipping agents for the real world with Agent Skills._ Anthropic Engineering. [https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

[^5]: Rajasekaran, P., Dixon, E., Ryan, C., & Hadfield, J. (2025). _Effective context engineering for AI agents._ Anthropic Engineering. [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

[^6]: OpenAI. (2026). _What are tokens and how to count them?_ OpenAI Help Center. [https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them) — the word-count-to-token ratio used for the estimates above, which are approximations and not measured counts.

[^7]: GoodBarber. (2026). _Design individual sections._ GoodBarber Help Center. [https://www.goodbarber.com/help/design-of-your-sections-r89/section-design-a106/](https://www.goodbarber.com/help/design-of-your-sections-r89/section-design-a106/) — the global App Style, per-section overrides, and the separate "Edit the design" entry points for a list and its detail page.

[^8]: Zi, Y., Menon, H., & Guha, A. (2025). _More Than a Score: Probing the Impact of Prompt Specificity on LLM Code Generation._ arXiv. [https://arxiv.org/abs/2508.03678](https://arxiv.org/abs/2508.03678)
