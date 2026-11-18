---
name: cycle-planning
description: Plan a cycle, sprint, or quarter sized from the team's real pace: asks timeframe and team size, offers a few strategic directions, then lays out what fits, what's stretch, and what waits. Use for "plan the next cycle", "sprint planning", "quarter planning", "what can we get done in 6 weeks", "capacity planning", or "build a roadmap for next quarter".
---

# Cycle Planning

Turn "what should we do next cycle?" into a plan the team can commit to, sized from how this team actually ships. Read-only until the user asks to change anything in Devplan.

## How this runs

Open with one friendly line and the plan:

> 1. Set the cycle: timeframe and team
> 2. Gather what's in flight, what's planned, and what Devplan suggests
> 3. Size what the team can do
> 4. Pick a strategic direction
> 5. Build your cycle plan

Start each step with a short progress line ("Step 2 of 5: ..."). Ask one question at a time, with 2 to 4 short options, using the client's question tool if there is one. Don't ask for anything the context already answers. Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan, then ask setup's first question, "Do you have a Devplan account?", with its three options (**Yes, connect it**, **No, create one**, **What is Devplan?**), and follow `devplan-setup` from step 1. Stop this skill there. Don't give connect steps or commands of your own, and don't offer to do the task without Devplan (no local drafts, notes-based plans, or git summaries).
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Set the cycle

Ask only what you don't already know, one question at a time:

1. **Timeframe.** "What are you planning for?" Options: **The next 2-week cycle**, **The next 6 weeks**, **This quarter**, **Custom dates**. Work out the start and end dates and the number of working weeks.
   - **Cycles inside it.** If the timeframe is longer than one cycle, split it into cycles. Use the team's cycle or sprint length from Linear or Jira if Devplan shows one; otherwise ask once: "How long are your cycles?" (**1 week**, **2 weeks**, **6 weeks**). A single-cycle plan has one cycle; a quarter of 2-week cycles has six.
2. **Engineers.** "How many engineers are working on it?" Offer the count Devplan sees as active in the last 30 days as the first option ("8, the engineers active in the last month"), plus **Fewer**, **More**. Then ask once whether anyone is out for part of the cycle, if it matters.
3. **Scope** (only if the workspace has several teams or product areas): "Whole product or one team?" with the teams or areas from the company context.

## 2. Gather

Quietly collect, using `list_workspace_projects`, `query_workspace_graph`, `search_entities`, `list_product_feature_catalog`, and `list_repository_descriptions`:

- **Strategy and goals:** company goals and context from `devplan-product-context`, plus strategy, roadmap, or OKR documents in Devplan. If the user has other connected sources with a strategy or planning doc (Notion, Confluence, Google Drive), read the most recent one. Use what you know about the user from memory too.
- **In progress:** active projects with their status, completion, owner, due date, and recent activity. These come first: unfinished work is the cheapest value.
- **Planned:** projects in Devplan's Now and Next roadmap sections, and ready-for-dev projects with specs and estimates.
- **Devplan's priorities:** feature-request insights ranked by business impact and accounts asking, active high-severity risks, suggested and inferred projects, and the top themes from the latest Demand Report if there is one.
- **Commitments:** dated promises, especially to customers, that land inside the cycle.

## 3. Size capacity and effort

Follow "How to estimate" below for the team's pace and each candidate's PRs.

- **Unplanned work:** the share of merged changes not linked to any project (support, bugs, interrupts). Reserve that share of capacity. If it can't be measured, reserve 25%.
- **Capacity** in engineer-weeks = engineers × working weeks × (1 − unplanned share), minus known time off. Then hold back a **20% buffer** of that and plan only the other 80%. Show the buffer explicitly everywhere capacity appears ("Buffer 20% · 7 eng-weeks"). Capacity in PRs = planned capacity × PRs per engineer-week. Do the same per cycle.
- **Each candidate:** PRs required (low-high), converted to engineer-weeks. For in-progress work, only the PRs still to go. Where a spec already has an estimate, compare it with the PR-based one and use the PR-based one unless the spec explains the difference.

If a candidate can't be sized, say so and give it a wide range.

<!-- shared:estimating -->
## How to estimate

Estimate from the team's git history in Devplan, not from ideal hours. Use the last 90 days and leave bots out (authors ending in `[bot]`, dependabot, renovate). Timestamps are epoch milliseconds; write the computed number in place of `$since`.

1. **Team pace from git.**
   ```
   MATCH (a:Person)-[:AUTHORED]->(pr:PullRequest)
   WHERE pr.mergedAt >= $since AND NOT coalesce(a.name,'') ENDS WITH '[bot]'
   RETURN count(DISTINCT a) AS engineers, count(DISTINCT pr) AS prs,
     percentileCont((pr.mergedAt - pr.openedAt)/3600000.0, 0.5) AS p50_hours,
     percentileCont((pr.mergedAt - pr.openedAt)/3600000.0, 0.85) AS p85_hours
   ```
   PRs per engineer-week = prs ÷ engineers ÷ weeks in the window.
2. **PRs per project, from comparable work.** Count the PRs behind each project's linked changes. Recent changes often link to commits rather than PRs, so count both, and convert commits to PRs with the workspace's ratio of merged PRs to commits over the same window (close to 1 when the team squash-merges).
   ```
   MATCH (c:Change)-[:LINKED_TO]->(p:Project) WHERE c.periodEnd >= $since
   MATCH (c)-[:USED]->(x) WHERE x:PullRequest OR x:GitCommit
   RETURN p.projectId,
     count(DISTINCT CASE WHEN x:PullRequest THEN x END) AS prs,
     count(DISTINCT CASE WHEN x:GitCommit THEN x END) AS commits
   ORDER BY prs + commits DESC LIMIT 50
   ```
   Join project IDs to `list_workspace_projects` for titles. Pick the 2 or 3 projects closest in area and scope as comparables.
3. **PRs this work needs.** Break the scope into pieces (from the technical approach, or the project's description), estimate PRs for each piece from the comparables, and add them up as a low-high range. For work already in progress, subtract the PRs already linked to it.
4. **Convert to time.**
   - Effort in engineer-weeks = PRs ÷ PRs per engineer-week.
   - Calendar time = the larger of (effort ÷ engineers on it) and (the longest chain of PRs that must land one after another × p85 cycle time).
   - Plan on the low PR count and median pace. Use the high PR count and p85 cycle time as the risk case.
5. **Show the basis in one line,** in this shape, with this workspace's numbers: "Based on N PRs from M engineers over 90 days (X PRs per engineer-week; cycle time A hours median, B hours at p85). Comparable projects took C to D PRs." Never reuse numbers from this example.

Never invent precision. With no comparable project, give a wide range and say what would narrow it.
<!-- /shared:estimating -->

## 4. Pick a strategic direction

Before building the plan, offer 3 directions that genuinely differ in what they optimize. Shape them from the evidence, for example:

- **Finish what's in flight:** land in-progress work and commitments first, few new starts.
- **Customer demand:** the strongest demand themes and competitive gaps.
- **A company goal:** one goal from the company context, pursued hard.
- **Reliability and speed:** risks, quality, and the things slowing delivery down.

For each direction show, in 3 lines: what it prioritizes, the top 3 items it would include, and what it gives up. Recommend one, with one sentence on why. Ask "Which direction?" with the three as options, plus **Mix them**. If they mix, ask which two and in what order.

## 5. Build the plan

Fit work into capacity in this order: commitments inside the window, then in-progress work for the chosen direction, then new work by the direction's ranking. Stop at the 80% line. With several cycles, fill them in order and place each item in the cycle where it starts; an item may span cycles. Give each cycle one primary theme and one goal (a measurable outcome) that follow from what's in it. The next items that would fit at the median but not the 85th percentile are **Stretch**. Everything else waits, with a reason.

For each planned item: owner (from who's working in that area; leave blank rather than guess), its estimate (PRs and engineer-weeks as ranges, plus calendar weeks), its start and end week, why it's in (direction, goal, evidence), dependencies, and the main risk. Flag any engineer who would be on more than two items at once.

## 6. Cycle plan

Title: "Cycle Plan". Masthead window: the planning dates and working weeks; scope: engineers, team, and number of cycles. No figures.

1. **Summary** (Summary pattern, no links): one bullet per cycle, in this shape: "**Cycle 1 · Nov 24–Dec 5: <theme>.** Goal: <outcome>. Projects: <A>, <B>, <C>." Then one bullet with the direction and the capacity line: "<N> eng-weeks capacity, 80% planned, 20% buffer held back."
2. **Timeline** (Timeline pattern), right under the summary: one week column per working week, a Cycles row naming each cycle and its theme, one bar per committed item from its start to end week (color by the cycle it starts in), stretch items hatched, and a "Buffer (20%)" row. Each bar's `title` gives the item and its estimate.
3. **Capacity** (Meter): in progress, new work, stretch, and the 20% buffer, as shares of total capacity. The caption says "80% planned · 20% buffer".
4. **Committed:** one Fold per planned item, closed by default, ordered by start week. The summary row: title linked to the Devplan project if there is one, cycle, owner, and the estimate in the side column ("Est. 3–4 eng-weeks · 8–11 PRs"). The body: why it's in, start and end week, dependencies and risks as child rows, evidence, and a **Write spec** button for items without a spec.
5. **Stretch:** rows, each with its estimate and what would need to go right.
6. **Not this time:** rows with the reason (capacity, direction, not ready, blocked).
7. **How this was sized** (table): engineers, working weeks, cycles, unplanned share, buffer (20%), PRs per engineer-week, cycle time (median and p85), capacity in PRs, and the comparable projects with their PR counts.
8. **Assumptions and risks:** rows for the assumptions that would change the plan most, each with an **Investigate** button where checking it would help.

The **Write spec** button's `data-prompt`:

```
Write a Devplan spec for "<item>". It's planned for <cycle name and dates> in my cycle plan (<direction>), estimated at <effort range>. Key evidence: <2 or 3 readable sources>.
```

In the footer, use "Run it again any time" for the refresh line.

After publishing, offer one next step: "Want me to move the committed projects into Now on your Devplan roadmap?" Only if the user says yes, use `update_project` with `action: "assign_roadmap_section"`, one project at a time.

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
9. Escape `&`, `<` and `>` in text from sources.
10. Footer: set the refresh line from the scheduled task ("weekdays at 7:47 and 12:47"), or "Run it again any time" if there is none. Point "Invite teammates" at the workspace members page (see `devplan-product-context`).

Before publishing, check once that every element you opened is closed, in order, and every `li` sits inside a `ul`. On every refresh, rebuild the whole page from the template rather than patching the old HTML.

## Publish

- **Claude:** publish an HTML artifact with this dashboard's name as its title. If one exists from an earlier run (setup saves the links), update that artifact instead of creating another. If your artifact tool adds its own page wrapper, publish what's inside `<head>` and `<body>` without the wrapper tags.
- **ChatGPT, or the Codex app, with Sites:** every report lives in one Site named "Devplan", one tab per report (the Tabs pattern, each report's sections inside its own tab panel, in this order: Daily Radar, Execution Monitoring, Demand Report, Engineering Analytics). Update only this report's tab and keep the others exactly as they are. If the Site doesn't exist yet, create it with this tab. Publish a new version only once the whole page is built and checked, so the last good version stays live if anything fails. Skip publishing when nothing in the report changed since the live version.
- **Sites unavailable, Claude Code, or Codex CLI:** write the complete page, from `<!doctype html>` through `</html>` with its `<head>`, to the working directory and give the path. In ChatGPT and Codex, that's the combined tabbed page at `devplan/devplan.html`; in Claude Code, `devplan/devplan-<skill-name>.html`. Replace the previous copy only once the new one is complete. The first time you create the `devplan/` folder inside a git repository, suggest adding `devplan/` to `.gitignore`; don't edit it yourself.
- **In chat**, after publishing: two or three lines with the most important finding and one suggested next step. Don't repeat the dashboard.
<!-- /shared:dashboard-format -->
