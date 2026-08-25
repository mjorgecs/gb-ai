# Objectives

## Description

This chapter defines the objectives of the internship project and the milestones expected at each stage.

As established in the introduction, GoodBarber's app-building process can be extended so that a user creates an application by **describing** it in natural language, rather than by manually assembling sections in the back office. The AI agent interprets that description and produces a first version of the app, which the user then customises and refines through the existing visual interface. The agent is therefore positioned as an **accelerator of the first draft**, not as a replacement for the platform's editor.

Turning that premise into a defensible proposal requires studying three things:

- **The existing solutions** — what other No-Code App Builders already ship, and how far they have taken description-driven building.
- **The available approaches** — which agent architectures (fully generative, strict assembler, hybrid) can be applied to a platform built around a closed, pre-tested component library.
- **The feasibility and the trade-offs** — cost, reliability, maintainability, and the risk of an agent producing output the platform cannot actually render.

The work is organised into three stages — **Research**, **Documentation** and **Implementation**. These are not strictly sequential: Documentation and Implementation run **continuously and in parallel**, so that every design decision made in the prototype is recorded while its rationale is still fresh, and so that the documentation describes the system that was actually built rather than the one that was originally imagined.

### Overview

| Stage             | Objective                                                                          | Main deliverable                                        |
| ----------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 1. Research       | Understand the market, the technology and the platform                             | Structured notes, section catalogue, comparative study  |
| 2. Documentation  | Justify the chosen approach and record its limits                                  | Report chapters (problem, solutions, challenges)        |
| 3. Implementation | Prove the approach works on GoodBarber's real component library                    | Working Proof of Concept + evaluation results           |

---

# 1. Research

The goal of this stage is to build the knowledge base the rest of the project depends on. Its output is not prose for the report yet, but organised, verifiable material.

### 1.1 State of the art

Map the No-Code App Builder market and the degree to which AI has been integrated into each platform's building process.

- **Deliverable:** a comparative overview of the relevant platforms, classified by the three integration scenarios defined in the introduction (fully AI builder, strict assembler, hybrid).
- **Success criterion:** each platform examined can be placed in one scenario, with a stated reason and a cited source.

### 1.2 Agentic AI

Understand how AI agents are designed and where they succeed or fail: the difference between a single prompted model and an agentic loop, the role of tools and skills, and the techniques that control the quality of the model's context (Prompt Engineering and Context Engineering).

- **Deliverable:** a synthesis of the techniques applicable to this project, with their advantages and disadvantages (Chapter *Context*).
- **Success criterion:** every technique described can be tied to a concrete design decision later taken in the prototype.

### 1.3 How the GoodBarber platform works

Use the platform as an end user: create a real application, add and configure sections, and observe the constraints the back office imposes.

- **Deliverable:** a working demonstration app, plus notes on the building flow, the configuration options exposed per section, and the points where a new user is most likely to hesitate.
- **Success criterion:** the building process can be described step by step, including which decisions the platform forces the user to make and in what order.

### 1.4 The platform's codebase and data model

Analyse the platform internals to extract the vocabulary the agent will have to speak: section type codenames, services (data sources), templates, and the rules that connect them.

- **Deliverable:** a catalogue of section types, services and templates, with each entry marked as *verified* (found in the codebase or in official documentation) or *inferred*.
- **Success criterion:** the catalogue is complete enough that a plan expressed in its vocabulary can be reproduced manually in the back office, and unverified entries are explicitly flagged rather than silently mixed in.

---

# 2. Documentation

This stage turns the research material into the argument of the report. It runs continuously alongside the implementation.

### 2.1 Problem definition

State the motivation: what is costly or slow in the current manual-assembly flow, who is affected, and why an AI-assisted flow is a plausible answer rather than a fashionable one.

- **Deliverable:** the *Introduction* and *Problem* chapters.
- **Success criterion:** the problem is stated independently of the proposed solution — a reader who disagrees with the solution should still recognise the problem.

### 2.2 Possible solutions

Describe the candidate approaches, compare them against the market solutions surveyed in 1.1, and justify the choice for GoodBarber specifically.

- **Deliverable:** the *Solutions* chapter, including the reasoning that rules the alternatives out.
- **Success criterion:** the justification refers to properties of GoodBarber's platform (closed component library, native SDK, existing back office), not to generic arguments that would apply to any platform.zc

### 2.3 Challenges and trade-offs

Document the costs and risks of the chosen approach: token cost and the pricing model of third-party AI APIs, context rot as the component catalogue grows, hallucinated component identifiers, the maintainability of AI-generated code, and the handling of requirements the platform cannot satisfy.

- **Deliverable:** the *Challenges* chapter, and, for each challenge, the mitigation adopted in the prototype (or an explicit statement that it was left unaddressed).
- **Success criterion:** no challenge is raised without either a mitigation or an acknowledged limitation.

### 2.4 Technical documentation of the prototype

Keep the prototype's own documentation current: its scope, its architecture, its invariants, and the reasoning behind each rule imposed on it.

- **Deliverable:** the agent's project file, system prompt and skill files, maintained as the implementation evolves.
- **Success criterion:** the documentation and the running prototype never disagree; a change in behavior is accompanied by the change in the document that caused it.

---

# 3. Implementation

The Proof of Concept aggregates the two previous stages into a working artefact: an AI agent that extracts an application's structure from a user's natural-language description and returns it as a **JSON object** describing the sections to create.

The PoC is deliberately **narrow**. It plans; it does not operate the back office, call GoodBarber APIs, or modify a live app. This restriction is what makes the output verifiable: a structure plan can be checked against the platform's real catalogue and reproduced by hand, whereas a live mutation could not be evaluated without risk.

### 3.1 Build the agent

A first working version — the **App Structure Agent** — is implemented. Its architecture reflects the Context Engineering conclusions of Stage 1:

- **A system prompt** defining the agent's role, its hard limits, and a **decision ladder** applied to every feature intent extracted from the description: decompose the request → decide whether the intent is a *screen* or a *behavior* → assign a section type → assign a service (data source) → check whether a `custom` source rescues the case → otherwise declare a one-line gap → assign a template.
- **Modular skills** rather than one monolithic prompt. The catalogue is split into `section-routing` (intent → type, output schema, validation), `content-sections`, `utility-sections` and `template-choices`, and the agent loads only what a given decision requires. This keeps the number of tokens in context proportional to the complexity of the request instead of to the size of the catalogue.
- **Closed vocabularies.** Type codenames, services and templates may only come from the skill tables. Inventing a plausible-looking identifier is treated as a defect, not as helpfulness.
- **Explicit uncertainty.** Every assignment carries a verification flag (`typeVerified`, `serviceVerified`, `templateVerified`), so an inference is visible in the output rather than indistinguishable from a verified fact. What the tables do not cover is reported as *undetermined* — neither invented nor assumed to be a gap.

### 3.2 Refine the agent

The remaining implementation work is qualitative: making the agent's output correct and consistent, not merely well-formed.

- Tighten the skill boundaries so that skill descriptions are distinct and routing is unambiguous — two skills that describe themselves similarly will both trigger, or neither will.
- Reduce output bloat: keep the JSON block as the deliverable and the surrounding prose as a short frame.
- Extend the catalogue coverage from the material produced in 1.4, adding table rows rather than special-case rules in the prompt.

- **Success criteria:** zero invented type, service or template identifiers across the test set; every inferred assignment flagged; the output validating against the declared schema on every run.

### 3.3 Evaluate the agent

Build a small evaluation set of application descriptions — short and vague, long and detailed, and descriptions containing at least one requirement the platform genuinely cannot satisfy — and measure the agent's behavior on it.

- **Deliverable:** a set of test prompts with the expected structure for each, and the observed results.
- **Success criteria:**
  - The structure plan is reproducible in the back office without correction.
  - Requirements outside the platform's capabilities are reported as gaps, not fabricated into sections.
  - Repeated runs on the same description produce equivalent plans.

### 3.4 Assess the integration path

Describe, without building it, how this planning agent would connect to the real platform: where the JSON plan would be consumed, what would have to be validated server-side, and which failure modes would have to be handled before real users could be exposed to it.

- **Deliverable:** a short integration analysis closing the report.
- **Success criterion:** the analysis identifies the concrete next engineering step, so the internship ends with a usable recommendation rather than only a demonstration.

---

## Out of scope

Stating what the project does **not** attempt keeps the objectives honest and the evaluation fair:

- **Generating application code.** The PoC assembles from the existing component library; it does not write custom components.
- **eCommerce applications.** The prototype targets content apps only.
- **Pricing and plan tiers.** The agent has no pricing data and must not supply one.
- **Modifying live applications.** The agent produces a plan; applying it remains a manual, human-reviewed step.

## Conclusion

Taken together, the three stages follow a single line: understand what the platform can already do (Research), justify why an assembler-style agent is the right way to expose it (Documentation), and demonstrate that an agent restricted to the platform's real vocabulary can turn a plain-English description into a structure a user could actually build (Implementation).
