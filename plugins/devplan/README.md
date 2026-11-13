![Devplan](assets/logo.png)

# Devplan

Product intelligence for software teams, inside Claude, ChatGPT and Codex. Devplan reads your code, tickets, Slack, docs, calls, and support, and keeps a live map of your product: what exists, what's shipping, what customers ask for, and what was decided. This plugin puts that map to work in your chats.

## What you get

- **Six dashboards, refreshed every weekday:** a Daily Radar tailored to you, Execution Monitoring for planned and inferred projects, a Demand Report that turns customer demand and market moves into suggested projects, Stale Commitments, a searchable Changelog, and Engineering Analytics.
- **Cycle plans you can commit to.** Tell it the timeframe and team size, pick one of a few strategic directions, and get a plan of what fits, sized from how your team actually ships.
- **Specs that track themselves.** A short discovery conversation, then a spec with a technical plan and estimate. Every spec becomes a Devplan project, and the PRs, tickets, and conversations that touch it link to it as they happen.
- **Answers with sources.** Ask any product question and get an answer that cites the PRs, tickets, calls, and decisions behind it.

The plugin needs a Devplan account. Setup walks you through creating one.

## Get started

Say **"Set up Devplan"** in a new chat. Setup takes about ten minutes:

1. Connect Devplan, or create your workspace and connect your sources
2. Check what Devplan can see
3. Confirm your company context and what your Daily Radar should focus on
4. Build all six dashboards and schedule weekday refreshes
5. A quick tour

## What you can ask

| Say | What you get |
|---|---|
| "Run my Daily Radar" | What shipped, what's moving, what's stuck, and what needs you |
| "How are our projects going?" | Every planned and inferred project, with activity, progress, and risks |
| "What are customers asking for?" | Demand themes, market moves, and the projects they suggest |
| "Plan the next 6 weeks" | Strategic directions, then a plan sized from your team's pace |
| "Write a spec for SSO" | A few questions, then a spec tracked in Devplan |
| "What slipped this week?" | Commitments that went quiet, slipped, or got blocked |
| "When did we ship exports?" | The searchable Changelog |
| "How fast are we shipping?" | Cycle time, throughput, and work in progress |

## What this plugin connects to and sends

- **Devplan.** The plugin declares one remote server, `https://app.devplan.com/api/v1/mcp`, and you sign in with your Devplan account. Skills read your Devplan workspace. Setup can save your company context and dashboard settings there, and the Spec skill creates or updates a project for every spec you write.
- **Your other connected tools (optional).** Cycle Planning reads the most recent strategy or planning doc from a docs tool you've connected (Notion, Confluence, Google Drive), if there is one.
- **The web.** The Demand Report searches the public web for your competitors' announcements and market trends. Setup reads your company website once to draft your company context.
- **Dashboards** are published as artifacts in your account, or saved as HTML files in your working folder.
- **Daily email** is a scheduled task in your own account, sent only to you.
- **Links** in dashboards point to your sources and to Devplan at `app.devplan.com`.

Dashboards are read-only: nothing is posted, sent, or changed in your tools.

## Support

[devplan.com](https://devplan.com) · [docs.devplan.com](https://docs.devplan.com)
