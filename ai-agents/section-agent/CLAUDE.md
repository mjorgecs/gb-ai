# App Structure Agent — Project File

Scope note: this file governs work **inside `section-agent/`**. The repository root `CLAUDE.md` describes the internship project as a whole; this one describes the agent being built here.

## What this agent is

An agent that turns a plain-English app description into a GoodBarber structure plan: section types, services, prices, and — where the platform has no answer — a developer-ready custom-code specification.

It is a **planning** agent. It reads a description and writes a document. It does not operate the back office, call GoodBarber APIs, or modify a live app.

## Layout

```
section-agent/
  CLAUDE.md            this file
  SYSTEM-PROMPT.md     the agent's role, decision ladder and invariants
  skills/
    section-routing/   intent → type; owns the enum, output schema, validation
    content-sections/  Article · Photo · Video · Sound · Maps · Agenda
    utility-sections/  static pages, forms, links, social, live, QR, search
    commerce-sections/ the Shop product line
    extensions-pricing/ free vs paid, plan gates, live store lookup
    custom-code-spec/  the gap path
  examples/            worked runs used as regression tests
```

## Ground rules

**Never invent a `GBModuleType*` codename.** The enum is the one closed vocabulary in the system. An unknown extension is a lookup; an unknown type is a gap. A constant that looks real but isn't is the worst possible output.

**Types and services come from the skills; extensions and prices come from the site.** Codenames barely change and must be deterministic. Prices change monthly and must be fresh. Every price carries an `asOf` date.

**Mark inference.** `typeVerified`, `serviceVerified`, `createRouteVerified` exist so a guess is visible. Use them.

**Both halves of a gap.** A gap answer without alternatives is incomplete; a gap answer without a custom-code spec is incomplete. Always both.

## Output

One Markdown report per run, containing a fenced JSON block. Schema and report structure live in `section-routing`. Per the root `CLAUDE.md`, generated reports go to `ai-output/`.

## When changing a skill

1. Check the claim against `section-docs/0-section-type-codenames.md` first. If it isn't there and isn't on goodbarber.com, it doesn't go in unlabelled.
2. Re-run the four examples in `examples/`. They exist to catch regressions, particularly the two that are designed to be failed by a careless agent (`02-wish-list-gap`, `04-shop-with-loyalty`).
3. Keep skill descriptions distinct. They are how the agent routes; two skills that describe themselves similarly will both trigger or neither will.
