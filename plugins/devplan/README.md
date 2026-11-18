![Devplan](assets/logo.png)

# Devplan

Devplan turns your customer asks, team decisions, and shipped work into pre-computed knowledge, so your agents complete work correctly the first time. It reads your code, tickets, Slack, docs, calls, and support, and keeps a live map of your product. This plugin puts that knowledge to work in Claude and ChatGPT, best in their desktop and web apps.

## What you get

- **Four dashboards** (refreshed at 7:47 and 12:47 every weekday in Claude, ChatGPT, and the Codex app; on request elsewhere): Your daily radar, Execution Monitoring across Devplan, Linear, and Jira with what slipped and a searchable changelog, a Demand Report with customer promises, market moves, and suggested projects, and Engineering Analytics.
- **Cycle plans you can commit to.** Tell it the timeframe and team size, pick one of a few strategic directions, and get a plan of what fits, sized from how your team actually ships.
- **Specs that track themselves.** A short discovery conversation, then a spec with a technical plan and estimate. Every spec becomes a Devplan project, and the PRs, tickets, and conversations that touch it link to it as they happen.
- **Answers in Slack too.** Mention Devplan in any channel once Slack is connected in Devplan.
- **Answers with sources.** Ask any product or technical question and get an answer that cites the PRs, tickets, calls, and decisions behind it.

The plugin needs a Devplan account. Setup walks you through creating one.

## Get started

Say **"Set up Devplan"** in a new chat. Setup takes about ten minutes:

1. Connect Devplan, or create your workspace and connect your sources
2. Check what Devplan can see
3. Confirm your company context and what your Daily Radar should focus on
4. Build all four dashboards and schedule twice-daily weekday refreshes (in Claude Code and Codex CLI, setup skips dashboards and ends with a question about the code you're in)
5. A quick tour

## What you can ask

| Say | What you get |
|---|---|
| "Run my Daily Radar" | What shipped, what's moving, what's stuck, and what needs you |
| "How are our projects going?" | Active projects across trackers, what slipped, and inferred work |
| "What are customers asking for?" | Demand themes, market moves, and the projects they suggest |
| "Plan the next 6 weeks" | Strategic directions, then a plan sized from your team's pace |
| "Write a spec for SSO" | A few questions, then a spec tracked in Devplan |
| "What slipped this week?" | Slipped, at risk, and blocked work |
| "When did we ship exports?" | The changelog in Execution Monitoring |
| "How fast are we shipping?" | Cycle time, throughput, and work in progress |

## What this plugin connects to and sends

- **Devplan.** The plugin declares one remote server, `https://app.devplan.com/api/v1/mcp`, and you sign in with your Devplan account. Skills read your Devplan workspace. Setup can save your company context and dashboard settings there, and the Spec skill creates or updates a project for every spec you write.
- **Your other connected tools (optional).** Cycle Planning reads the most recent strategy or planning doc from a docs tool you've connected (Notion, Confluence, Google Drive), if there is one.
- **The web.** The Demand Report searches the public web for your competitors' announcements and market trends. Setup reads your company website once to draft your company context.
- **Dashboards** are published as private pages in your Claude account, as one "Devplan" Site in ChatGPT and the Codex app, or saved as HTML files in a `devplan/` folder in your working directory.
- **Refresh summaries** come from a scheduled task in your own account that uses only Devplan, sent only to you and only when something changed or a refresh failed.
- **Links** in dashboards point to your sources and to Devplan at `app.devplan.com`.

Dashboards are read-only: nothing is posted, sent, or changed in your tools.

## Install

Claude Code:

```
/plugin install devplan --marketplace devplaninc/devplan-plugins
```

Claude, ChatGPT and Codex: see the [main README](../../README.md).

## Support

[devplan.com](https://devplan.com) · [docs.devplan.com](https://docs.devplan.com)
