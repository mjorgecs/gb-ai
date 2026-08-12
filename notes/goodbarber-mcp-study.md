# GoodBarber MCP Server — Study

*Prepared: August 10, 2026*

## What It Is

GoodBarber MCP is an official server implementing the **Model Context Protocol** (open standard, donated to the Linux Foundation in late 2025). It lets any MCP-compatible AI assistant (Claude, ChatGPT, Cursor, Claude Code, n8n, etc.) operate a **live** GoodBarber app — content, shop, orders, members, push — through natural-language conversation, instead of clicking through the back office.

**Important boundary:** MCP covers *operations*, not *design*. It cannot change layout, sections, or app structure — that stays in the no-code builder. GoodBarber's own distinction: "the AI Extension Builder helps you create the app; MCP lets an assistant operate it after it's built."

## Capabilities

| Area | What the assistant can do |
|---|---|
| **Shop** | Browse/create/edit products, variants, prices, stock; view & update orders and shipping status; view customers; send push notifications |
| **CMS** | Create/edit articles, events, photo galleries, videos |
| **Community / Membership** | View active subscribers, manage subscriptions, send push notifications |
| **Marketing** | Draft, target, and schedule push campaigns; create promo codes |
| **Analytics** | Read app stats — page views, sessions, downloads, device/platform breakdown |
| **Multi-app** | Agencies can run a whole portfolio of client apps from one assistant (via per-app endpoint) |

The exact tool set exposed depends on which services your app has enabled (Shop, CMS, Community, Membership). Every mutating action (create/update/delete/send) requires explicit user confirmation before it executes.

### Skills layer (on top of MCP)

GoodBarber also publishes an open-source **Skills** library on GitHub ([goodbarber/goodbarber-skills](https://github.com/goodbarber/goodbarber-skills), Unlicense/public domain) — 41 pre-built `.md` instruction sets that orchestrate multi-step MCP tool calls into single workflows. (GoodBarber's marketing pages round this up to "44 skills"; the repo itself currently lists 41: 17 eCommerce + 4 Community + 9 Membership + 11 CMS.)

Examples: `best-sellers`, `stock-check`, `catalog-audit`, `customer-insights`, `rfm-segmentation`, `promo-campaign`, `subscription-audit`, `weekly-digest`, `article-publish`, `editorial-calendar`, `content-audit`, `push-broadcast`. Design principles per the repo: pagination-aware, fuzzy name matching, workflow-chaining (each skill suggests related next steps), no destructive action without confirmation, structured report output.

## How It Can Be Used

1. **Direct conversation** — ask the connected assistant in plain language ("Increase the price of Corsican honey by €5 and send a push to announce it"); the assistant calls the relevant MCP tools and asks for confirmation before acting.
2. **Skills-driven workflows** — install the GitHub skills matching your app type so recurring tasks (weekly digest, stock audit, editorial calendar) run as a single structured request rather than several ad-hoc prompts.
3. **Automation platforms** — GoodBarber has a published guide on chaining MCP into **n8n** for no-code multi-step automations (e.g. triggered content publishing, scheduled reports).
4. **Agency / multi-app management** — a single assistant session can be pointed at different apps via `https://mcp.goodbarber.dev/<app_id>/mcp/sse`, letting one person operate several client apps.

## How to Set It Up

**Requirements:** a GoodBarber account with at least one app, and an MCP-capable AI client (Claude.ai, Claude Desktop/Cowork, Claude Code, ChatGPT, Cursor, VS Code, Windsurf, etc.).

**Steps (Claude Desktop/Cowork):**

1. In Claude, go to **Settings → Connectors**.
2. Click **Add custom connector**.
3. Paste the MCP server URL: `https://mcp.goodbarber.dev/mcp/sse` (single app) — or `https://mcp.goodbarber.dev/<app_id>/mcp/sse` for a specific app if managing several.
4. Leave OAuth Client ID/Secret fields empty — GoodBarber uses Dynamic Client Registration.
5. Click **Add**. This opens GoodBarber's authorization page.
6. On that page, paste your **GoodBarber Public API key**, generated from your app's back office under **Public API / MCP server**, and authorize.
7. Done — GoodBarber tools appear in the conversation, scoped to that one app.

**Claude Code (CLI):**
```
claude mcp add goodbarber --transport sse https://mcp.goodbarber.dev/mcp/sse
```
The first tool call triggers the same browser-based OAuth step.

**Cursor / VS Code / Windsurf:** add to the client's MCP config file:
```json
{ "mcpServers": { "goodbarber": { "url": "https://mcp.goodbarber.dev/mcp/sse" } } }
```

**Optional — install the Skills:**
```
git clone https://github.com/goodbarber/goodbarber-skills.git
cp -r goodbarber-skills/skills/<app-type>/* ~/.claude/skills/
```
(`<app-type>` = `ecommerce`, `community`, `membership`, and/or `cms` — install multiple if the app combines types; watch for name collisions like `weekly-digest` across folders.)

**Caution — do not open the `/authorize` URL manually.** It must be initiated by the MCP client, which supplies required OAuth parameters (`redirect_uri`, `client_id`, `state`, `code_challenge`); opening it directly will fail.

## Security & Scope

- OAuth 2.1 with PKCE; the GoodBarber API key itself is never shared with the AI client.
- Each connection is scoped to a single app — the assistant cannot reach any other GoodBarber account.
- Revocable anytime, either from the GoodBarber account or by removing the connector.
- Included in all GoodBarber plans — no separate MCP fee.

## Relevance to This Project

This is GoodBarber's live answer to "AI agents managing an app by description" — but note it operates an **already-built** app (content/commerce/ops), not app creation/design. The separate **AI Extension Builder** (generates new sections from a prompt) is the closer analog to natural-language *app construction*, and would be worth a follow-up study alongside this one.

---

**Sources:**
- [GoodBarber MCP — product page](https://www.goodbarber.com/mcp/)
- [GoodBarber MCP — the complete guide](https://www.goodbarber.com/mcp-complete-guide/)
- [Connect your GoodBarber app to Claude](https://www.goodbarber.com/connect-claude-app/)
- [goodbarber/goodbarber-skills (GitHub)](https://github.com/goodbarber/goodbarber-skills)
