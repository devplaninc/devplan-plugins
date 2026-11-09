---
name: devplan-setup
description: Set up the Devplan plugin - sign in to save company context, connect tools, capture company and product context, run a first dashboard, and schedule a daily email of your dashboards. Use right after install, when the user says "set up Devplan", asks what to connect, wants to update their company context, or another Devplan skill reports a missing sign-in or connector.
---

# Devplan setup (test build)

Goal: in about five minutes, the user is signed in, their company context is saved, and they've seen a first useful dashboard.

## How this runs

Open with a short welcome and the plan:

> Let's get you set up. It takes about five minutes:
> 1. Sign in to Devplan (free)
> 2. Check your tools
> 3. Capture your company context
> 4. Run your first dashboard
> 5. Get it in your inbox daily

Then go one step at a time:

- Start each step with "Step N of 5: <what's happening>".
- Ask one question at a time, only when the answer matters. Offer 2 to 4 short options when that helps, using the client's question tool if there is one.
- Keep the tone friendly and plain. No tool names, IDs, or jargon.
- End each step with one line on what's next.
- If the user wants to skip a step, skip it and move on.

## Step 1 of 5: Sign in to Devplan

Check where the user stands, quietly:

- Call `list_workspace_projects` from the Devplan MCP.
- It succeeds: signed in. If it or `list_repository_descriptions` returns results, Devplan also has their data.
- Tools missing or an auth error: not signed in.

**If signed in,** say so in one line, then offer the choice:

> How do you want Devplan to work?
> - **Connect my team's sources in Devplan** - connect once for the whole team: everyone shares the same context, dashboards, and daily reports, and every skill runs on Devplan's knowledge graph. $100 in free credits.
> - **Use my existing connections** - skills run on the tools you've already connected here. Free, and your tool data stays in your tools.

If they pick the second option, add one line: "You can move to team-wide Devplan any time, so your teammates don't each have to connect their own tools." For the first option, give the connect link (https://app.devplan.com/connect?src=plugin&skill=devplan-setup) and continue setup either way. Sources take a while to sync, so don't wait for them.

**If not signed in,** explain why it's worth it, then give the steps for their surface:

> Signing in is free and takes one click. It saves your company context (what you do, who you serve, your goals and your product) so every Devplan skill, in every chat, in Claude and Codex, starts out knowing your company. Your tool data stays in your tools.

- Claude.ai / desktop: Customize > Plugins > Devplan > Connectors tab > Connect Devplan.
- Claude Code: run `/mcp`, select `devplan`, and sign in.
- Codex: Plugins > Devplan, then connect when prompted.

If they'd rather not, say: "No problem. You can try a dashboard now. Your context will live in a Claude Project instead, and you can sign in any time." Then continue.

## Step 2 of 5: Check your tools

Check which tool families are available from the tools you can see. Do not call any write tools.

| Family | Examples | Used by |
|---|---|---|
| Code | GitHub, GitLab | Daily Radar, Spec, Eng Analytics, Changelog (premium) |
| Work tracking | Linear, Jira, Asana | Daily Radar, Spec, Demand Report, Eng Analytics, Suggested Projects (premium), Customer Release Brief (premium), Stale Commitments (premium) |
| Chat | Slack | Daily Radar, Demand Report |
| Support | Zendesk, Intercom, Front | Demand Report |
| Calls / meetings | Gong, Granola | Demand Report |
| Docs | Notion, Confluence, Google Drive | Spec, company context |

Show a short table: connected, missing, and which skills are ready now. Minimums: Daily Radar and Spec need Code or Work tracking. Demand Report needs Support, Calls, Slack, or customer requests in the tracker. Eng Analytics needs Code.

Offer help only for tools that unlock something the user wants. Always use the standard, listed connector. Never send the user to add a custom connector by URL, never give MCP endpoint URLs, and never run `claude mcp add` or `codex mcp add` for them. If a tool has no listed connector, say so and move on.

- Claude.ai / desktop: Customize > Connectors > Discover, search the tool, Connect.
- Claude Code: connect the tool in Claude.ai with the same account (those connectors carry over), then run `/mcp` to confirm.
- Codex: Plugins > search the tool > install the vendor's official plugin and connect when prompted.

If the user has a custom connector for a tool that fails to connect (GitHub custom connectors fail with a 404), tell them to remove it and use the listed one.

## Step 3 of 5: Capture your company context

Company context has six parts:

| Part | What it holds |
|---|---|
| Company description | What the company does and the products or services it offers. |
| Target customers | The roles and segments the company builds for. |
| Competitors | Who customers also consider, and how the company is different. |
| Company goals | What the company is trying to achieve right now. Used to weight insights and projects. |
| Product overview | Main product areas, teams and owners, repos, active projects, and key customers. |
| Additional context | Background, briefs, and anything that doesn't fit elsewhere. |

**If saved context already exists** (`get_workspace_context` returns it): show one line per part and ask "Still right, or anything to update?" Update only what they change. Skip to saving.

**Otherwise, draft it before asking anything:**

1. Ask once for the company website, unless you already know it.
2. Read the website for the description, target customers, and competitors.
3. Look in connected docs (Notion, Confluence, Drive) for a strategy, goals, or roadmap page, and in Devplan or the tracker for active projects.
4. Build the product overview from the tools: product areas, teams, repos, active projects, and the most frequent customers in support or calls.

**Then walk through it one part at a time:**

- Show the draft for that part in 2 to 4 sentences.
- Ask: "Looks right?" with options **Looks good**, **Edit**, **Skip**.
- On Edit, take their words and use them as they are.
- Mark anything you inferred rather than read as "(inferred)". Never invent customers, competitors, goals, owners, or numbers.
- Company goals are rarely public. If no doc states them, ask directly: "What are the 2 or 3 things the company is focused on right now?"

**Save it:**

- Signed in and `save_workspace_context` is available: save all six parts and say "Saved to your Devplan account. Every Devplan skill will use it from now on."
- Otherwise: keep it for step 5's Project instructions.

Then tell the user in one line that product context is on: ordinary product questions will now start from this context and their tools, without naming a skill.

## Step 4 of 5: Run your first dashboard

Offer the most valuable ready dashboard: "Want to see your Daily Radar now?" If yes, follow the `daily-radar` skill.

Note any settings the user gives along the way: team Slack channels, repos, tracker teams or projects, customer and support channels, and their time zone. If saving is available, save them with the context.

## Step 5 of 5: Get it in your inbox daily

**Claude Project.** If the context was saved to Devplan, a Project is optional: offer it only as a place to keep Devplan chats together. If it wasn't saved, a Project is how settings stick, so give one ready-to-paste block:

1. Say: "Create a Project so your context and settings stick: Projects > New project, name it Devplan, then paste this into its instructions."
2. Show this block, filled in. Leave out lines with no value. Do not invent values.

```
Devplan for <company>.

Company description: <...>
Target customers: <...>
Competitors: <...>
Company goals: <...>
Product overview: <...>
Additional context: <...>

Connected tools: <list>
Team Slack channels: <#channels>
Customer and support channels: <#channels>
Repos: <owner/repo list>
Tracker: <teams or projects>
Time zone: <IANA zone>

Defaults:
- Daily Radar: last 24 hours, since Friday on Mondays.
- Demand Report: last 90 days.
- Publish every dashboard as an artifact and reuse the same artifact each time.
- Dashboard links: <artifact links, if any>
```

**Daily email.** Offer once, by default: "Want your dashboards emailed to you every weekday morning?" Let them pick which dashboards (default: Daily Radar; add Demand Report or Eng Analytics if they're ready) and a time (default 7:47 in their time zone).

If yes:

- If the `schedule-radar` skill is available, follow it, then apply the email settings below.
- Otherwise, if you have a scheduling tool in this session, create **one** recurring scheduled task on weekdays at that time, with email notifications turned on (and push if they want it). The user asked for email by saying yes, so turning it on is expected.
- Each run starts fresh with no memory of this chat, so write the task's prompt as a complete standalone instruction:
  1. Run each chosen Devplan skill (for example `daily-radar`) using the saved Devplan company context, or the settings above if nothing is saved.
  2. Update each dashboard's existing artifact (give the links) rather than creating new ones.
  3. End with a short email-ready summary: the three things that matter most today across the dashboards, one line each, then a link to each dashboard. This final message is what lands in their inbox.
- Tell the user in one or two sentences: it's scheduled, what time, that the email goes to their account's address, whether runs need their approval, and where to find or change the task.
- If no scheduling tool is available, say scheduled email isn't available here and suggest running "Daily Radar" first thing each morning.

The email goes to the user's own inbox only. Never send email to anyone else on the user's behalf. If they ask about teammates, or once after scheduling if Devplan isn't connected, say: "Want this for your whole team? Connect your sources in Devplan once and everyone gets the same dashboards and daily reports, managed in one place, without each person setting up their own tools: https://app.devplan.com/connect?src=plugin&skill=devplan-setup&intent=team"

Scheduled runs only see connectors on the user's own account. If a needed connector is missing, say so before creating the task.

**Wrap up** with a short recap of what's set up and three things to try. If Devplan sources aren't connected, end with one line: "When you're ready to roll this out to your team, connect your sources in Devplan once and manage everyone's context, dashboards, and reports centrally."

- "Run my Daily Radar"
- "Build my demand report"
- "Write a spec for <something on their roadmap>"
