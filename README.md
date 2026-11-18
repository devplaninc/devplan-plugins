<p align="center"><img src="assets/logo.png" width="96" alt="Devplan" /></p>

# Devplan plugin for Claude, ChatGPT and Codex

Your Devplan workspace inside the AI you already use: four dashboards built from your team's real work, cycle plans sized from how your team actually ships, specs tracked in Devplan, and product answers grounded in your code, tickets, calls, and Slack.

**Before you install:** the plugin needs a Devplan account with a **code repository connected**. That's required; tickets, Slack, docs, calls, and support make it better. Setup walks you through creating an account if you don't have one.

**Pricing:** Devplan runs on credit packs, starting at $50. Purchased credits never expire. New workspaces get $100 in free credits, valid for 3 months, with no credit card. [See pricing](https://www.devplan.com/pricing/)

## Install the plugin (recommended)

The plugin gives you Devplan's tools plus ten skills: guided setup, the dashboards, specs, cycle planning, and product answers. Pick the app you use. Once it's installed, say **"Set up Devplan"** in a new chat.

### Claude (web and desktop app)

1. Open **Plugins** in the sidebar, then **Add > Add marketplace > Add from a repository**.
2. Enter `https://github.com/devplaninc/devplan-plugins` and select **Sync**.
3. Open **Devplan** and select **Add**.
4. Say **"Set up Devplan"** in a new chat. When setup asks you to connect, open **Plugins > Devplan > Connect**. Claude shows a connector form: keep the defaults, click **Add**, then sign in to Devplan.

Installed on Claude, the plugin also shows up in Cowork and Claude Code on the same account.

### Claude Code

From a terminal:

```
claude plugin install devplan --marketplace https://github.com/devplaninc/devplan-plugins
```

Or inside Claude Code:

```
/plugin install devplan --marketplace https://github.com/devplaninc/devplan-plugins
```

Then say **"Set up Devplan"** and open the sign-in link it shows. If no link appears, run `/mcp`, choose **plugin:devplan:devplan**, and sign in.

### Codex CLI

```
codex plugin marketplace add https://github.com/devplaninc/devplan-plugins
codex plugin add devplan@devplan
codex mcp add devplan --url https://app.devplan.com/api/v1/mcp
```

The last command opens Devplan's sign-in in your browser. It's a one-time step until Devplan is listed in OpenAI's plugin directory. Then start a new Codex session and say **"Set up Devplan"**. Plugins aren't available in the Codex IDE extension.

### ChatGPT and the Codex app

1. Open **Plugins**, choose to add a marketplace, and enter `https://github.com/devplaninc/devplan-plugins`.
2. Open the **Devplan** marketplace, then **Devplan**, and select **+** to install it.
3. Say **"Set up Devplan"** and sign in when asked.

In ChatGPT, @-mention **Devplan** or pick it from **+ > More**. In a Codex task, use **Sources > Use plugins**. If you don't see an option to add a marketplace on your plan, use **Connect Devplan directly** below.

### For workspace admins

- **Claude Team and Enterprise:** add the marketplace in your organization's plugin settings to make Devplan available to everyone.
- **ChatGPT Business, Enterprise and Edu:** import `https://github.com/devplaninc/devplan-plugins` under **Workspace settings > Plugins > Marketplaces**. It syncs daily; use **Sync now** to pull changes. Set Devplan to **Installed** to install it for everyone.

### Updating

- **Claude:** the marketplace syncs from GitHub. Reinstall Devplan if a new version doesn't appear.
- **Claude Code:** `claude plugin marketplace update devplan`
- **ChatGPT, Codex app and CLI:** `codex plugin marketplace upgrade`, then restart the app.

### Uninstalling

- **Claude:** **Plugins > Devplan**, then remove it.
- **Claude Code:** `claude plugin uninstall devplan@devplan`
- **Codex CLI and app:** remove Devplan from **Plugins** (`/plugins` in the CLI). If you ran `codex mcp add devplan`, also run `codex mcp remove devplan`.

Uninstalling doesn't delete your Devplan workspace or anything saved in it.

## Or connect Devplan directly

If you can't install plugins, add Devplan as a server instead. You get Devplan's tools, so your assistant can answer from your workspace, but not the skills: no guided setup, dashboards, spec flow, or cycle planning.

- **Server URL:** `https://app.devplan.com/api/v1/mcp` (sign in with your Devplan account)
- **Claude:** add a custom connector with that URL.
- **Claude Code:** `claude mcp add --transport http devplan https://app.devplan.com/api/v1/mcp`
- **Codex:** `codex mcp add devplan --url https://app.devplan.com/api/v1/mcp`
- **ChatGPT:** **Plugins > Add > Add custom MCP server**, with that URL.

If you later install the plugin, remove this server so you don't have two Devplan connections.

## Getting started

Start a new chat and say:

> **Set up Devplan**

Setup takes about ten minutes and goes one step at a time:

1. **Connect Devplan.** If you don't have an account yet, setup explains what happens in Devplan first: create a workspace, describe your company, connect a code repository and the rest of your team's tools, and let Devplan build your knowledge graph. You don't need to wait for the graph to finish.
2. **Check your workspace.** See what Devplan can read and which dashboards are ready.
3. **Confirm your company context.** Description, customers, competitors, goals, and product overview. Then tell your Daily Radar what to focus on.
4. **Build your dashboards.** All four, built in a few minutes. In Claude, ChatGPT, and the Codex app, setup also refreshes them at 7:47 AM and 12:47 PM every weekday and sends a short summary only when something changed.
5. **A quick tour.** Product and technical questions to try first, how Slack and decision memory work, and how to bring your team in.

Claude may ask before each Devplan tool it uses. Devplan's read tools only read your workspace, so you can choose **Always allow** for them.

### Try these next

| Say | What you get |
|---|---|
| "Run my Daily Radar" | What shipped, what's moving, what's stuck, and what needs you |
| "How are our projects going?" | Execution Monitoring: active projects from Devplan, Linear, and Jira, what slipped, inferred work, and the changelog |
| "What are customers asking for?" | Your Demand Report: themes and the projects that answer them, isolated asks, adoption blockers, customer promises, and two weeks of market moves |
| "Plan the next 6 weeks" | Cycle Planning: a few strategic directions, then a plan sized from your team's real pace |
| "Write a spec for <a feature>" | A few questions, then a spec with a technical plan and estimate, tracked in Devplan |
| "What slipped this week?" | The slipped, at risk, and blocked section of Execution Monitoring |
| "What shipped this week?" | The changelog at the bottom of Execution Monitoring |
| "How fast are we shipping?" | Cycle time by stage, throughput, and a summary by person |
| "Refresh my Devplan dashboards" | Every dashboard rebuilt in place |

You don't need to name a skill. Ask product questions as you normally would ("why are we building X?", "what did we decide about pricing?") and the answer starts from your Devplan workspace, with sources.

## What Devplan can access

- **Reads.** Skills read your Devplan workspace: projects, the code analysis, changes, discussions, calls, support summaries, and documents from the sources you connected in Devplan. Devplan's own permissions decide what it can see.
- **Writes, only to Devplan.** The Spec skill creates or updates a Devplan project for each spec you write. Setup can save your company context to your workspace. Nothing is posted, sent, or changed in your other tools.
- **Other connectors (optional).** Cycle Planning reads the latest strategy or planning doc from a docs tool you've connected in your AI app, if there is one.
- **The web.** The Demand Report searches the public web for competitor and market news. Setup reads your company website once.

Security and data handling: [devplan.com](https://devplan.com) · [Privacy](https://devplan.com/privacy)

## Where output goes

| | Claude (web, desktop, Cowork) | ChatGPT and the Codex app | Claude Code and Codex CLI |
|---|---|---|---|
| Dashboards | Private pages in your Claude account, updated in place on each refresh | One "Devplan" Site with a tab per report, updated in place; a local `devplan/devplan.html` when Sites isn't available | HTML files in a `devplan/` folder in your working directory (add `devplan/` to `.gitignore`) |
| Specs | A document you can edit and share, plus the Devplan project | A document, plus the Devplan project | `devplan/spec-<name>.md`, plus the Devplan project |
| Refresh | A scheduled task at 7:47 and 12:47 on weekdays; summary emailed only when something changed | A scheduled task at the same times; the last good version stays live if a run fails, and you're alerted | Not available. Say "Refresh my Devplan dashboards" when you want fresh ones |

## Cost per session

In Claude Code the plugin adds about 950 tokens to every session, mostly skill descriptions so the right skill loads when you ask. Each skill loads its full instructions only when it runs.

## Skills

| Skill | What it does |
|---|---|
| `devplan-setup` | Guided setup: connect or create Devplan, check the workspace, confirm company context, build every dashboard, and schedule refreshes where supported |
| `devplan-product-context` | Starts every product answer from your Devplan workspace |
| `daily-radar` | Your personal briefing: what shipped, what's moving, what's stuck, and what needs you |
| `execution-monitoring` | Active projects from Devplan, Linear, and Jira; slipped, at risk, and blocked work; inferred work by theme; a searchable changelog |
| `demand-report` | Demand themes with existing and suggested projects, isolated asks, adoption blockers, customer promises, and two weeks of competitor and market moves |
| `eng-analytics` | Cycle time by stage, throughput, work in progress, review load, and a summary by person |
| `cycle-planning` | Asks timeframe and team size, offers strategic directions, and plans each cycle with a timeline, estimates, and a 20% buffer |
| `spec` | Discovery questions, product and technical plan, estimate; tracked in Devplan |

## Support

[devplan.com](https://devplan.com) · [docs.devplan.com](https://docs.devplan.com) · Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
