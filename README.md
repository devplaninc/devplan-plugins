<p align="center"><img src="assets/logo.png" width="96" alt="Devplan" /></p>

# Devplan plugin for Claude, ChatGPT and Codex

Daily product and engineering dashboards, built from your team's tools. Connect Devplan to run them all on a shared knowledge graph.

## Install

Pick the app you use. Once it's installed, say **"Set up Devplan"** in a new chat.

### Claude (web and desktop app)

1. Go to **Customize > Plugins > Add > Add marketplace** and enter `devplaninc/devplan-plugins`.
2. Find **Devplan** and select **Add**.
3. Open the plugin's **Connectors** tab and connect **Devplan** (optional, free).

Installed on Claude, the plugin also shows up in Cowork and Claude Code.

### Claude Code

```
/plugin marketplace add devplaninc/devplan-plugins
/plugin install devplan@devplan
```

Then run `/mcp`, select **devplan**, and sign in (optional, free).

### ChatGPT and Codex desktop app

1. Add the Devplan marketplace once, from a terminal:
   ```
   codex plugin marketplace add devplaninc/devplan-plugins
   ```
2. Restart the app, open the **Plugins** directory (in Work mode or Codex), and choose the **Devplan** marketplace.
3. Open **Devplan** and select the **+** button to install it.
4. Connect Devplan when prompted (optional, free).

Installed plugins work in both ChatGPT (Chat or Work) and Codex. In ChatGPT, @-mention **Devplan** or pick it from **+ > More**. In a Codex task, use **Sources > Use plugins**.

### Codex CLI

```
codex plugin marketplace add devplaninc/devplan-plugins
codex
```

Then type `/plugins`, open the **Devplan** marketplace tab, and install **Devplan**. Start a new session before using it. Plugins aren't available in the Codex IDE extension.

### For workspace admins

- **ChatGPT Business, Enterprise and Edu:** import `devplaninc/devplan-plugins` as a marketplace under **Workspace settings > Plugins > Marketplaces**. It syncs daily; use **Sync now** to pull changes. Set Devplan to **Installed** to install it for everyone.
- **Claude Team and Enterprise:** add the marketplace in your organization's plugin settings to make Devplan available to everyone.

### Updating

- Claude: the marketplace syncs from GitHub; reinstall Devplan if a new version doesn't appear.
- Claude Code: `/plugin marketplace update devplan`
- ChatGPT, Codex app and CLI: `codex plugin marketplace upgrade`, then restart the app.

## Getting started

Setup takes about ten minutes. Start a new chat and say:

> **Set up Devplan**

Setup walks you through six steps, one at a time:

1. **Choose how Devplan runs.** On your own connections (free, nothing to sign in to), or on Devplan for your whole team (connect your sources once, $100 in free credits).
2. **Check your tools.** Setup shows what's connected and what each dashboard needs. Connect at least one of GitHub, Linear, Jira, or Slack to get going; support and call tools (Zendesk, Intercom, Gong, Granola) add customer demand.
3. **Capture your company context.** Setup drafts your company description, customers, competitors, goals, and product overview from your website and tools. Approve it in one click or edit any part.
4. **Save it.** Sign in to Devplan (free) so it follows you everywhere and your teammates start with it filled in, or keep it just for you.
5. **Build your dashboards.** Every dashboard your tools support, built in a few minutes.
6. **Get them daily.** Optionally schedule an email every weekday morning with the top three things and links to every dashboard.

### Try these next

| Say | What you get |
|---|---|
| "Run my Daily Radar" | What shipped, what's moving, what's stuck, and who owns it |
| "What are customers asking for?" | Your Demand Report: recurring asks, blockers, and demand nobody is building |
| "Write a spec for <a feature>" | A few questions, then a spec with a technical plan and estimate |
| "How fast are we shipping?" | Cycle time, review waits, and throughput |
| "What slipped this week?" | Commitments that went quiet, slipped, or got blocked |
| "What shipped today?" | A plain-language changelog |
| "What should we build next?" | Project ideas backed by evidence |
| "Who should we tell about what shipped?" | Releases matched to customers, with drafts |

You don't need to name a skill. Ask product questions as you normally would ("why are we building X?", "what should I know before changing billing?") and the answer starts from your company context and tools.

### Tips

- **Work in one place.** On Claude.ai, run Devplan chats inside a Devplan Project if you didn't sign in, so your context sticks.
- **Change the scope in plain words:** "Daily Radar for the last week", "Demand Report for Acme only".
- **Everything is read-only.** Nothing is posted, sent, or changed unless you ask after seeing the result.
- **Each report says which mode it ran in.** On your own connections, it ends with what the run took and what the Devplan graph would add.
- **Update your context any time** by saying "Set up Devplan" again.

## Skills

| Skill | Refresh | On your own connections | On the Devplan graph |
|---|---|---|---|
| `devplan-setup` | Once | Guided 6-step setup: choose Devplan or your own connections, check tools, capture company context, save it (Devplan or locally), build every dashboard your tools support, daily email | Same |
| `devplan-product-context` | Always on | Starts every answer from your saved company context and connected tools | Plus the graph |
| `daily-radar` | Daily | What shipped, moved and stuck, from code, tracker and Slack | Every signal attributed to people and projects |
| `demand-report` | Daily | Recurring demand, uncaptured asks and blockers from support, calls, Slack, tracker | Deduplicated and linked to projects and code |
| `eng-analytics` | Daily | Cycle time, reviews, throughput, WIP from GitHub and tracker | Every PR joined to project and team |
| `stale-commitment-watch` | Daily | Slipped, quiet and blocked commitments from tracker, Slack, meetings | Commitments tracked to the work across every tool |
| `suggested-projects` | Daily | Project ideas from tracker demand, incidents and roadmap docs | Full evidence, scope and owners from the graph |
| `changelog` | Daily | Plain-language changelog from merged PRs | Grouped by feature, availability verified |
| `customer-release-brief` | Daily | Recent releases matched to customers by search, with drafts | Every customer who asked, availability checked |
| `spec` | On demand | Discovery questions, product and technical plan, estimate | Full graph, estimates from real velocity, tracked automatically |

Every report ends with what this run cost (tool calls, tools, items read) and why the Devplan graph is better: faster and cheaper, always up to date, shared across the team, fits in context, and matched across tools.

## Repo layout

```
.claude-plugin/marketplace.json      Claude marketplace (Codex also reads this)
.agents/plugins/marketplace.json     Codex marketplace with install and auth policy
plugins/devplan/
  .claude-plugin/plugin.json         Claude manifest
  plugin.json                        Portable manifest + OpenAI extension (Codex/ChatGPT)
  .mcp.json                          Devplan MCP, Claude format
  mcp.json                           Devplan MCP, portable format with OAuth (DCR)
  skills/                            All skills, free and premium
docs/
  ENTITLEMENT_SPEC.md                Server-side gating and metering contract
  UPSELL_COPY.md                     Default upsell strings served by the MCP
  INSTALL_SCREEN.md                  Onboarding final step
```

## Maintainer notes

- Keep `.mcp.json` and `mcp.json` in sync. Claude reads the first, Codex the second.
- Keep `.claude-plugin/plugin.json` and `plugin.json` versions in sync. Bump both on every release.
- Skills call `get_entitlement` when the Devplan MCP has it, and use its mode and upsell copy. Until it ships, they fall back to checking whether Devplan has data, and to the built-in Why Devplan footer. Nothing needs to change in the plugin when the server tools go live.
- No lifecycle hooks: hooks make the plugin ineligible for OpenAI's public directory.
