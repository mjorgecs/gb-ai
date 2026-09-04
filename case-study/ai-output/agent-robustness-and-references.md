# Making the Section Agent Objective + 4 Reference Repos

Date: 2026-09-02 · Scope: `ai-agents/section-agent/`

---

# Part 1 — Why your agent is unpredictable, and how to fix it

## 1.1 The root cause, in one sentence

**There is no code anywhere in your loop.** The routing, the vocabulary lookup, *and* the validation all happen inside the model's head. Every rule in your repo is a suggestion the model may or may not weigh — including the rules whose whole job is to stop it from guessing.

Your files total ~1,050 lines of instruction (150 system prompt + ~860 skills + 46 CLAUDE.md). Not one line is enforceable.

## 1.2 Named failure modes, traced to your files

| # | Failure mode | Where it comes from | Symptom |
|---|---|---|---|
| 1 | **Non-deterministic context** | `SYSTEM-PROMPT.md` L9: *"DO NOT start reading all files… Read the others only when the decision requires them"* | Which tables are in context varies per run → same input, different output. This alone explains most of the unpredictability. |
| 2 | **Closed enum lives in prose** | `section-routing` §2 — 28 codenames in a Markdown table | Nothing *prevents* `GBModuleTypeNews`. You wrote "never invent one" 5+ times across 3 files; that repetition is the tell that it isn't enforceable. |
| 3 | **The model validates itself** | `section-routing` §8 — 16 checkboxes | Models pass their own checklists. This is your single biggest robustness gap. |
| 4 | **Contradictory instructions** | "You must be **FAST**, don't read files" vs. a 7-step ladder + 16-item checklist. "Ask ALWAYS when you have a question" vs. "at most two lines of prose before the JSON" | The model has to arbitrate. Arbitration *is* variance. |
| 5 | **Policy triplicated, never checked** | no-prices / no-eCommerce / no-custom-code appear in `CLAUDE.md`, `SYSTEM-PROMPT.md`, and `section-routing` §8 | Three copies drift apart. And a rule stated 3× but never checked is weighted by salience, not by truth. |
| 6 | **Schema given as one example instance** | `section-routing` §7 | Cardinality, required-vs-optional, allowed values, and conditionals ("gap ⇒ `alternatives` required") are prose bullets. Unenforceable, and ambiguous to the model. |
| 7 | **Overloaded uncertainty model** | `status` (3 values) × 4 `*Verified` booleans = 48 states, with boundaries decided by prose | `gap` vs `undetermined` is a fresh judgment call on every run. Guaranteed to flip between runs. |
| 8 | **No test set** | `examples/` has 2 hand-written outputs | You cannot tell whether a prompt edit made things better or worse. You are debugging blind. |

## 1.3 The file-format question — verdict

You're **half right**. The problem isn't Markdown; it's that you're using *one* format for *three* different jobs. Split by role:

| Content | Today | Should be | Why |
|---|---|---|---|
| Closed vocabularies (28 codenames, catalog→type map, service tables, template families) | MD tables inside skills | **YAML / JSON data files** | This is data to be *looked up and validated against*, not read. |
| The output contract | prose + one example JSON | **JSON Schema** (or a Pydantic model) | Machine-checkable; generates your validator for free. |
| Decision ladder, disclosures, house style | MD | **stays MD** | This is genuinely instruction. Markdown is the right format for it. |
| Test cases | none | **YAML fixtures** | `input → expected output`, diffable. |

**Why not XML.** XML's advantage in LLM work is delimiting *regions of a prompt* (`<rules>…</rules>`) so the model doesn't blur them together. That's a prompt-structuring trick, not a data format. For actual data, YAML/JSON wins: real parsers, real validators, clean git diffs, and you can generate code from it.

> ⚠️ **The trap:** converting your MD tables to YAML *and changing nothing else* buys you nothing. YAML pasted into a prompt is still just text the model reads. The win only arrives when the YAML is (a) loaded by code and (b) used to validate the output. **Format ≠ enforcement.**

## 1.4 Target architecture — the deterministic sandwich

Code decides everything that can be decided by code. The LLM only does the part that genuinely needs judgment.

```
user description
      │
 [LLM]  decompose ──────────► intents[]  {id, text, kind: screen|behaviour}
      │                       (schema-constrained output)
      │  ── for each intent, independently ──
      │
 [CODE] retrieve ───────────► candidate types  (filter vocabulary.yaml;
      │                        don't dump all 28 every time)
      │
 [LLM]  choose ─────────────► {type, service, template, confidence, notes}
      │                        constrained to the candidate enum
      │
 [CODE] validate ───────────► JSON Schema + custom rules
      │       ├─ fail ──► feed the error list back, retry (max 2)
      │       └─ fail twice ──► status: "undetermined"   (never a guess)
      │
 [CODE] assemble ───────────► final report JSON
                              (dedupe Home, strip auto-added, order, policy scan)
```

## 1.5 Concrete changes, ordered by payoff ÷ effort

**1. Extract the vocabularies into `data/*.yaml`.** `types.yaml`, `catalog.yaml`, `services.yaml`, `templates.yaml`. Encode as *fields* what your prose currently states in sentences:

```yaml
- codename: GBModuleTypeFakeclickto
  role: Link-out styled as a native section
  takes_service: false
  has_template: false
  auto_added: false
  catalog_tiles: [TikTok, Reddit, WhatsApp, Discord, Threads, Snapchat]
  mandatory_disclosure: >-
    This is a branded link that opens the external app, not embedded content.
```

The skills then *reference* the data instead of containing it. Kills failure mode #1 outright — code decides what's in context, not the model.

**2. Write the output contract as JSON Schema.** Generate the `enum` from `types.yaml` (never hand-copy — that's how the two drift). Use `additionalProperties: false` (this alone stops a stray `customCode` field), and conditional requires:

```json
{ "if":   { "properties": { "status": { "const": "gap" } } },
  "then": { "required": ["alternatives"] } }
```

**3. Validate outside the model.** A `validate.py` running the schema plus the rules a schema can't express: `Home` appears ≤ 1×; no auto-added section is ever *created*; every `Fakeclickto` carries its disclosure; the template family prefix matches the type. Your §8 checklist stops being 16 hopeful checkboxes and becomes ~60 lines of Python that cannot be talked out of its answer.

**4. Retry on validation errors — don't retry blind.** Feed the validator's error list back as the next turn: *"`GBModuleTypeNews` is not in the enum; nearest candidates are …"*. **This is your single biggest reliability win.** PydanticAI ships it as `ModelRetry`; LangGraph does it with a conditional edge back to the model node (see repo #1 below).

**5. One decision per LLM call.** Today, one call does: decompose + a 7-step ladder × N features + assembly + self-validation. Split it. Small prompts with a single job are dramatically more repeatable — and each stage becomes independently testable.

**6. Retrieve, don't dump.** 28 types fit in a prompt fine. Services × templates do not, and they'll grow. Filter candidates in code before the LLM sees them. Smaller candidate set = smaller hallucination surface.

**7. Move policy out of the prompt and into the pipeline.** "No prices", "nothing eCommerce" become a deny-list scan over the emitted JSON. One implementation, one place, actually enforced — instead of the same sentence written three times and checked zero times.

**8. Replace the tri-state judgment with a number.** Keep `status` in the output, but have the *model* emit `confidence: 0.0–1.0` per decision and have *code* map it to the status (high → `matched`, low → `undetermined`). Models score a single decision far more consistently than they apply a prose boundary. Likewise, `serviceVerified` should be computed — "is this string a key in `services.yaml`?" is a lookup, not a judgment.

**9. Kill the contradiction in your house style.** Pick one: either the agent asks questions mid-run (output is a conversation, untestable), or it always emits a report with an `openQuestions[]` array (testable). Take the second.

**10. Build 15–20 golden cases** in `tests/cases/*.yaml` — description + expected sections. Run each **3×** and measure agreement across runs. That self-consistency number *is* your predictability metric. Right now you have 2 examples and no score.

**Also:** temperature 0, and pin the model version. Free wins.

### Suggested layout after the refactor

```
section-agent/
  data/           types.yaml  catalog.yaml  services.yaml  templates.yaml
  schema/         app-structure.schema.json      (enum generated from data/)
  prompts/        decompose.md  choose.md        (small, one job each)
  skills/         section-routing/  content-sections/  …  (prose only)
  src/            pipeline.py  retrieve.py  validate.py  assemble.py
  tests/cases/    *.yaml
```

---

# Part 2 — 4 reference repositories

All four are Python, verified live on 2026-09-02, and all match your shape: **interpret a description → select from a source → emit a structured report**.

---

## EASY · single-agent — LangGraph Data Enrichment Template

🔗 <https://github.com/langchain-ai/data-enrichment> · MIT · ~235★ · official LangChain template

### Overview

You give it a **topic** plus a **JSON extraction schema**; one agent searches, extracts, and returns JSON conforming to your schema. It is the closest published analogue to your agent that exists, and it's ~500 lines total.

The mapping to your problem is almost 1:1 — the schema is *supplied as input* rather than baked into a prompt, which is exactly change #2 above.

### Structure

```
src/enrichment_agent/
  graph.py          the whole agent: 3 nodes + 2 routers
  state.py          InputState / State / OutputState
  tools.py          search, scrape_website
  prompts.py        the single main prompt
  configuration.py  model, max_loops, prompt — all injectable
tests/              unit + integration
ntbk/testing.ipynb  calling it via the API
```

### Files that matter to you

- **`graph.py` — read this one first, top to bottom.** Three things to steal:
  1. **The output schema is bound as a *tool*, not described in prose.** The `info_tool` dict takes `state.extraction_schema` as its `parameters`, and the model is bound with `tool_choice="any"`. The model physically cannot emit a shape that isn't the schema. → your change #2.
  2. **The `reflect()` node is a *separate LLM call* with its own structured output** (`InfoIsSatisfactory`: `reason[]`, `is_satisfactory`, `improvement_instructions`). A second pass judging the first, not the same pass judging itself. → your change #3.
  3. **`route_after_checker()` loops back to the model on failure, bounded by `max_loops`.** Unsatisfactory output is returned as a `ToolMessage` with `status="error"` carrying the specific improvement instructions. → your change #4, in ~20 lines.
- **`state.py`** — separate input / internal / output schemas. Your report should be an `OutputState`, not "whatever the model printed".
- **`configuration.py`** — the prompt is configuration, not a constant. Makes A/B testing prompts trivial.

> This repo is your primary reference. If you read only one, read this one.

---

## EASY · multi-agent — Resume Optimization Crew (CrewAI)

🔗 <https://github.com/tonykipkemboi/resume-optimization-crew> · CrewAI

### Overview

Three agents — Job Analyzer, Resume Analyzer, Company Researcher — read a job posting and a résumé, score the match, and write **three JSON files** to `output/`. Small, complete, and it is the cleanest example of *declaring agents as data* rather than as prose.

### Structure

```
src/resume_crew/
  config/agents.yaml    ← the 3 agents: role, goal, backstory  (YAML, not prose!)
  config/tasks.yaml     ← the 3 tasks: description, expected_output, output_file
  models.py             ← Pydantic models = the output contract
  crew.py               ← wires agents + tasks + tools
  main.py               ← inputs
knowledge/              ← the source documents (résumé PDF)
output/*.json           ← the reports
```

### Files that matter to you

- **`config/agents.yaml` + `config/tasks.yaml`** — this is the direct answer to your format question. Agent identity and task contracts live in YAML; only the *reasoning guidance* stays prose. Compare against your 148-line `SYSTEM-PROMPT.md`, where role, procedure, schema and policy are all one undifferentiated block.
- **`models.py`** — Pydantic models with `Field(description=...)` per field. CrewAI passes these as `output_json`, so the JSON is validated by the library, not hoped for. Your `SectionPlan` / `AppStructure` models go here.
- **`tasks.yaml` → `output_file:`** — note that "produce a report" is *configuration*, not something the prompt asks nicely for.
- **`knowledge/`** — CrewAI's knowledge-source pattern: the source corpus is a directory, loaded by the framework. This is where your `data/*.yaml` vocabulary would live.

> Steal the **agents.yaml / tasks.yaml / models.py** three-way split. It's the shape your `section-agent/` should have.

---

## MEDIUM · single-agent — Local Deep Researcher

🔗 <https://github.com/langchain-ai/local-deep-researcher> · MIT · official LangChain

### Overview

One agent, one state object, one loop: generate a query → search → summarise → **reflect to find knowledge gaps** → generate a follow-up query → repeat N times → emit a Markdown report with sources. Runs fully locally against Ollama/LMStudio.

Harder than #1 because of the iterative state accumulation, but still only 6 files.

### Structure

```
src/ollama_deep_researcher/
  graph.py          the loop: generate_query → web_research → summarize → reflect → route
  state.py          SummaryState — accumulates sources + running summary across loops
  prompts.py        one prompt per node
  configuration.py  max_web_research_loops, use_tool_calling, provider…
  utils.py          search adapters, source deduplication/formatting
  lmstudio.py       provider glue
```

### Files that matter to you

- **`graph.py`** — the `reflect_on_summary` node. It asks the model *"what do you still not know?"* and turns the answer into the next query. This is what your Step 0 decomposition should become: an explicit node whose output is inspectable and correctable, instead of a silent step buried in a ladder.
- **`configuration.py` → `use_tool_calling`** — read the README's *Model Compatibility Note*. Some models can't reliably produce JSON, so there are **two output strategies plus a fallback**. This is the mature version of the problem you're hitting: it treats "the model produced malformed output" as an expected engineering case with a coded fallback, not as a prompt to be reworded.
- **`state.py`** — one typed state object threaded through every node, so you can dump it mid-run and see exactly what the agent believed at step 3. Your agent has no inspectable intermediate state at all; that's a large part of why it feels buggy rather than merely wrong.
- **`prompts.py`** — one small prompt per node. Contrast with your single 148-line prompt doing five jobs.

---

## MEDIUM · multi-agent — GPT Researcher · `multi_agents/`

🔗 <https://github.com/assafelovic/gpt-researcher/tree/master/multi_agents> · Apache-2.0 · ~23k★ on the parent repo

### Overview

A LangGraph team of 8 agents (inspired by the STORM paper) that plans, researches, **reviews, revises**, writes and publishes a 5–6 page report. Deliberately the most complex of the four — but each agent file is small and single-purpose, so it stays readable.

Read this one for the **orchestration and the review loop**, not for the research.

### Structure

```
multi_agents/
  agent.py           ChiefEditorAgent — builds the LangGraph StateGraph
  main.py            entrypoint
  task.json          ← the run contract: query, guidelines, max_sections, formats
  langgraph.json     deployment config
  agents/
    orchestrator.py  the master graph: nodes, edges, parallel subtopic branches
    editor.py        plans the outline  (≈ your Step 0 decomposition)
    researcher.py    gathers per subtopic
    reviewer.py      ← validates a draft against `guidelines`
    reviser.py       ← rewrites from reviewer feedback; loops until accepted
    writer.py        assembles the final report
    publisher.py     writes md / pdf / docx
    human.py         optional human-in-the-loop node
  memory/            shared state definitions
```

### Files that matter to you

- **`agents/reviewer.py` + `agents/reviser.py` — the reason this repo is on the list.** Two *separate* agents in a bounded loop: one only criticises, one only fixes. Neither judges its own work. This is your §8 checklist done properly. Read these two files together; they're short.
- **`task.json`** — especially the `guidelines: []` array. The rules a report must satisfy are **input data**, not prompt text — so they can be changed, versioned and tested without touching a prompt. Your "no prices / no eCommerce / no custom-code spec" invariants belong exactly here, and `follow_guidelines` toggles the reviewer loop on and off.
- **`agents/orchestrator.py`** — how a supervisor graph is actually wired: conditional edges, and the fan-out that runs each subtopic's research→review→revise cycle in **parallel**. This is the model for processing your `intents[]` independently instead of in one giant call.
- **`agents/editor.py`** — plan-then-execute. The outline is produced and *fixed* before any research runs, so downstream steps can't quietly redefine the task. Your decomposition should be frozen the same way.

---

## Suggested reading order

1. **`data-enrichment/graph.py`** — the schema-as-tool + reflect + retry loop. This is your architecture.
2. **`resume-optimization-crew/config/*.yaml` + `models.py`** — how to split data from prose. This is your file layout.
3. **`gpt-researcher/multi_agents/agents/{reviewer,reviser}.py` + `task.json`** — separated validation, and rules-as-data.
4. **`local-deep-researcher/configuration.py` + README compat note** — how to survive a model that won't emit clean JSON.

---

## Sources

- [langchain-ai/data-enrichment](https://github.com/langchain-ai/data-enrichment) — README + `src/enrichment_agent/graph.py`
- [tonykipkemboi/resume-optimization-crew](https://github.com/tonykipkemboi/resume-optimization-crew) — README + `src/resume_crew/` tree
- [langchain-ai/local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) — README + `src/ollama_deep_researcher/` tree
- [assafelovic/gpt-researcher · multi_agents](https://github.com/assafelovic/gpt-researcher/tree/master/multi_agents) — README + `multi_agents/agents/` tree
- [langchain-ai/rag-research-agent-template](https://github.com/langchain-ai/rag-research-agent-template) — *bonus*: query routing (relevant / ambiguous → ask / out-of-scope) as a graph node, and retrieval over a local corpus
- Your files: `ai-agents/section-agent/{CLAUDE.md, SYSTEM-PROMPT.md, skills/*}`
