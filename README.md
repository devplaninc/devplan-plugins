<p align="center"><img src="assets/logo.png" width="96" alt="Devplan" /></p>

# Devplan for Claude and ChatGPT

Devplan turns your code, tickets, Slack, docs, calls, customer feedback, and CRM data into pre-computed product knowledge: what was decided and why, what's shipping, and what customers are asking for. Your agent starts every task already knowing it, so it gets the work right the first time and spends far fewer tokens getting there.

This plugin brings that knowledge into the Claude and ChatGPT apps:

- **Agents that start from what your company knows.** Every product or technical answer, spec, and plan draws on your real decisions, customer asks, and shipped work, with sources you can check.
- **Fewer tokens per task.** Agents pull pre-computed answers instead of searching and re-reading Slack threads, tickets, and code on every question.
- **Four dashboards, refreshed twice every weekday.** Your daily radar, Execution Monitoring, Demand Report, and Engineering Analytics, built from your team's real work.
- **Specs and cycle plans that track themselves.** Specs are estimated from your team's git history and saved as Devplan projects; cycle plans are sized from how your team actually ships.
- **Answers in Slack too.** Mention Devplan in any channel and get the same answer, with its sources.

**Before you install:** the plugin needs a Devplan account with a **code repository connected**. That's required; tickets, Slack, docs, calls, customer feedback, and CRM data make it better. Setup walks you through creating an account if you don't have one.

**Pricing:** Devplan runs on credit packs, starting at $50. Purchased credits never expire. New workspaces get $100 in free credits, valid for 3 months, with no credit card. [See pricing](https://www.devplan.com/pricing/)

## Install (recommended: the Claude or ChatGPT desktop app)

The desktop and web apps give you the full experience: live dashboards that refresh on their own, specs as shareable documents, and guided setup. Once Devplan is installed, say **"Set up Devplan"** in a new chat.

### Claude desktop and web

1. Open **Plugins** in the sidebar, then **Add > Add marketplace > Add from a repository**.
2. Enter `https://github.com/devplaninc/devplan-plugins` and select **Sync**.
3. Open **Devplan** and select **Add**.
4. Say **"Set up Devplan"** in a new chat. When setup asks you to connect, open **Plugins > Devplan > Connect**. Claude shows a connector form: keep the defaults, click **Add**, then sign in to Devplan.

Installed on Claude, the plugin also shows up in Cowork and Claude Code on the same account.

### ChatGPT desktop and web

1. Open **Plugins**, choose to add a marketplace, and enter `https://github.com/devplaninc/devplan-plugins`.
2. Open the **Devplan** marketplace, then **Devplan**, and select **+** to install it.
3. Say **"Set up Devplan"** and sign in when asked.

In ChatGPT, @-mention **Devplan** or pick it from **+ > More**. If you don't see an option to add a marketplace on your plan, use **Connect Devplan directly** below.

### For workspace admins

- **Claude Team and Enterprise:** add the marketplace in your organization's plugin settings to make Devplan available to everyone.
- **ChatGPT Business, Enterprise and Edu:** import `https://github.com/devplaninc/devplan-plugins` under **Workspace settings > Plugins > Marketplaces**. It syncs daily; use **Sync now** to pull changes. Set Devplan to **Installed** to install it for everyone.

## Getting started

Start a new chat in Claude or ChatGPT and say:

> **Set up Devplan**

Setup takes about ten minutes and goes one step at a time:

1. **Connect Devplan.** If you don't have an account yet, setup explains what happens in Devplan first: create a workspace, describe your company, connect a code repository and the rest of your team's tools, and let Devplan build your knowledge graph. You don't need to wait for the graph to finish.
2. **Check your workspace.** See what Devplan can read and which dashboards are ready.
3. **Confirm your company context.** Description, customers, competitors, goals, and product overview. Then tell your daily radar which areas to focus on.
4. **Build your dashboards.** All four, built in a few minutes and refreshed at 7:47 AM and 12:47 PM every weekday. You get a short summary only when something changed.
5. **A quick tour.** Product and technical questions to try first, answering in Slack, and how to bring your team in.

Claude may ask before each Devplan tool it uses. Devplan's read tools only read your workspace, so you can choose **Always allow** for them.

### Try these next

| Say | What you get |
|---|---|
| "What should I know before changing billing?" | The decisions, customer asks, open risks, and recent changes behind that area, with sources |
| "Why did we build webhooks this way?" | The PRs, threads, calls, and specs behind it |
| "Run my daily radar" | The biggest themes for your role, product updates, and what's in motion |
| "How are our projects going?" | Execution Monitoring: active projects from Devplan, Linear, and Jira, what slipped, inferred work, and the changelog |
| "What are customers asking for?" | Your Demand Report: themes built from Devplan's suggested projects, isolated asks, adoption blockers, customer promises, and two weeks of market moves |
| "How fast are we shipping?" | Engineering Analytics: throughput, cycle time, and PRs by person and repo, daily or weekly |
| "Plan the next 6 weeks" | Cycle Planning: a few strategic directions, then a plan with a timeline, estimates, and a 20% buffer |
| "Write a spec for <a feature>" | A few questions, then a spec with a technical plan and estimate, tracked in Devplan |
| "Refresh my Devplan dashboards" | Every dashboard rebuilt in place |

You don't need to name a skill. Ask product questions as you normally would and the answer starts from your Devplan workspace.

**In Slack:** once Slack is connected in Devplan (Integrations), mention Devplan in any channel or thread to get the same answers, with sources, where your team already talks.

## What Devplan can access

- **Reads.** Skills read your Devplan workspace: projects, the code analysis, changes, discussions, calls, support summaries, and documents from the sources you connected in Devplan. Devplan's own permissions decide what it can see.
- **Writes, only to Devplan.** The Spec skill creates or updates a Devplan project for each spec you write. Setup can save your company context to your workspace. Nothing is posted, sent, or changed in your other tools.
- **Other connectors (optional).** Cycle Planning reads the latest strategy or planning doc from a docs tool you've connected in your AI app, if there is one.
- **The web.** The Demand Report searches the public web for competitor and market news. Setup reads your company website once.

Security and data handling: [devplan.com](https://devplan.com) · [Privacy](https://devplan.com/privacy)

## Updating and uninstalling

- **Claude:** the marketplace syncs from GitHub; reinstall Devplan if a new version doesn't appear. To remove it, open **Plugins > Devplan** and remove it.
- **ChatGPT:** reinstall Devplan from **Plugins** if a new version doesn't appear. To remove it, remove Devplan from **Plugins**.

Uninstalling doesn't delete your Devplan workspace or anything saved in it.

## Or connect Devplan directly

If you can't install plugins, add Devplan as a server instead. You get Devplan's knowledge, so your assistant can answer from your workspace, but not the skills: no guided setup, dashboards, spec flow, or cycle planning.

- **Server URL:** `https://app.devplan.com/api/v1/mcp` (sign in with your Devplan account)
- **Claude:** add a custom connector with that URL.
- **ChatGPT:** **Plugins > Add > Add custom MCP server**, with that URL.

If you later install the plugin, remove this server so you don't have two Devplan connections.

## Skills

| Skill | What it does |
|---|---|
| `devplan-setup` | Guided setup: connect or create Devplan, check the workspace, confirm company context, build every dashboard, and schedule refreshes where supported |
| `devplan-product-context` | Starts every product and technical answer from your Devplan workspace |
| `daily-radar` | Your daily radar: the biggest themes for your role, product updates, and what's in motion |
| `execution-monitoring` | Active projects from Devplan, Linear, and Jira; slipped, blocked, and at-risk work; inferred work by theme; a searchable changelog |
| `demand-report` | Demand themes built from Devplan's suggested projects, isolated asks, adoption blockers, customer promises, and two weeks of competitor and market moves |
| `eng-analytics` | Throughput, cycle time, review load, and work in progress, daily or weekly, by person and repo |
| `cycle-planning` | Asks timeframe and team size, offers strategic directions, and plans each cycle with a timeline, estimates, and a 20% buffer |
| `spec` | Discovery questions, product and technical plan, estimate; tracked in Devplan |

## Claude Code and Codex CLI

The plugin also runs in a terminal. There it's built for engineers: Devplan's knowledge while you code, so your coding agent knows the decisions, customer asks, and recent changes behind the files it's touching. Setup is three short steps (connect, check your workspace and company context, try it on the code in front of you) and doesn't build dashboards. Ask for one any time ("Build my daily radar") and it's written to a `devplan/` folder in your working directory; add `devplan/` to `.gitignore`. Scheduled refreshes aren't available in a terminal.

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

- **Update:** `claude plugin marketplace update devplan`
- **Uninstall:** `claude plugin uninstall devplan@devplan`
- **Connect without the plugin:** `claude mcp add --transport http devplan https://app.devplan.com/api/v1/mcp`
- **Cost per session:** the plugin adds about 950 tokens to every session, mostly skill descriptions so the right skill loads when you ask. Each skill loads its full instructions only when it runs.

### Codex CLI

```
codex plugin marketplace add https://github.com/devplaninc/devplan-plugins
codex plugin add devplan@devplan
codex mcp add devplan --url https://app.devplan.com/api/v1/mcp
```

The last command opens Devplan's sign-in in your browser. It's a one-time step until Devplan is listed in OpenAI's plugin directory. Then start a new Codex session and say **"Set up Devplan"**. Plugins aren't available in the Codex IDE extension.

- **Update:** `codex plugin marketplace upgrade`
- **Uninstall:** remove Devplan with `/plugins`, then run `codex mcp remove devplan`.

### Try these in a terminal

| Say | What you get |
|---|---|
| "What should I know before changing <this module>?" | Past decisions, customer asks, open risks, and recent changes for that area |
| "Write a spec for <feature>" | A spec with a technical plan and an estimate from your team's git history, saved to Devplan for your PM |
| "Why did we build <thing> this way?" | The PRs, threads, and calls behind it |
| "Who knows <service> best?" | The people who've worked on it most, from the graph |

## Support

[devplan.com](https://devplan.com) · [docs.devplan.com](https://docs.devplan.com) · Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
