---
name: devplan-setup
description: Set up the Devplan plugin - choose Devplan or your own connections, check tools, capture company and product context, save it, build every dashboard your tools support, and schedule a daily email of them. Use right after install, when the user says "set up Devplan", asks what to connect, wants to update their company context, or another Devplan skill reports a missing sign-in or connector.
---

# Devplan setup

Goal: the user's company context is captured and saved, every dashboard their tools support is built, and a daily email is scheduled.

## How this runs

Open with a short welcome and the plan:

> Let's get you set up. It takes about ten minutes:
> 1. Choose how Devplan runs
> 2. Check your tools
> 3. Capture your company context
> 4. Save it
> 5. Build your dashboards
> 6. Get them in your inbox daily

Then go one step at a time:

- Start each step with "Step N of 6: <what's happening>".
- Ask one question at a time, only when the answer matters. Offer 2 to 4 short options when that helps, using the client's question tool if there is one.
- Keep the tone friendly and plain. No tool names, IDs, or jargon.
- End each step with one line on what's next.
- If the user wants to skip a step, skip it and move on.

## Step 1 of 6: Choose how Devplan runs

Check where the user stands, quietly:

- Call `list_workspace_projects` from the Devplan MCP.
- It succeeds: signed in. If it or `list_repository_descriptions` returns results, Devplan also has their data.
- Tools missing or an auth error: not signed in.

If Devplan already has their data, say so in one line ("You're connected to Devplan: everything will run on your team's knowledge graph") and go to step 2.

Otherwise, offer the choice:

> How do you want Devplan to run?
> - **On Devplan, for the whole team** - connect your team's sources once. Everyone shares the same company context, dashboards, and daily reports, and every skill runs on Devplan's knowledge graph: faster, cheaper, and always up to date. $100 in free credits.
> - **On my own connections** - skills run on the tools you've already connected here. Free, and your tool data stays in your tools.

- **On Devplan:** if they aren't signed in, give the sign-in steps below first. Then give the connect link (https://app.devplan.com/connect?src=plugin&skill=devplan-setup&intent=team) and continue setup. Sources take a while to sync, so don't wait for them.
- **On my own connections:** say "Great, nothing to sign in to yet. You can move to Devplan any time." Then go to step 2.

Sign-in steps, by surface:

- Claude.ai / desktop: Customize > Plugins > Devplan > Connectors tab > Connect Devplan.
- Claude Code: run `/mcp`, select `devplan`, and sign in.
- Codex: Plugins > Devplan, then connect when prompted.

## Step 2 of 6: Check your tools

Check which tool families are available from the tools you can see. Do not call any write tools.

| Family | Examples | Used by |
|---|---|---|
| Code | GitHub, GitLab | Daily Radar, Spec, Eng Analytics, Changelog, Customer Release Brief |
| Work tracking | Linear, Jira, Asana | Daily Radar, Spec, Demand Report, Eng Analytics, Suggested Projects, Customer Release Brief, Stale Commitments |
| Chat | Slack | Daily Radar, Demand Report, Stale Commitments |
| Support | Zendesk, Intercom, Front | Demand Report |
| Calls / meetings | Gong, Granola | Demand Report, Stale Commitments |
| Docs | Notion, Confluence, Google Drive | Spec, company context |

Show a short table: connected, missing, and which skills are ready now. Minimums: Daily Radar, Spec, and Customer Release Brief need Code or Work tracking. Demand Report needs Support, Calls, Slack, or customer requests in the tracker. Eng Analytics and Changelog need Code. Stale Commitments and Suggested Projects need Work tracking.

Offer help only for tools that unlock something the user wants. Always use the standard, listed connector. Never send the user to add a custom connector by URL, never give MCP endpoint URLs, and never run `claude mcp add` or `codex mcp add` for them. If a tool has no listed connector, say so and move on.

- Claude.ai / desktop: Customize > Connectors > Discover, search the tool, Connect.
- Claude Code: connect the tool in Claude.ai with the same account (those connectors carry over), then run `/mcp` to confirm.
- Codex: Plugins > search the tool > install the vendor's official plugin and connect when prompted.

If the user has a custom connector for a tool that fails to connect (GitHub custom connectors fail with a 404), tell them to remove it and use the listed one.

## Step 3 of 6: Capture your company context

Company context has six parts:

| Part | What it holds |
|---|---|
| Company description | What the company does and the products or services it offers. |
| Target customers | The roles and segments the company builds for. |
| Competitors | Who customers also consider, and how the company is different. |
| Company goals | What the company is trying to achieve right now. Used to weight insights and projects. |
| Product overview | Main product areas, teams and owners, repos, active projects, and key customers. |
| Additional context | Background, briefs, and anything that doesn't fit elsewhere. |

**If saved context already exists** (in Devplan via `get_workspace_context`, or in a local file or Project block from an earlier setup): say who it came from if known ("Your team already saved your company context"), show one line per part, and ask "Still right, or anything to update?" with options **Looks good**, **Update some**. Update only what they change, then go to step 4.

**Otherwise, draft it before asking anything:**

1. Ask once for the company website, unless you already know it.
2. Read the website for the description, target customers, and competitors.
3. Look in connected docs (Notion, Confluence, Drive) for a strategy, goals, or roadmap page, and in Devplan or the tracker for active projects.
4. Build the product overview from the tools: product areas, teams, repos, active projects, and the most frequent customers in support or calls.

**Then confirm it:**

- First offer the fast path: show all six drafts together, 2 to 4 sentences each, and ask "Look right?" with options **Looks good, all of it**, **Go through it one by one**.
- One by one: show each part and ask "Looks right?" with options **Looks good**, **Edit**, **Skip**. On Edit, use their words as they are.
- Mark anything you inferred rather than read as "(inferred)". Never invent customers, competitors, goals, owners, or numbers.
- Company goals are rarely public. If no doc states them, ask directly: "What are the 2 or 3 things the company is focused on right now?"

Then tell the user in one line that product context is on: ordinary product questions will now start from this context and their tools, without naming a skill.

## Step 4 of 6: Save it

**If signed in and `save_workspace_context` is available:** save all six parts, plus the settings gathered so far, and say: "Saved to Devplan. Your teammates will start with this too; they'll just confirm it." Go to step 5.

**Otherwise, ask once:**

> Want to save this to Devplan? It's free.
> - It follows you into every chat, in Claude and Codex, so you never set this up again.
> - Your company context belongs to the whole team. Saved in Devplan, your teammates start with it already filled in and just confirm it. Saved only here, each teammate repeats this setup, and the copies drift apart.
> - Your tool data stays in your tools. Only this context is saved.

Options: **Sign in and save**, **Save it just for me, here**.

- **Sign in and save:** give the sign-in steps from step 1, then save as above.
- **Save it just for me, here:** use the local fallback below, and say in one line where it lives and that it isn't shared.

**Local fallback, by surface.** Write the context block below, filled in, leaving out lines with no value:

- **Claude Code:** write it to `${CLAUDE_PLUGIN_DATA}/company-context.md`. This is the plugin's own folder for this user. It survives plugin updates and isn't in any repository. Never write company context into a project repository.
- **Codex:** write it to `~/.codex/devplan/company-context.md` (create the folder if needed). Never write it into a project repository.
- **Claude.ai / desktop:** chats can't keep files, so use a Claude Project. Say: "Create a Project so this sticks: Projects > New project, name it Devplan, and paste this into its instructions." Show the block, and run future Devplan chats inside that Project.

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
Dashboard links: <artifact links, added after step 5>
```

## Step 5 of 6: Build your dashboards

Build every dashboard the user's connections support, so setup ends with a full set rather than one sample. Every dashboard works from the user's own connections; with the Devplan graph connected, each one runs on the graph instead.

| Dashboard | Build when | Refresh |
|---|---|---|
| Daily Radar | Code or Work tracking connected | Daily |
| Demand Report | Support, Calls, Slack, or customer requests in the tracker | Daily |
| Engineering Analytics | Code connected | Daily |
| Stale Commitments | Work tracking connected | Daily |
| Suggested Projects | Work tracking connected | Daily |
| Changelog | Code connected | Daily |
| Customer Release Brief | Work tracking or Code connected | Daily |

**Confirm once.** Say what you'll build and roughly how long it takes, for example: "Your tools support 5 dashboards: Daily Radar, Demand Report, Engineering Analytics, Stale Commitments, and Changelog. Building them takes a few minutes. Build all of them?" Options: **Build all**, **Pick which**, **Just Daily Radar**. If the Devplan graph isn't connected, add one line: "These will run on your own connections. On Devplan, they run faster and cheaper, stay up to date on their own, and are shared with your team."

**Build them one at a time,** in the table's order. For each:

- Say "Building 2 of 5: Demand Report".
- Follow that dashboard's skill, using the saved company context and the settings gathered so far. Ask the skill's one-time questions (for example, which Slack channels) only once across all dashboards, and reuse the answer.
- Publish it as its own artifact and keep its link.
- If one fails or has too little data, say so in one line, skip it, and continue. Never let one dashboard stop setup.

**Finish with a list** of every dashboard built, each with its link and one line on what it shows. Add the links and any new settings to wherever the context was saved in step 4.

## Step 6 of 6: Get them in your inbox daily

Offer once: "Want your dashboards emailed to you every weekday morning?" Default time 7:47 in their time zone. The email covers every dashboard built in step 5.

If yes:

- If the `schedule-radar` skill is available, follow it, then apply the email settings below.
- Otherwise, if you have a scheduling tool in this session, create **one** recurring scheduled task on weekdays at that time, with email notifications turned on (and push if they want it). The user asked for email by saying yes, so turning it on is expected.
- Each run starts fresh with no memory of this chat, so write the task's prompt as a complete standalone instruction:
  1. Refresh every dashboard built in step 5 (list each by its skill name). Load the company context from where step 4 saved it (Devplan, or give the local file path or say it's in the Devplan Project). Each skill picks graph or connector mode on its own, so the email keeps working if the Devplan connection changes.
  2. Update each dashboard's existing artifact (give the links) rather than creating new ones.
  3. End with a short email-ready summary: the three things that matter most today across the dashboards, one line each, then a link to every dashboard. This final message is what lands in their inbox.
- Tell the user in one or two sentences: it's scheduled, what time, that the email goes to their account's address, whether runs need their approval, and where to find or change the task.
- If no scheduling tool is available, say scheduled email isn't available here and suggest running "Daily Radar" first thing each morning.

Scheduled runs only see connectors on the user's own account. If a needed connector is missing, say so before creating the task.

The email goes to the user's own inbox only. Never send email to anyone else on the user's behalf. If they ask about teammates, or once after scheduling if Devplan isn't connected, say: "Want this for your whole team? Connect your sources in Devplan once and everyone gets the same context, dashboards, and daily reports, managed in one place, without each person setting up their own tools: https://app.devplan.com/connect?src=plugin&skill=devplan-setup&intent=team"

**Wrap up** with a short recap of what's set up and three things to try:

- "Write a spec for <something on their roadmap>"
- "What should I know before changing <an area of their product>?"
- Open any dashboard and ask a follow-up question about it

If Devplan isn't connected, end with one line: "When you're ready to roll this out to your team, connect your sources in Devplan once and manage everyone's context, dashboards, and reports centrally."
