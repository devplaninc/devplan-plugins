---
name: demand-report
description: Demand Report: customer demand themes with the projects that answer them, isolated asks, adoption blockers, customer promises, and the last two weeks of competitor and market moves. Use for "demand report", "customer requests", "what are customers asking for", "feature requests", "voice of customer", "what should we build next", "suggested projects", "what did we promise customers", or "what are competitors doing".
---

# Demand Report

What customers need, what we promised them, what the market is doing, and what to do about it. Read-only: never reply to tickets, post in Slack, or create projects unless the user asks.

## How this runs

Open with one friendly line and the plan:

> 1. Load Devplan's suggested projects, customer evidence, and promises
> 2. Check the last two weeks of market and competitor moves
> 3. Find the demand themes and the projects that answer them
> 4. Build your Demand Report

Start each step with a short progress line ("Step 2 of 4: ..."). Ask at most one question, only when the answer changes the result. Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan, then ask setup's first question, "Do you have a Devplan account?", with its three options (**Yes, connect it**, **No, create one**, **What is Devplan?**), and follow `devplan-setup` from step 1. Stop this skill there. Don't give connect steps or commands of your own, and don't offer to do the task without Devplan (no local drafts, notes-based plans, or git summaries).
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Scope

Default: customer evidence from the last 90 days, all customers. Market and competitor items: a rolling 2 weeks, always. Honor any window, account, segment, or product area the user gives. Older evidence can corroborate a recent theme. Weight everything by the company goals in the company context.

## 2. Devplan suggested projects (the starting point)

Devplan already turns customer requests into suggested projects. They are the input for the themes, so start here:

1. Page through `list_workspace_projects` with `status: "DRAFT"`, then `"IN_REVIEW"`, following `nextCursor` until it's gone (pages are small).
2. Keep the projects Devplan suggested from customer demand: their description names a person at an account ("Jane Doe at Acme needs...", "Acme's Jane Doe wants..."), usually with no owner. Skip internal work, inferred workstreams (multi-bullet descriptions with an engineer owner), and labelled QA or test projects.
3. For each, keep: title, account(s), requester, status, link, and created date.
4. Add feature-request insights from the graph (`MATCH (i:Insight {kind:'feature_request'})`) that have no matching suggested project; fetch them in `evidence` mode for the accounts behind them.

## 3. Customer evidence

Use customer evidence to corroborate and size what step 2 found, not to replace it. Use `search_entities` across `insight`, `customer_support_ticket`, `call_note`, `discussion_topic`, and `signal`, and `query_workspace_graph` for feature-request insights with their status, business impact, and supporting signals. Devplan has already deduplicated evidence and matched customers across tools.

If a search filtered by date comes back empty, search again without the date filter and filter by each result's source date yourself. Some sources aren't indexed by source time.

For each piece of evidence keep: account, requester, date, source, and a one-line paraphrase.

Then check the existing projects for each candidate theme with `list_workspace_projects`, `list_product_feature_catalog`, and recent changes: delivered, in progress, planned, or none. Also collect the suggested projects Devplan has already generated (suggested or proposed projects in `list_workspace_projects`, and feature-request insights that carry a suggested project) so they can sit under the theme they answer.

**Customer promises.** Find commitments made to customers in the last 60 days: in call notes, support tickets, customer Slack channels, and emails Devplan has ("we'll ship by", "ETA", "I'll follow up", "on the roadmap for Q1"). For each: account, who promised it, when, what, the date promised if any, and the linked project or ticket. Judge it: **Delivered** (`s-ok`), **On track** (`s-info`), **At risk** (`s-warn`: due within 7 days with evidence it won't make it), **Slipped** (`s-bad`: the date passed and it isn't done), **Blocked** (`s-bad`). Leave out promises that were explicitly withdrawn or superseded.

## 4. Market and competitors

Use web search. Keep it to about six searches.

- **Competitors:** for each competitor in the company context (top 3 to 5), search for launches, pricing changes, and announcements in the last 2 weeks. Prefer the competitor's own changelog, blog, and docs.
- **Market trends:** two or three searches on the company's category and its target customers' buying criteria (for example "mid-market analytics buyers SSO requirement 2026").

Keep only items dated within the last 2 weeks with a source you can link. Market evidence changes the weight of a theme; it never creates one on its own:

- A competitor shipping what customers ask for raises urgency: mark the theme "competitive gap".
- A trend that makes a theme a buying requirement raises it.
- Market items that match no customer demand go in the market section only.

## 5. Themes

1. **Group the suggested projects into themes.** A theme is a product capability or adoption problem that two or more suggested projects (or insights) address. Every suggested project lands in exactly one theme or in Isolated asks; never drop one. Aim for 4 to 8 themes; split a theme when its projects need different remedies, and merge when they're the same remedy.
2. **Name themes as specific product implications:** a capability, a workflow, or an adoption blocker. Broad aspirations ("single source of truth") are context, not themes.
3. **Keep themes stable between runs.** If a Demand Report already exists (setup saves the link), read it first and reuse its theme names and grouping for projects that haven't changed. Only add, split, or retire a theme when new suggested projects or evidence require it, and say what changed in one line in chat.
4. **Count accounts strictly.** An account counts once per theme, across all its suggested projects and corroborating evidence. A theme needs two or more independent accounts; anything with one account is an isolated ask.
5. **Adoption blockers need proof** that the issue blocked approval, adoption, or reliance, not just a wish.
6. **Rank** by independent accounts, then recency of the newest ask, then goal fit and market pressure.

## 6. Projects under each theme

For each theme, list:

1. **Existing projects:** planned projects in Devplan, Linear, or Jira that already answer the theme (an owner, a spec, or a status past draft): name, state, link.
2. **Devplan suggested projects:** every suggested project grouped into this theme, with its account. These are the theme's backbone.
3. **New suggestions:** only where nothing above covers part of the theme, at most one small project: title, the problem in one sentence, rough scope (S, M, or L), and the main risk.

## 7. Dashboard

Title: "Demand Report". Scope line: accounts and sources covered. No summary and no figures; start straight with the themes.

1. **Themes:** one group per theme, ranked. The parent row: theme name, type, accounts and mentions, status as its state (`s-bad` no tracked work, `s-warn` partial or planned, `s-ok` delivered), "Competitive gap" in the side line when it applies, and evidence. Child rows under the label "Existing projects" (with link and state), then "Devplan suggested projects" (each with its account, a link to the suggested project, and a **Write spec** button), then any new suggestion. A theme already covered by existing projects gets **Draft customer update** instead, to tell the asking accounts where it stands.
2. **Isolated asks:** suggested projects and requests from a single account that fit no theme, each with **Draft reply** (to the requester, acknowledging the ask and where it stands) or **Write spec** when it's clearly worth building.
3. **Adoption blockers:** rows with the proof they blocked approval or adoption, each with **Write spec** for the fix, or **Draft message** to the account owner when the fix already exists.
4. **Customer promises:** rows ordered slipped, blocked, at risk, on track, then delivered: what was promised, to which account, by whom, when, the date promised, current state with evidence, and days overdue. Slipped and at-risk rows get **Draft follow-up** (to the customer, with an honest update) and, when an internal decision is needed, **Draft nudge** to the owner. Delivered rows get **Draft follow-up** to tell the customer it's live.
5. **Market and competitors (last 2 weeks):** dated entries with search and chips for "Competitor" and "Trend", each with its source behind the Evidence link and a state pill: "Gap" (`s-bad`), "Partial" (`s-warn`), "Context" (`s-info`). Gaps get **Write spec** or **Investigate**.

Button prompts (`data-prompt`) must start the task on their own:

- **Write spec:** `Write a Devplan spec for "<project title>". It comes from the "<theme>" theme in my Demand Report: <N> accounts asking, including <2 or 3 account names>. Key evidence: <2 or 3 readable sources>.`
- **Draft reply / Draft follow-up / Draft customer update:** `Draft a short, honest message to <contact> at <account> about "<ask or promise>". Where it stands: <state and date>. Context: <2 or 3 readable sources>. Don't promise dates we haven't committed to.`
- **Draft nudge / Draft message:** `Draft a short Slack message to <owner> about "<item>": <what's at stake for <account>>. Ask what they need to <recommit, re-date, or unblock> it.`

Empty states: no customer evidence means "Connect a support tool, call recorder, or customer Slack channel in Devplan"; no competitors in the company context means a button that prompts `Add our top competitors to my Devplan company context.`

In chat, after publishing, offer: "Want me to write a spec for one of these, or draft the customer follow-ups?" For a spec, follow the `spec` skill.

<!-- shared:dashboard-format -->
## Dashboard format

Build the page from [references/dashboard-template.md](references/dashboard-template.md). Don't write your own layout, CSS, or script.

1. Copy the template's `<head>`, `<style>` and `<script>` exactly. Change only the `<title>`.
2. Fill the masthead: workspace name, page title, window, scope, and "Last refreshed" with the time this run finished.
3. Use only the template's patterns: Summary, Figures, Rows, Groups, Folds, Dated entries, Table, Trend, Meter, Timeline, Tabs, and Empty. Use Summary and Figures only where this skill asks for them. Delete every pattern you don't use and every template comment. Never leave `{{...}}` placeholders.
4. **Be concise.** Summary bullets are one short line each, with no links. Row text is one or two short sentences. Cut anything the reader can't act on or doesn't need to know.
5. Use the same four states everywhere, as a class on the row and on its pill: `s-ok` (shipped, delivered, on track), `s-warn` (partial, at risk), `s-bad` (blocked, slipped, off track, no tracked work), `s-info` (new, neutral, suggested).
6. **Evidence** always uses the template's evidence toggle: a `details.ev` whose summary reads "Evidence · N" (N = number of pills), closed by default, holding `.src` pills. Each pill: the tool in `<i>` (GitHub, Linear, Jira, Slack, Gong, Zendesk, Notion, Devplan, Web), then a readable title: the PR's title, the ticket's title, #channel and topic, the call title and date, the ticket subject. No PR numbers or opaque IDs. The graph doesn't store PR titles: take the title from the Change that used the PR (its summary, or the commit message from `fetch_internal_entities_by_ids` in `evidence` mode, without the trailing "(#123)"). If a PR has no Change yet, label it "<repo> · <author> · opened <date>". Link every pill to its source: the PR, or `https://github.com/<repo>/commit/<sha>` when a Change gives only commits.
7. **Actions.** Any finding, decision, risk, ask, or item that needs someone to do something gets a button that copies a ready prompt: Write spec, Update spec, Draft message, Draft reply, Draft nudge, Prep review, Re-plan, Investigate. Put the exact message in `data-prompt`, written so it starts the right skill or task on its own and names the item and 2 or 3 readable sources (for example `Write a Devplan spec for &quot;SCIM provisioning&quot;...` or `Draft a Slack message to Ali asking whether &quot;Webhook retries&quot; still lands Friday. Context: ...`). Escape quotes as `&quot;`. One or two buttons per item, never more.
8. **Empty states.** Never drop an empty section or leave it blank. Keep its heading and use the Empty pattern: one sentence on why it's empty and the one fix. If a source is missing, name it and link "Connect <source>" to https://app.devplan.com (Integrations). If the window is too narrow or the data is just quiet, say so and add a button with a prompt that widens it or tries the next useful thing. If the whole page has nothing, show the notice and one Empty section with the fix.
9. Escape `&`, `<` and `>` in text from sources. Links are absolute `https://` URLs; the template's script opens them in a new tab, so don't add your own `target`.
10. Footer: set the refresh line from the scheduled task ("weekdays at 7:47 and 12:47"), or "Run it again any time" if there is none. Point "Invite teammates" at the workspace members page (see `devplan-product-context`).

Before publishing, check once that every element you opened is closed, in order, and every `li` sits inside a `ul`. On every refresh, rebuild the whole page from the template rather than patching the old HTML.

## Publish

- **Claude:** publish an HTML artifact with this dashboard's name as its title. If one exists from an earlier run (setup saves the links), update that artifact instead of creating another. If your artifact tool adds its own page wrapper, publish what's inside `<head>` and `<body>` without the wrapper tags.
- **ChatGPT, or the Codex app, with Sites:** every report lives in one Site named "Devplan", one tab per report (the Tabs pattern, each report's sections inside its own tab panel, in this order: Daily Radar, Execution Monitoring, Demand Report, Engineering Analytics). Update only this report's tab and keep the others exactly as they are. If the Site doesn't exist yet, create it with this tab. Publish a new version only once the whole page is built and checked, so the last good version stays live if anything fails. Skip publishing when nothing in the report changed since the live version.
- **Sites unavailable, Claude Code, or Codex CLI:** write the complete page, from `<!doctype html>` through `</html>` with its `<head>`, to the working directory and give the path. In ChatGPT and Codex, that's the combined tabbed page at `devplan/devplan.html`; in Claude Code, `devplan/devplan-<skill-name>.html`. Replace the previous copy only once the new one is complete. The first time you create the `devplan/` folder inside a git repository, suggest adding `devplan/` to `.gitignore`; don't edit it yourself.
- **In chat**, after publishing: two or three lines with the most important finding and one suggested next step. Don't repeat the dashboard.
<!-- /shared:dashboard-format -->
