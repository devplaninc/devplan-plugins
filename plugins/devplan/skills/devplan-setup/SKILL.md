---
name: devplan-setup
description: Set up Devplan - connect or create a Devplan workspace, confirm company context, build every dashboard, and schedule twice-daily weekday refreshes. Use right after install, when the user says "set up Devplan", "get started", "what does Devplan do", says "refresh my Devplan dashboards", wants to change their dashboards, schedule, or company context, or another Devplan skill finds Devplan isn't connected.
---

# Devplan setup

Goal: by the end, the user has Devplan connected, their company context confirmed, a full set of live dashboards, and a weekday refresh scheduled. They should also know what Devplan does for them and their team, and what to expect while it builds.

## How this runs

On a first run, your first message is always this welcome and the plan, on every surface, even when Devplan is already connected:

> Welcome to Devplan. In about ten minutes you'll have:
> - Four dashboards built from your team's real work, refreshed twice every weekday
> - Answers to any product or technical question, grounded in your code, tickets, calls, and Slack, with sources
> - Your customer asks, team decisions, and shipped work turned into knowledge your agents use, so they get work right the first time
> - Answers in Slack too: mention Devplan in any channel
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
- If setup already ran (saved settings list dashboard links or a Site, or `devplan/devplan*.html` files exist in the working folder), say so and ask what to change: **Company context**, **Dashboards**, **Schedule**, **Start over**. Jump to that step.
- If the user asks to refresh their dashboards, skip the welcome and the questions: rebuild every dashboard that exists, in step 4's order (Daily Radar, Execution Monitoring, Demand Report, Engineering Analytics), updating each in place, then give the same short summary a scheduled run would.

## In a terminal (Claude Code or Codex CLI)

Engineers in a terminal want Devplan's knowledge while they code, not dashboards. On these surfaces, run a shorter setup instead of the five steps:

> Welcome to Devplan. Devplan turns your customer asks, team decisions, and shipped work into knowledge your coding agent can use, so it gets the change right the first time. Three quick steps:
>
> 1. Connect Devplan
> 2. Check your workspace and company context
> 3. Try it on the code in front of you

1. **Connect Devplan:** step 1 below, with the terminal connect steps.
2. **Check your workspace and company context:** step 2's summary in two or three lines, then step 3's company-context check. Skip the Daily Radar focus question.
3. **Try it on the code in front of you:** find the repository in the working directory (its git remote or folder name) and match it to `list_repository_descriptions`. Name its busiest product area from the feature catalog, then end with one exact message to try first, for example: "Try this: *What should I know before changing <that area>?*" If the folder isn't a connected repository, say which repos Devplan knows and suggest a question about one of them. Then list, in three lines, what else works here: "Write a spec for <feature>" (estimated from your team's git history and saved to Devplan), "Why did we build <thing> this way?", and "Who knows <service> best?".

Don't build dashboards or offer scheduling here. Close with one line: "Dashboards are available any time: say 'Build my Daily Radar' (or Execution Monitoring, Demand Report, Engineering Analytics) and I'll write it to `devplan/`." Build one only when asked, following that dashboard's skill.

## Step 1 of 5: Connect Devplan

Check whether the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.

**Connected:** call `list_workspace_projects` with a small limit. If it answers, say "You're connected to Devplan." and go to step 2. If it fails with a sign-in error, treat Devplan as not connected.

**Not connected:** ask "Do you have a Devplan account?" with options **Yes, connect it**, **No, create one**, **What is Devplan?**

- **What is Devplan?** Answer in four lines, then ask again:
  > Devplan connects to your code, tickets, Slack, docs, calls, and support, and keeps a live map of your product: what exists, what's shipping, what customers are asking for, and what was decided.
  > It links every PR, ticket, conversation, and customer request to the people, projects, and features it belongs to, across all your tools.
  > Your agents, Slack and your team work from the same map.
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

Connect steps, by surface. Give only the ones for the surface you're on, word for word. Never suggest other commands, and never send the user to the Devplan website to connect: signing in there doesn't connect this app.

- **Claude (web and desktop):** "Open **Plugins** in the sidebar, then **Devplan**, and click **Connect**. Claude shows a connector form: keep the defaults, click **Add**, then sign in to Devplan."
- **Claude Code:** if a sign-in link appears in the chat, open it and sign in. Otherwise: "Run `/mcp`, choose **plugin:devplan:devplan**, and sign in. If it isn't listed, start a new Claude Code session first."
- **Codex CLI:** "In a separate terminal, run `codex mcp add devplan --url https://app.devplan.com/api/v1/mcp` and sign in to Devplan in the browser that opens. Then start a new Codex session and say 'Set up Devplan'."
- **ChatGPT:** "Open **Plugins**, then **Devplan**, and connect. If Devplan isn't listed, add a custom MCP server with the URL `https://app.devplan.com/api/v1/mcp`."

Then add one line: "Claude may ask before each Devplan tool it uses. Devplan's read tools only read your workspace, so you can choose **Always allow** for them." (Adapt "Claude" to the app you're in.)

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
| Execution Monitoring | Projects, tickets, or code activity |
| Demand Report | Customer evidence: support tickets, calls, customer Slack, or requests |
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

**Then personalize the Daily Radar.** If you already know the user's role and focus areas from memory or earlier conversations, confirm them in one line. Otherwise ask once: "Which areas should your Daily Radar focus on?" Offer up to three focus areas drawn from what step 2 found (the busiest product areas from the feature catalog, or teams from the company context, for example **Billing and payments**, **Mobile app**, **Customer onboarding**), plus **Everything**, and let them pick several or type their own. Don't ask for project names. Keep the answer as the radar focus areas for step 4.

## Step 4 of 5: Build your dashboards and schedule updates

**Confirm once.** Name what you'll build and when it refreshes:

> Your workspace supports 4 dashboards: Daily Radar, Execution Monitoring, Demand Report, and Engineering Analytics. I'll build them now (a few minutes) and refresh them every weekday at 7:47 AM and 12:47 PM your time. You'll get a short summary when something changed, and nothing when it didn't.

Options: **Build and schedule**, **Pick different times**, **Build without scheduling**. Only list dashboards step 2 found ready; mention the rest will be added once their sources are connected.

**In Claude Code and Codex CLI, this step only runs when the user asks for dashboards** (see "In a terminal" above). Don't offer scheduling there: their schedulers can't use this app's Devplan sign-in. Build what was asked and say "To refresh, say 'Refresh my Devplan dashboards' any time."

**Build them one at a time,** in this order: Daily Radar, Execution Monitoring, Demand Report, Engineering Analytics. For each:

- Say "Building 2 of 4: Execution Monitoring".
- Follow that dashboard's skill, using the company context, the radar focus areas, and the settings gathered so far.
- Publish it as that skill's Publish section says. In Claude, each is its own artifact; keep its link. In ChatGPT, each is a tab in the one "Devplan" Site; keep the Site's link.
- If one fails or has too little data, give it its empty state, say so in one line, and continue. Never let one dashboard stop setup.

### Schedule: Claude

If you have a scheduling tool in this session, create **one** recurring scheduled task that runs at both times on weekdays in the user's time zone (for example `CRON_TZ=<zone> 47 7,12 * * 1-5`), with email notifications on (and push if they want it). If the tool lets you choose which connectors the task gets, attach only Devplan. Each run starts fresh with no memory of this chat, so write its prompt as a complete standalone instruction:

```
Refresh my Devplan dashboards. Use the Devplan plugin skills.

1. Rebuild each dashboard below with its skill. Read the existing artifact at its link first, then update it in place instead of creating a new one:
   - Daily Radar (daily-radar): <link>
   - Execution Monitoring (execution-monitoring): <link>
   - Demand Report (demand-report): <link>
   - Engineering Analytics (eng-analytics): <link>
2. Daily Radar is for <name> (<email>), <role>. Focus areas: <radar focus areas>.
3. Time zone: <IANA zone>. In each footer, the refresh line is "Refreshes weekdays at 7:47 and 12:47". In each masthead, "Last refreshed" is the time this run finished.
4. Use only Devplan and the web. Don't use other connectors or tools.
5. When fetching a long spec or project, use `contentMode: "evidence"` rather than full content.
6. If a dashboard's content is the same as the live version, leave that artifact alone.
7. If Devplan isn't connected, change nothing and reply only: "Your Devplan dashboards didn't refresh because Devplan isn't connected. Say 'Set up Devplan' to reconnect."
8. If nothing changed on any dashboard, reply only: "No changes since the last refresh."
9. Otherwise finish with an email-ready summary: up to three things that changed and matter most, one short line each, then a link to every dashboard. This final message is the email.
```

Then tell the user in two or three sentences: it's scheduled, at what times, that the summary goes to their account's email only when something changed, whether runs need their approval, what the task can access (name the connectors and tools it was given, if the tool reports them), and where to change it. If no scheduling tool is available, say scheduled refresh isn't available here and suggest saying "Refresh my Devplan dashboards" each morning.

### Schedule: ChatGPT

Use ChatGPT's scheduled tasks to create **one** recurring task at both times on weekdays in the user's time zone, with Devplan as its only connector where you can choose. Write its prompt as a complete standalone instruction:

```
Refresh my Devplan dashboards in my "Devplan" Site: <site link>. Use the Devplan plugin skills and only the Devplan connector and the web.

1. Rebuild each tab with its skill, in this order: Daily Radar (daily-radar), Execution Monitoring (execution-monitoring), Demand Report (demand-report), Engineering Analytics (eng-analytics). Update the existing Site in place; never create a new Site.
2. Daily Radar is for <name> (<email>), <role>. Focus areas: <radar focus areas>.
3. Time zone: <IANA zone>. The footer's refresh line is "Refreshes weekdays at 7:47 and 12:47". The masthead's "Last refreshed" is the time this run finished, so it always shows the last successful refresh.
4. Build the whole page and check it before publishing. Publish one new version only if it's complete; if anything fails, publish nothing, so the previous version stays live.
5. If no tab changed since the live version, don't publish and reply only: "No changes since the last refresh."
6. If the refresh fails (Devplan not connected, a tool error, or the Site can't be published), reply only: "Your Devplan dashboards didn't refresh: <one-line reason>. The version from <last refreshed time> is still live. Say 'Set up Devplan' to fix it." Send this as a notification.
7. If Sites isn't available, write the same page to devplan/devplan.html instead and say so in one line.
8. Otherwise finish with up to three things that changed and matter most, one short line each, and the Site link.
```

Then tell the user in two sentences: it's scheduled, at what times, that they only hear from it when something changed or a refresh failed, and where to change it. If the app has no scheduler here, say so and suggest "Refresh my Devplan dashboards".

If `save_workspace_context` is available, save the dashboard links (or the Site link), schedule, and time zone in the workspace settings.

## Step 5 of 5: A quick tour

Finish with a short recap of what's set up (dashboards with links, refresh time), then what they can do now:

- **Act from a dashboard.** Buttons like "Write spec", "Draft message", and "Draft nudge" copy a ready message. Paste it into your chat and I'll take it from there. Evidence sits behind each item's "Evidence" link.
- **Ask any product or technical question.** Devplan context sits behind every answer, so ask the way you'd ask a teammate who's read everything. Answers cite the PRs, tickets, calls, and decisions behind them.
  - Product: "What did we decide about pricing, and why?", "Which customers asked for SSO, and what did we tell them?"
  - Technical: "What should I know before changing billing?", "Which services touch auth, and who knows them best?", "Why did we build webhooks this way?"
  - Planning: "How long would SCIM take us?", "What's actually blocking the mobile release?"
- **Ask in Slack.** Mention Devplan in a channel and get the answer with its sources. If Slack isn't connected in Devplan yet, add it under Integrations.
- **Decisions don't get lost.** Devplan captures decisions from Slack, meetings, and specs with their reasoning, so the team stops reopening settled questions.
- **Plan a cycle.** "Plan the next 6 weeks" sizes what the team can do from how it actually ships, offers a few strategic directions, and lays out what fits.
- **Specs are tracked in Devplan.** A spec written here is saved to its Devplan project, and the PRs, tickets, and conversations that touch it link to it as they happen.

Then one subtle team line, once: "Devplan works best when your team shares it: everyone gets the same context, dashboards, and decision history. [Invite teammates](<members page>)." Build the members link as described in `devplan-product-context`.

End with one concrete thing to try first, written as the exact message to send, built from what you saw in step 2. Prefer a technical or product question about their busiest area, for example: "Try this first: *What should I know before changing <busiest product area>?*" If the Demand Report has a strong theme, offer that instead: "*Write a spec for <top suggested project>*".
