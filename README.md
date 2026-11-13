<p align="center"><img src="assets/logo.png" width="96" alt="Devplan" /></p>

# Devplan plugin for Claude, ChatGPT and Codex

Your Devplan workspace inside the AI you already use: six dashboards refreshed every weekday, cycle plans sized from how your team actually ships, specs tracked in Devplan automatically, and product answers grounded in your code, tickets, calls, and Slack.

The plugin needs a Devplan account. Setup walks you through creating one and connecting your sources.

## Install

Pick the app you use. Once it's installed, say **"Set up Devplan"** in a new chat.

### Claude (web and desktop app)

1. Go to **Customize > Plugins > Add > Add marketplace** and enter `devplaninc/devplan-plugins`.
2. Find **Devplan** and select **Add**.
3. Say **"Set up Devplan"** in a new chat. Setup connects Devplan for you.

Installed on Claude, the plugin also shows up in Cowork and Claude Code.

### Claude Code

```
/plugin marketplace add devplaninc/devplan-plugins
/plugin install devplan@devplan
```

Then say **"Set up Devplan"**, or run `/mcp`, select **devplan**, and sign in.

### ChatGPT and Codex desktop app

1. Open **Plugins**, choose to add a marketplace, and enter `devplaninc/devplan-plugins`. (Or from a terminal: `codex plugin marketplace add devplaninc/devplan-plugins`.)
2. Open the **Plugins** directory (in Work mode or Codex), and choose the **Devplan** marketplace.
3. Open **Devplan** and select the **+** button to install it.
4. Say **"Set up Devplan"**. Sign in to Devplan when asked.

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

Start a new chat and say:

> **Set up Devplan**

Setup takes about ten minutes and goes one step at a time:

1. **Connect Devplan.** If you don't have an account yet, setup explains what happens in Devplan first: create a workspace, describe your company, connect a code repository and the rest of your team's tools, and let Devplan build your knowledge graph. You don't need to wait for the graph to finish.
2. **Check your workspace.** See what Devplan can read and which dashboards are ready.
3. **Confirm your company context.** Description, customers, competitors, goals, and product overview, shared with your whole workspace. Then tell your Daily Radar what to focus on.
4. **Build your dashboards and schedule updates.** All six, built in a few minutes and refreshed every weekday morning, with a short summary emailed to you.
5. **A quick tour.** What you can ask, how Slack and decision memory work, and how to bring your team in.

### Try these next

| Say | What you get |
|---|---|
| "Run my Daily Radar" | What shipped, what's moving, what's stuck, and what needs you |
| "How are our projects going?" | Execution Monitoring: every planned and inferred project, with activity, progress, and risks |
| "What are customers asking for?" | Your Demand Report: demand themes, market moves, and the projects they suggest |
| "Plan the next 6 weeks" | Cycle Planning: a few strategic directions, then a plan sized from your team's real pace |
| "Write a spec for <a feature>" | A few questions, then a spec with a technical plan and estimate, tracked in Devplan |
| "What slipped this week?" | Commitments that went quiet, slipped, or got blocked |
| "When did we ship <feature>?" | The searchable Changelog |
| "How fast are we shipping?" | Cycle time, throughput, work in progress, and planned work |

You don't need to name a skill. Ask product questions as you normally would ("why are we building X?", "what did we decide about pricing?") and the answer starts from your Devplan workspace, with sources.

### Tips

- **Act from a dashboard.** "Write spec", "Update spec" and "New project" buttons copy a ready message. Paste it into a chat to start.
- **Change the scope in plain words:** "Daily Radar for the last week", "Demand Report for Acme only".
- **Dashboards are read-only.** Nothing is posted, sent, or changed unless you ask. Specs are the exception: every spec is tracked as a Devplan project.
- **Update your context, dashboards, or schedule** by saying "Set up Devplan" again.

## Skills

| Skill | Refresh | What it does |
|---|---|---|
| `devplan-setup` | Once | Guided setup: connect or create Devplan, check the workspace, confirm company context, build every dashboard, schedule weekday refreshes |
| `devplan-product-context` | Always on | Starts every product answer from your Devplan workspace and what Claude knows about you |
| `daily-radar` | Weekdays | Your personal briefing: what shipped, what's moving, what's stuck, and what needs you |
| `execution-monitoring` | Weekdays | Planned and inferred projects with activity, progress, risks, and drift; start a new project |
| `demand-report` | Weekdays | Customer demand themes with competitor and market research, and suggested projects that start a spec |
| `stale-commitments` | Weekdays | Commitments that slipped, went quiet, or got blocked, and who needs to decide |
| `changelog` | Weekdays | Searchable 30-day changelog by product area, with delivery state |
| `eng-analytics` | Weekdays | Cycle time, throughput, work in progress, review load, and planned work |
| `cycle-planning` | On demand | Asks timeframe and team size, offers strategic directions, and plans what fits from observed pace, priorities, and work in flight |
| `spec` | On demand | Discovery questions, product and technical plan, estimate; tracked in Devplan automatically |

## Repo layout

```
.claude-plugin/marketplace.json      Claude marketplace (Codex also reads this)
.agents/plugins/marketplace.json     Codex marketplace with install and auth policy
plugins/devplan/
  .claude-plugin/plugin.json         Claude manifest
  plugin.json                        Portable manifest + OpenAI extension (Codex/ChatGPT)
  .mcp.json                          Devplan MCP, Claude format
  mcp.json                           Devplan MCP, portable format with OAuth (DCR)
  skills/                            The skills
shared/
  dashboard-template.html            The dashboard design every dashboard skill uses
  blocks/                            Text shared across skills
scripts/sync.py                      Copies shared blocks and the template into the skills
docs/
  SERVER_SPEC.md                     Devplan MCP tools the plugin uses or needs
  INSTALL_SCREEN.md                  Onboarding final step
```

## Maintainer notes

- Edit shared text in `shared/`, then run `python3 scripts/sync.py`. Don't edit the copies inside skills between `<!-- shared:... -->` markers or in `references/dashboard-template.md`.
- Keep `.mcp.json` and `mcp.json` in sync. Claude reads the first, Codex the second.
- Keep `.claude-plugin/plugin.json` and `plugin.json` versions in sync. Bump both on every release.
- Skills use new server tools (`get_workspace_context`, `save_workspace_context`, `create_project`) when they exist and fall back to existing tools until then. Nothing needs to change in the plugin when they ship. See `docs/SERVER_SPEC.md`.
- No lifecycle hooks: hooks make the plugin ineligible for OpenAI's public directory.
- The earlier free version, which ran on the user's own connectors, is in the git history before v0.2.0.
