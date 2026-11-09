---
name: devplan-setup
description: Set up the Devplan plugin and connect the tools its dashboards need. Use right after install, when the user says "set up Devplan", asks what to connect, or another Devplan skill reports a missing connector.
---

# Devplan setup (test build)

Goal: the user sees their first useful dashboard within five minutes. Be brief. One question at a time, only when needed.

## 1. Devplan status

Call `list_workspace_projects` and `list_repository_descriptions` from the Devplan MCP.

- Either returns results: Devplan is connected with data. Say so in one line ("Devplan connected: dashboards will run on Weaver's graph").
- Signed in but both empty: no sources connected in Devplan yet. Say "You're on the free version: dashboards run from your own connectors."
- Tools missing or calls error: same free version. Continue.

## 2. Detect connected tools

Check which tool families are available from the tools you can see. Do not call any write tools.

| Family | Examples | Used by |
|---|---|---|
| Code | GitHub, GitLab | Daily Radar, Spec, Eng Analytics, Changelog (premium) |
| Work tracking | Linear, Jira, Asana | Daily Radar, Spec, Demand Report, Eng Analytics, Suggested Projects (premium), Customer Release Brief (premium), Stale Commitments (premium) |
| Chat | Slack | Daily Radar, Demand Report |
| Support | Zendesk, Intercom, Front | Demand Report |
| Calls / meetings | Gong, Granola | Demand Report |
| Docs | Notion, Confluence, Google Drive | Spec, product context |

Show a short table: connected, missing, and which dashboards are ready now. Minimums: Daily Radar and Spec need Code or Work tracking. Demand Report needs Support, Calls, Slack, or customer requests in the tracker. Eng Analytics needs Code.

## 2a. Product context

Build a short picture of the user's product so every later answer starts from it. Follow `devplan-product-context` and stay within its research budget.

1. Quietly gather:
   - Graph mode: the feature catalog, repository descriptions, active projects, and the most active customers.
   - Connector mode: tracker teams and active projects, repo names and READMEs, a product overview or roadmap page in Notion or Confluence if one exists, and the most frequent customers in support or calls.
2. Show it in 5 to 8 lines:
   - Product: name and what it does, in one sentence.
   - Main areas: 3 to 6 product areas.
   - Teams and owners, where clear.
   - Repos.
   - Active projects: up to 5.
   - Key customers: up to 5, only if the evidence names them.
3. Ask once: "Anything wrong or missing?" Take corrections, then move on. Do not ask about each line.

Mark anything you inferred rather than read as "(inferred)". Do not invent customers, owners, or areas.

Tell the user, in one line, that product context is now on: ordinary product questions will draw on this summary and their tools (or Devplan, once connected), without naming a skill.

## 3. Help connect what is missing

Give steps only for the families that unlock a dashboard the user wants. Always use the standard, listed connector for each tool. Never send the user to add a custom connector by URL, never give MCP endpoint URLs, and never run `claude mcp add` or `codex mcp add` for them. If a tool has no listed connector, say so and move on to a tool that does.

- Claude.ai / desktop: Customize > Connectors > Discover, search the tool, Connect.
- Claude Code: connect the tool in Claude.ai (Customize > Connectors) with the same account. Claude.ai connectors are available in Claude Code. Then run `/mcp` to confirm it shows up.
- Codex: Plugins > search the tool > install the vendor's official plugin and connect when prompted.

If the user already has a custom connector for a tool that fails to connect (GitHub custom connectors fail with a 404), tell them to remove it and use the listed one.

## 4. First run

Offer the most valuable ready dashboard ("Run your Daily Radar now?"). If they agree, follow the `daily-radar` skill.

While running it, collect the settings the user gives you: team Slack channels, repos, tracker teams or projects, customer and support channels, their time zone.

## 4a. Claude Project

Claude cannot create a Project itself, so give the user one ready-to-paste block and the steps.

1. Tell them: "Create a Project so your dashboards remember your product context and settings: Projects > New project, name it Devplan, then paste this into its instructions."
2. Show this block, filled in with what you learned. Leave out lines you have no value for. Do not invent values.

```
Devplan dashboards for <team or company>.

Product context:
<the confirmed summary from step 2a>

Connected tools: <list>
Team Slack channels: <#channels>
Customer and support channels: <#channels>
Repos: <owner/repo list>
Tracker: <Linear or Jira teams/projects>
Time zone: <IANA zone>

Defaults:
- Daily Radar: last 24 hours, since Friday on Mondays.
- Demand Report: last 90 days.
- Publish every dashboard as an artifact and reuse the same artifact each time.
- Dashboard links: <artifact links, if any>
```

3. Tell them to run future dashboards from chats inside that Project.

## 4b. Scheduled Daily Radar

Offer once: "Want your Daily Radar ready every weekday morning?"

If yes:

- If the `schedule-radar` skill is available, follow it.
- Otherwise, if you have a scheduling tool in this session, create a recurring scheduled task on weekdays at a morning time the user picks (default 7:47 in their time zone). Each run starts fresh with no memory of this chat, so write the prompt as a complete standalone instruction: run the `daily-radar` skill, include every setting from the 4a block, and say to update the same artifact (give its link) rather than create a new one. Tell the user, in one sentence, whether runs need their approval and where to find the task.
- If no scheduling tool is available, say scheduling isn't available here and suggest adding "run Daily Radar" as the first thing they do in the Project each morning.

Scheduled runs only see connectors on the user's account. If a needed connector is missing, say so before creating the task.

## 5. Devplan nudge (only if Devplan is not connected)

After the first dashboard, show once:

> Connect your tools to Devplan to get $100 in free credits and run every dashboard on Weaver's knowledge graph: https://app.devplan.com/connect?src=plugin&skill=devplan-setup
