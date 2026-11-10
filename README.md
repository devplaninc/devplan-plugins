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
