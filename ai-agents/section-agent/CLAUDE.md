# App Structure Agent — Project File

Scope note: this file governs work **inside `section-agent/`**. The repository root `CLAUDE.md` describes the internship project as a whole; this one describes the agent being built here.

## What this agent is

An agent that turns a plain-English app description into a GoodBarber structure plan: for each feature, a section type, a service and a template — or, where the platform has no answer, a one-line gap.

It is a **planning** agent. It reads a description and writes a document. It does not operate the back office, call GoodBarber APIs, or modify a live app.

**Scope, deliberately narrow.** Content apps only. No pricing, no eCommerce, no custom-code specifications, and no web access — the skills are the entire world the agent knows. Each of those was removed on purpose, because each one made the agent slower and its output longer without making it more correct.

## Layout

```
section-agent/
  CLAUDE.md            this file
  SYSTEM-PROMPT.md     the agent's role, decision ladder and invariants
  skills/
    section-routing/   intent → type; owns the enum, output schema, validation
    content-sections/  Article · Photo · Video · Sound · Maps · Agenda
    utility-sections/  static pages, forms, links, social, live, QR, search
    template-choices/  list + detail design templates for the six content types
```

No `examples/` folder exists yet. If worked runs are added later as regression tests, they go there.

## Ground rules

**Never invent a `GBModuleType*` codename**, service or template. These are closed vocabularies. A constant that looks real but isn't is the worst possible output.

**The skills are the whole world.** Types, services and templates all come from the tables in the skills, and nothing comes from the web. A platform, extension or capability that isn't in a table is not a lookup and not automatically a gap — it is `undetermined`, and the agent says what it doesn't know instead of guessing or searching.

**Mark inference.** `typeVerified`, `serviceVerified`, `templateVerified` and `createRouteVerified` exist so a guess is visible. Use them.

**A gap is one line.** No type, no service, no extension → name the gap, list the nearest real alternatives, stop. The agent does **not** write a custom-code specification, design a replacement feature, or describe how one could be built.

**Never state a price, plan tier or cost.** The agent has no pricing data and must not supply one from memory.

## Output

One Markdown report per run whose **main content is a fenced JSON block**. Prose is a short frame around it, not the deliverable. Schema, report structure and the prose budget live in `section-routing` §7.

## When changing a skill

1. Check the claim against `section-docs/0-section-type-codenames.md` first. If it isn't there and isn't on goodbarber.com, it doesn't go in unlabelled. *(This applies to **you**, editing the skills — the agent itself never browses.)*
2. Keep the skills' vocabulary closed: adding a table row is how the agent learns something new.
3. Keep skill descriptions distinct. They are how the agent routes; two skills that describe themselves similarly will both trigger or neither will.
