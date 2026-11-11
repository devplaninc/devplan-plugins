![Devplan](assets/logo.png)

# Devplan

Daily product and engineering dashboards, built from the tools your team already uses. Devplan turns GitHub, Linear, Jira, Slack, Notion, Zendesk, Gong and more into a Daily Radar of what shipped and what's stuck, a Demand Report of what customers need, engineering analytics, a daily changelog, stale commitments, suggested projects, customer release briefs, and grounded specs.

Everything works on your own connections. Connect Devplan to run it all on a shared knowledge graph: faster and cheaper, always up to date, the same for your whole team, and with people, customers and projects matched across every tool.

## Get started

Say **"Set up Devplan"** in a new chat. Setup takes about ten minutes and walks you through six steps:

1. Choose how Devplan runs: on your own connections (free) or on Devplan for your whole team
2. Check which tools are connected
3. Capture your company context (description, customers, competitors, goals, product overview)
4. Save it to Devplan (free sign-in) or keep it just for you
5. Build every dashboard your tools support
6. Optionally get them by email every weekday morning

## What you can ask

| Say | What you get |
|---|---|
| "Run my Daily Radar" | What shipped, what's moving, what's stuck, and who owns it |
| "Build my demand report" | Recurring customer asks, adoption blockers, and demand nobody is building |
| "Write a spec for SSO" | A few questions, then a spec with a technical plan and estimate |
| "How fast are we shipping?" | Cycle time, review waits, throughput, and work in progress |
| "What slipped this week?" | Commitments that went quiet, slipped, or got blocked |
| "What shipped today?" | A plain-language changelog |
| "What should we build next?" | Project ideas backed by evidence |
| "Who should we tell about what shipped?" | Releases matched to the customers who asked, with drafts |

You don't need to name a skill. Ordinary product questions start from your company context and tools.

## What this plugin connects to and sends

- **Your connected tools.** Skills read from the connectors you've already added (for example GitHub, Linear, Slack, Zendesk, Gong). They are read-only: nothing is posted, sent, or changed unless you ask after seeing the result.
- **Devplan (optional).** The plugin declares one remote server, `https://app.devplan.com/api/v1/mcp`. If you connect it, skills read your Devplan workspace, and setup can save your company context and settings there. In free mode without Devplan, no tool data is sent to Devplan.
- **Your company website.** During setup, Claude reads your public website once to draft your company context.
- **Local files.** If you keep your context on your machine instead of in Devplan, setup writes `company-context.md` to the plugin's own data folder (Claude Code) or `~/.codex/devplan/` (Codex). Never to a project repository.
- **Dashboards** are published as artifacts in your Claude account, or saved as HTML files in your working folder.
- **Daily email (optional)** is a scheduled task in your own account, sent only to you.
- **Links** in reports point to your sources and to Devplan sign-up at `app.devplan.com`.

## Support

[devplan.com](https://devplan.com) · [docs.devplan.com](https://docs.devplan.com)
