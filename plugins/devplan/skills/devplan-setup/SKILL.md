---
name: devplan-setup
description: Set up Devplan - connect or create a Devplan workspace, confirm company context, build every dashboard, and schedule weekday refreshes. Use right after install, when the user says "set up Devplan", "get started", "what does Devplan do", wants to change their dashboards, schedule, or company context, or another Devplan skill finds Devplan isn't connected.
---

# Devplan setup

Goal: by the end, the user has Devplan connected, their company context confirmed, a full set of live dashboards, and a weekday refresh scheduled. They should also know what Devplan does for them and their team, and what to expect while it builds.

## How this runs

Open with a short welcome that shows what they're about to get, then the plan:

> Welcome to Devplan. In about ten minutes you'll have:
> - Six dashboards built from your team's real work, refreshed every weekday morning
> - Product answers in any chat, grounded in your code, tickets, calls, and Slack, with sources
> - A shared memory of what your company decided and why
>
> 1. Connect Devplan
> 2. Check your workspace
> 3. Confirm your company context
> 4. Build your dashboards and schedule updates
> 5. A quick tour

Then go one step at a time:

- Start each step with "Step N of 5: <what's happening>".
- Ask one question at a time, only when the answer matters. Offer 2 to 4 short options, using the client's question tool if there is one.
- Keep the tone friendly and plain. No tool names, IDs, or jargon.
- End each step with one line on what's next.
- If the user wants to skip a step, skip it and move on.
- If setup already ran (saved settings list dashboard links), say so and ask what to change: **Company context**, **Dashboards**, **Schedule**, **Start over**. Jump to that step.

## Step 1 of 5: Connect Devplan

Check whether the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.

**Connected:** call `list_workspace_projects` with a small limit. If it answers, say "You're connected to Devplan." and go to step 2. If it fails with a sign-in error, treat Devplan as not connected.

**Not connected:** ask "Do you have a Devplan account?" with options **Yes, connect it**, **No, create one**, **What is Devplan?**

- **What is Devplan?** Answer in four lines, then ask again:
  > Devplan connects to your code, tickets, Slack, docs, calls, and support, and keeps a live map of your product: what exists, what's shipping, what customers are asking for, and what was decided.
  > It links every PR, ticket, conversation, and customer request to the people, projects, and features it belongs to, across all your tools.
  > Claude, Slack, and your team work from that same map, so nobody starts from scratch.
  > Setup takes about ten minutes of your time. Devplan does the rest in the background.

- **No, create one.** Show what to expect, then the link:
  > Here's what happens in Devplan:
  > 1. **Create your account and workspace.** If your company already has a Devplan workspace, join it instead so you share the same context.
  > 2. **Describe your company and product.** Devplan drafts this from your website. Fix anything important, like who your customers are.
  > 3. **Connect a code repository.** This is required. Then add the rest of your team's tools: Linear or Jira, Slack, Notion or Confluence, Gong or Granola, Zendesk or Intercom. For each one, pick the repos, channels, and projects Devplan should read.
  > 4. **Devplan builds your knowledge graph.** It reads the code to learn what your product does, then links tickets, PRs, conversations, and customer requests to the people, projects, and features they belong to. How long it takes depends on how much you connect. Early results appear before it finishes, and it keeps enriching in the background.
  > 5. **Come back here and connect Devplan.** You don't need to wait for the graph to finish.
  >
  > Start here: https://app.devplan.com/?mode=signup&src=plugin&skill=devplan-setup

  Then give the connect steps below, and say: "Once you've connected a repo, connect Devplan here and say 'continue'."

- **Yes, connect it.** Give the connect steps.

Connect steps, by surface:

- **Claude (web and desktop):** Customize > Plugins > Devplan > Connectors tab > Connect Devplan, then sign in.
- **Claude Code:** run `/mcp`, select `devplan`, and sign in.
- **ChatGPT and Codex:** open Plugins > Devplan and connect, or @-mention Devplan in a chat and sign in when asked.

When the user says they're connected, check again. If the tools still don't appear, say: "Start a new chat and say 'Set up Devplan'. I'll pick up at step 2."

## Step 2 of 5: Check your workspace

Quietly find out what Devplan has, in a few calls:

- `get_workspace_context`, if available (workspace name, settings, links).
- `list_repository_descriptions`: repos analyzed.
- `list_workspace_projects`: planned and inferred projects.
- `list_workspace_members`: team size.
- One `search_entities` call over the last 30 days with `change`, `discussion_topic`, `call_note`, `customer_support_ticket`, and `document`, a few results each, to see which kinds of sources have data.

Show a short summary: the workspace name, what Devplan can see (for example "4 repos, Linear, Slack, Gong; no support tool yet"), and which dashboards are ready:

| Dashboard | Needs |
|---|---|
| Daily Radar | Code or ticket activity |
| Execution Monitoring | Projects or code activity |
| Demand Report | Customer evidence: support tickets, calls, customer Slack, or requests |
| Stale Commitments | Projects, tickets, or discussions |
| Changelog | Code changes |
| Engineering Analytics | Pull requests |

- **Graph still building** (repos and projects both empty): "Devplan is still building your graph. I'll set everything up now. Your dashboards fill in as the analysis finishes, and each morning's refresh picks up the rest."
- **A source type is missing:** one line per gap, only where it unlocks a dashboard: "Connect a support tool in Devplan (Integrations) to fill in your Demand Report." Link https://app.devplan.com.

## Step 3 of 5: Confirm your company context

Company context has six parts: company description, target customers, competitors, company goals, product overview, and additional context. Every Devplan skill starts from it, and it's shared with the whole workspace.

**If Devplan already has it** (from `get_workspace_context`, or written during Devplan onboarding): show one line per part and ask "Still right?" with options **Looks good**, **Update some**. Update only what they change.

**If parts are missing,** draft them before asking anything:

1. Read the company website (ask once for the URL if you don't know it) for the description, target customers, and competitors.
2. Build the product overview from Devplan: product areas from the feature catalog, repos, active projects, and the customers who come up most in support and calls.
3. Company goals are rarely public. Look for a strategy or goals document in Devplan. If there isn't one, ask: "What are the 2 or 3 things the company is focused on right now?"
4. Show all parts together, 2 to 4 sentences each, with options **Looks good, all of it**, **Go through it one by one**. Mark anything inferred as "(inferred)". Never invent customers, competitors, goals, owners, or numbers.

**Save it:** if `save_workspace_context` is available, save the parts and say "Saved to Devplan. Your teammates start from this too." Otherwise say "Add this under Knowledge > Workspace in Devplan so your whole team shares it," and show the text to copy.

**Then personalize the Daily Radar.** If you already know the user's role and focus from memory or earlier conversations, confirm it in one line. Otherwise ask once: "What should your Daily Radar focus on?" with options **My team's work**, **Specific projects**, **Customers and revenue**, **Everything**. Follow up for names only if they pick specific projects. Keep the answer as the radar focus for step 4.

## Step 4 of 5: Build your dashboards and schedule updates

**Confirm once.** Name what you'll build and when it refreshes:

> Your workspace supports 6 dashboards: Daily Radar, Execution Monitoring, Demand Report, Stale Commitments, Changelog, and Engineering Analytics. I'll build them now (a few minutes) and refresh them every weekday at 7:47 AM your time, with a short summary emailed to you.

Options: **Build and schedule**, **Pick a different time**, **Build without scheduling**. Only list dashboards step 2 found ready; mention the rest will be added once their sources are connected.

**Build them one at a time,** in this order: Daily Radar, Execution Monitoring, Demand Report, Stale Commitments, Changelog, Engineering Analytics. For each:

- Say "Building 2 of 6: Execution Monitoring".
- Follow that dashboard's skill, using the company context, the radar focus, and the settings gathered so far.
- Publish it as its own artifact (or file) and keep its link.
- If one fails or has too little data, say so in one line and continue. Never let one dashboard stop setup.

**Schedule the refresh.** If you have a scheduling tool in this session, create **one** recurring scheduled task on weekdays at the chosen time in the user's time zone, with email notifications on (and push if they want it). Each run starts fresh with no memory of this chat, so write its prompt as a complete standalone instruction:

```
Refresh my Devplan dashboards. Use the Devplan plugin skills.

1. Rebuild each dashboard below with its skill, and update the existing artifact at its link instead of creating a new one:
   - Daily Radar (daily-radar): <link>
   - Execution Monitoring (execution-monitoring): <link>
   - Demand Report (demand-report): <link>
   - Stale Commitments (stale-commitments): <link>
   - Changelog (changelog): <link>
   - Engineering Analytics (eng-analytics): <link>
2. Daily Radar is for <name> (<email>), <role>. Focus: <radar focus>.
3. Time zone: <IANA zone>. In each footer, the refresh line is "Refreshes weekdays at <time>".
4. If Devplan isn't connected, skip the dashboards and reply only: "Your Devplan dashboards didn't refresh because Devplan isn't connected. Open Claude and say 'Set up Devplan'."
5. Finish with an email-ready summary: the three things that matter most today across all dashboards, one line each with a link, then a link to every dashboard. This final message is the email.
```

Then tell the user in one or two sentences: it's scheduled, at what time, that the summary goes to their account's email, whether runs need their approval, and where to change it. If no scheduling tool is available, say scheduled refresh isn't available here and suggest saying "Refresh my Devplan dashboards" each morning.

If `save_workspace_context` is available, save the dashboard links, schedule, and time zone in the workspace settings.

## Step 5 of 5: A quick tour

Finish with a short recap of what's set up (dashboards with links, refresh time), then what they can do now:

- **Act from a dashboard.** "Write spec" and "New project" buttons copy a ready message. Paste it here and I'll take it from there.
- **Ask anything about the product.** "What did we decide about pricing?", "What should I know before changing billing?", "Who's working on SSO?" Answers cite the PRs, tickets, calls, and decisions behind them.
- **Ask in Slack.** Mention Devplan in a channel and get the answer with its sources. If Slack isn't connected in Devplan yet, add it under Integrations.
- **Decisions don't get lost.** Devplan captures decisions from Slack, meetings, and specs with their reasoning, so the team stops reopening settled questions.
- **Plan a cycle.** "Plan the next 6 weeks" sizes what the team can do from how it actually ships, offers a few strategic directions, and lays out what fits.
- **Specs are tracked automatically.** Any spec written here becomes a Devplan project, and the PRs, tickets, and conversations that touch it link to it as they happen.

Then one subtle team line, once: "Devplan works best when your team shares it: everyone gets the same context, dashboards, and decision history. [Invite teammates](<members page>)." Build the members link as described in `devplan-product-context`.

Suggest one first thing to try, based on what you saw in step 2, for example "Write a spec for <the top suggested project in your Demand Report>".
