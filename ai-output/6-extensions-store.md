# The GoodBarber Extensions Store

This report covers the **Extensions Store** (`Extensions Store` in the left sidebar) — GoodBarber's marketplace of installable features layered on top of the Structure/App Style system already documented in `4-structure-backoffice.md` and `5-appstyle-edition-json.md`. Findings are based on direct inspection of the ReBook back office and GoodBarber's in-product help documentation, accessed 2026-08-11.

## 1. What the Extensions Store Is

The store's own tagline: *"Get the most out of your app with our Extension Store — more than 190 extensions for your project."* It is reached from the left sidebar (`Extensions Store`), which expands into three groups: **Extensions** (All extensions / Management), **Look** (Themes — the Themes Library from the App Style report), and **Services** (Reseller — white-label reselling tools, out of scope here).

**Relationship to Structure's section catalog**: the ~120 section types catalogued in `4-structure-backoffice.md` §4 are a *subset* of the Extensions Store, specifically its **Content** collection (branded there as "the integrated CMS": CMS Articles, CMS Videos, CMS Podcasts, CMS Photos, CMS Agenda, CMS Map, CMS Contact, CMS About, Bookmark — all free, all addable directly from Structure's "+ Add a section"). The Extensions Store's remaining ~70+ entries are things that are *not* simple content sections: third-party service integrations (Zapier, Make, Stripe-adjacent monetization tools), account/permission systems (Authentication, User groups), whole AI-powered tools (see §3), design-asset libraries (Google Fonts, Pexels), and raw developer primitives (the Custom Code family). In short: **Structure's section catalog is what you can add as a navigable screen; the Extensions Store is everything you can add to the app, full stop** — sections are one category among several.

**Categories**: Content, Memberships & Login, Monetization, Notifications, Essentials, Productivity, Tools for developers, Lab, plus a catch-all "All categories." A search bar sits above them (functional — tested with "MCP," returned one precise match).

**Pricing model**: extensions carry one of several badges/prices, not a single scheme:
- **Free** — the majority, including all CMS/content types and most integrations (Zapier, Make, Authentication, Chat, etc.).
- **Plan-gated free** — e.g. Memberships is "Free | Available from the Premium offer. Free with the Pro offer": free to use, but only unlocked on certain GoodBarber subscription tiers.
- **Flat annual add-on price** — e.g. Couponing (60€/year), Club card (40€/year), Loyalty card (80€/year), RAG Chatbot (349€/year, discounted from a 540€/year list price as an observed "launch offer").
- **"Installed by default"** — a set of extensions every app ships with already active, not opt-in (see §4).
- **"LAB"** — a badge (not a filterable category with contents at the time of writing; the Lab category page showed "Lab (0)") marking experimental/beta features, seen on Buy Me a Coffee and Donately within Monetization.
- **"In test until [date]"** — a time-boxed free-trial state, observed on RAG Chatbot in ReBook (trial running until 08/27/2026).

## 2. How Integration Actually Works

Two distinct mechanisms were confirmed, and a given extension can use either or both:

1. **Section-based integration.** Most extensions — all CMS types, custom feeds, social embeds — install as a new entry in Structure's "+ Add a section" catalog (or are already there; see `4-structure-backoffice.md` §4). Nothing about their back-office presence changes: they show up, get configured, and get placed in the Menu exactly like any native section.
2. **Sidebar-level integration, backed by the same section mechanism.** More complex extensions get their **own dedicated top-level entry in the left sidebar**, separate from `My App`. RAG Chatbot is the clearest example: it has its own sidebar icon, and clicking it does *not* open a settings form directly — it opens a page saying *"You don't have any RAG Chatbot section — Start by adding one!"* with an **Add a section** button. This confirms the sidebar entry is a **dedicated management console layered on top of the same section-creation mechanism** documented in `4-structure-backoffice.md`, not a parallel system. The extension elevates itself to first-class sidebar status for discoverability and centralized management, but structurally it still lives inside Structure once instantiated.

**Installed vs. available** is tracked centrally at `Extensions Store > Management` ("Your extensions"), which lists every extension currently active in the app with its status: an `Enabled`/toggle switch for some (e.g. **Advanced Settings** — see the critical cross-reference in §5), a price + trial badge for paid ones (RAG Chatbot), or an `Installed by default` label for the baseline set every app ships with (see §4). A trash-can icon next to each row allows removal.

**Note on this research**: I did not click Install/Add a section/Create a new key set on anything during this exploration, since those are state-changing actions on a live app. All findings below come from extension detail pages, the Management screen's existing state, and GoodBarber's help docs — not from performing installs myself.

## 3. Deep Dive: The AI Collection

GoodBarber curates a dedicated **"AI, when you really need it"** banner section in the store, and a matching **"Enhance your app with AI and automations"** category in the help center — confirming AI tooling is treated as a first-class, marketed pillar of the platform, not a buried feature. Four extensions stood out as most directly relevant to Mário's AI-integration case study.

### 3.1 AI Extension Builder — *the single most relevant extension to this project*

**What it is**: *"Describe a feature, AI creates it in your app."* Built by GoodBarber, free, available on all plans. This is GoodBarber's own existing implementation of exactly the concept this project is researching: building app features from a natural-language description.

**How it works**: a two-pane chat interface (`CHAT` | `PREVIEW`) inside the back office. You type a description (e.g., *"Build a caring daily mood tracker. Ask 'How do you feel today?' and let the user pick one of five mood emojis... Save each entry in-component for the current session and display the last 7 entries as a horizontal chart of colored dots..."*), an AI agent generates working code, and the result renders live in the preview pane next to the chat. A `</>` toggle reveals the generated code directly. Iteration happens conversationally — *"Display last 30 check-ins for subscribers only, 7 days for non-subscribers"* was shown as a realistic follow-up turn that regenerates the same component. GoodBarber's own framing: *"Creation doesn't stop with the first result. You dialogue with the agent to adjust the rendering... The process resembles a conversation with a developer — except that he responds within seconds. If you understand the code, you can also manually edit the generated files from your back office. Both approaches can be combined."*

**What it can actually build**: per GoodBarber's own explanation, *"the agent doesn't work in a limited sandbox — it uses GoodBarber's public APIs (the same ones developers use to create Custom Code sections)."* Concretely, this means an AI-generated section can: store data locally on-device (offline-capable), associate data per authenticated user, adapt content by subscription status (free vs. premium — a direct link to the Memberships extension in §3.4 below), query geolocation and open native map apps, trigger native sharing and system alerts, detect network connectivity, and automatically inherit the app's global App Style (typography, colors, spacing — a direct link to `5-appstyle-edition-json.md`). A **Prompt Library** (categorized: Utilities, Content, Games, Social) offers ready-made starting prompts — countdown timer, currency converter, todo list, calculator, breathing coach, mood tracker, quiz game, habit tracker.

**When to use it**: for bespoke, small-to-medium interactive widgets that don't map to any existing section type (calculators, converters, games, mood/habit trackers) — i.e., exactly the gap left by the ~120 pre-built section types. Not a fit for large, data-heavy content systems (use a CMS section instead) — it is explicitly positioned as a Custom Code generator, not a content management replacement.

**Case-study relevance**: this is a live, working precedent for the Description→Implementation Agent architecture discussed in `1-structure.md`. It resolves the ambiguity in a single tool: conversational input → live-previewed, iteratively-refined, directly-editable code output, scoped to GoodBarber's own public API surface rather than an unconstrained sandbox.

### 3.2 MCP — connecting external AI assistants directly to the app

**What it is**: *"Connect your content app to Claude, ChatGPT, or any AI assistant through MCP — and manage your content by conversation."* Built by GoodBarber, free, **installed by default** on every app (confirmed via the Management screen — ReBook already has it active without any explicit install step).

**What it does, precisely**: MCP (Model Context Protocol) is described as *"an open standard that lets an AI assistant act inside another tool."* GoodBarber's implementation *"exposes your app's operations as actions an MCP-aware assistant can call."* You connect a client (Claude, ChatGPT, Cursor, or any MCP client) to a server URL, authenticate once via OAuth, and issue instructions in plain language instead of clicking through the back office manually.

**Concrete capabilities**, per the help documentation (four use cases):
- **Content management & data exports** — draft, edit, or categorize articles and media through conversation; retrieve, back up, or export CMS content.
- **Targeted push notifications** — write copy, target recipients by criteria, schedule/send notifications, all through the assistant.
- **App analytics & insights** — ask the assistant to summarize traffic, identify top content, analyze audience engagement.
- **Automated workflows** — connect the app to external tools or build automated editorial calendars.

**Permission model**: configured at `Settings > MCP Server & Public APIs`. You create a named API key set, choose which **modules** the AI assistant can access (`User`, `Stats`, `Cms` were the three observed), and set a **permission level per module** (`Read only` or `Read & write`). The server URL follows the pattern `https://mcp.goodbarber.dev/{appId}/mcp/sse` (an SSE transport endpoint) — ReBook's is `https://mcp.goodbarber.dev/4603405/mcp/sse`, using the same numeric app ID observed elsewhere in this project's JSON research. GoodBarber publishes the underlying tool/skill definitions publicly ("View skills on GitHub").

**Important scope distinction from AI Extension Builder**: MCP is a **content-operations** interface (CRUD on existing sections' items, notifications, analytics) — every example given is about managing content *within* sections that already exist. Nothing in the documentation suggests MCP can create new sections or alter Structure/App Style itself; that remains AI Extension Builder's and the manual back office's domain. Read as a pair: MCP handles the ongoing *operation* of a built app via agentic access; AI Extension Builder handles *building* new pieces of it.

**Case-study relevance**: this is direct, load-bearing evidence that GoodBarber already treats "AI assistants driving the back office" as supported infrastructure, with a real permission/scoping model (module × read/write) — a concrete reference point for designing the Implementation Agent's own access boundaries.

### 3.3 RAG Chatbot — paid, app-facing (not back-office-facing) AI

**What it is**: *"AI that answers using your content."* Built by GoodBarber. Unlike AI Extension Builder and MCP (both free, back-office tools), RAG Chatbot is a **paid, end-user-facing** feature: 349€/year (launch-discounted from 540€/year), currently in ReBook on a free trial until 08/27/2026.

**What it does**: adds a conversational assistant *inside the published app itself* (not the back office) that answers app users' questions grounded in the app's own content via retrieval-augmented generation — *"Each response draws on your content to ensure accuracy, relevance, and consistency with your app's theme."*

**Integration mechanics**: confirmed to follow the sidebar-console-over-section-mechanism pattern from §2 — its dedicated sidebar entry currently shows an empty state ("You don't have any RAG Chatbot section") with an "Add a section" call to action, meaning enabling it for real requires explicitly adding a RAG Chatbot section, distinct from merely having the extension "installed" (billing-wise) in Management.

**When to use it**: apps with a non-trivial content library (docs, articles, FAQs, a knowledge base) where users would otherwise search or browse manually — directly applicable to ReBook's own article/podcast library.

### 3.4 Memberships — the monetization backbone

**What it is**: *"Make money in your app with Memberships."* Free to use, but plan-gated ("Available from the Premium offer, free with the Pro offer" — an example of the plan-gated pricing tier from §1).

**What it does**: native, auto-renewing in-app subscriptions (iOS/Android IAP-based), giving users permanent access to gated content as long as their membership stays active, cancellable anytime. GoodBarber's own note: *"Memberships represents nearly 50% of the revenue generated by native apps,"* and — notably — *"GoodBarber does not charge any commission on the revenue generated by your sales"* (only the platform store's own cut applies).

**Why it's a standout**: it's the load-bearing piece that other extensions plug into — AI Extension Builder explicitly lists "adapt content according to subscription status (free or premium)" as a capability of AI-generated sections, and MCP's permission model presumably interacts with the same user/subscription state. Understanding Memberships is a prerequisite for understanding several other extensions' more advanced capabilities.

### 3.5 Advanced Settings — the extension behind `{EDITION}`

**What it is**: found in the Tools for developers category as *"Advanced edition: Activate the advanced features that give you access to hidden settings."* Free.

**Why this matters here specifically**: cross-referencing the Management screen confirms this is the **exact same feature documented as `{EDITION}` in `5-appstyle-edition-json.md`** — the raw-JSON configuration inspector present on nearly every back-office screen. It appears in Management as **"Advanced Settings,"** currently `Enabled` via a toggle switch (not a delete-only entry like most extensions — it can be turned off without being removed). This is a concrete, confirmed answer to a question left open in the previous report: the JSON editor is not a hidden built-in feature everyone has by default, it is itself an installable/toggleable extension, gating access to the platform's raw configuration layer.

## 4. Installed-by-Default Baseline

Beyond the AI collection, the Management screen shows every ReBook app ships with a further baseline of pre-installed (not separately chosen) extensions: **Pexels** (stock photo library), **Google Analytics**, **Google Tag Manager**, **Meta Title & Meta Description** (SEO), **Genius Palette** (the AI-assisted color-theme generator referenced as "Magic Palette" in App Style's own documentation — apparently the extension's product name differs slightly from the in-context UI label), **Statistics & Dashboard**, **Custom font**, **LottieFiles** (animation assets), **Countly** (analytics), **Offline** (offline-mode support), and **Custom Domain**. None of these were separately "installed" by anyone at ReBook — they represent GoodBarber's default extension baseline for every new app.

## 5. Catalog by Category (Selected)

| Category | Notable entries |
|---|---|
| Content (= Structure's native sections) | CMS Articles/Videos/Podcasts/Photos/Agenda/Map/Contact/About, Bookmark — all free |
| Memberships & Login (8) | Memberships, Authentication, Chat, Community, User groups, Zapier, Make, App Walkthrough |
| Monetization (14) | Memberships, External advertising networks, Google AdMob/Ad Manager, Internal ad server, Buy Me a Coffee (LAB), Donately (LAB), Meta Audience Network Native Ads, Google Ads, Couponing (60€/yr), Club card (40€/yr), Loyalty card (80€/yr) |
| Tools for developers (14) | Custom Sound/Map/Video/Photo/Events/Article feed (all free), Zapier, Make, API for Content applications, **Advanced edition**, Custom Code menu / navigation mode / section / widget (the full "build from scratch" family) |
| AI (cross-category) | AI Extension Builder, MCP, RAG Chatbot, AI Assistant ("powered by OpenAI," content-creation helper), Genius Palette |
| Design assets (cross-category, "Details that count for exceptional design") | Google Material Icons, Google Fonts, Custom font, Pexels, Advanced edition |

## 6. Relevance to the AI-Integration Case Study

This report surfaces the most direct evidence yet for the case study's core question — GoodBarber has already built two complementary halves of an AI-driven app-building pipeline:

1. **AI Extension Builder is a working Implementation Agent, scoped to Custom Code.** It already does conversational, iteratively-refined, live-previewed feature generation against GoodBarber's public APIs — a smaller-scope but functioning proof of the exact "describe it, the platform builds it" loop this project is designing for the *whole app*, not just individual widgets.
2. **MCP is a working precedent for agent-driven back-office operation**, complete with a real per-module, per-permission-level access model (`User`/`Stats`/`Cms` × `Read only`/`Read & write`) — directly useful as a reference for scoping what an Implementation Agent should and shouldn't be allowed to touch.
3. **The two are scope-separated by design**: building (AI Extension Builder) vs. operating (MCP) are different tools with different permission surfaces, suggesting that any unified Description→Implementation Agent architecture for this project should likely preserve a similar split rather than collapsing "create the app" and "run the app" into one undifferentiated capability.
4. **The extension/plan/pricing layer is a real constraint an agent must reason about** — not everything is free or instantly available; some capabilities require a specific subscription tier (Memberships), a paid add-on (RAG Chatbot), or are still labeled experimental (LAB). An agent recommending or invoking extensions on a user's behalf needs to surface these constraints rather than assume uniform availability.

---

*Sources: direct inspection of the ReBook back office at `rebook.goodbarber.app/manage/addons/list/`, `.../addons/management/`, `.../addons/category/{monetization,developer-tools,memberships-login,lab}/`, `.../addons/detail/{ai_extension_builder,inapppurchase,rag,mcp_classic}/`, and `.../settings/publicapi/` (2026-08-11); GoodBarber in-product help article "Connect your app to AI assistants with GoodBarber MCP" (help ID 124/432, category "Enhance your app with AI and automations," accessed via the back office's built-in help panel).*
