---
name: cycle-planning
description: Plan an engineering cycle, sprint, or quarter. Asks for the timeframe and team size, sizes capacity from the team's observed cycle time and throughput, weighs strategy, goals, Devplan's suggested priorities, and planned and in-progress work, offers a few strategic directions to choose from, then publishes a cycle plan of what fits, what's stretch, and what waits. Use for "plan the next cycle", "sprint planning", "quarter planning", "what can we get done in 6 weeks", "capacity planning", or "build a roadmap for next quarter".
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
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan connected, then follow `devplan-setup` from step 1. Stop this skill there.
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Set the cycle

Ask only what you don't already know, one question at a time:

1. **Timeframe.** "How long is this cycle?" Options: **2 weeks**, **6 weeks**, **This quarter**, **Custom dates**. Work out the start and end dates and the number of working weeks.
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
- **Capacity** in engineer-weeks = engineers × working weeks × (1 − unplanned share), minus known time off. Keep about 10% as buffer on top. Capacity in PRs = that × PRs per engineer-week.
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
5. **Show the basis in one line,** for example: "Based on 410 PRs from 4 engineers over 90 days (8 PRs per engineer-week; cycle time 0.9 hours median, 41 hours at p85). Comparable projects took 28 to 40 PRs."

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

Fit work into capacity in this order: commitments inside the cycle, then in-progress work for the chosen direction, then new work by the direction's ranking. Stop at capacity. The next items that would fit at the median but not the 85th percentile are **Stretch**. Everything else waits, with a reason.

For each planned item: owner (from who's working in that area; leave blank rather than guess), PRs required and effort range, why it's in (direction, goal, evidence), dependencies, and the main risk. Flag any engineer who would be on more than two items at once.

## 6. Cycle plan

Title: "Cycle Plan". Masthead window: the cycle dates and working weeks; scope: engineers and team.

1. **The plan** (the Today pattern, labeled "The plan"): the direction and the three most important outcomes of the cycle, one sentence each.
2. **Figures:** capacity in engineer-weeks, planned, stretch, and buffer.
3. **Capacity** (Meter): in progress, new work, stretch, and buffer, as shares of capacity.
4. **Committed:** one group per planned item, ordered by sequence. Parent row: title linked to the Devplan project if there is one, why it's in, owner, effort range, and the evidence trail. Child rows: dependencies and risks. Items without a spec get a **Write spec** button.
5. **Stretch:** rows, each with what would need to go right.
6. **Not this cycle:** rows with the reason (capacity, direction, not ready, blocked).
7. **How this was sized** (table): engineers, working weeks, unplanned share, PRs per engineer-week, cycle time (median and p85), capacity in PRs, and the comparable projects with their PR counts.
8. **Assumptions and risks:** rows for the assumptions that would change the plan most.

The **Write spec** button's `data-prompt`:

```
Write a Devplan spec for "<item>". It's planned for <cycle dates> in my cycle plan (<direction>), sized at <effort range>. Key evidence: <2 or 3 readable sources>.
```

In the footer, use "Run it again any time" for the refresh line.

After publishing, offer one next step: "Want me to move the committed projects into Now on your Devplan roadmap?" Only if the user says yes, use `update_project` with `action: "assign_roadmap_section"`, one project at a time.

<!-- shared:dashboard-format -->
## Dashboard format

Build the page from [references/dashboard-template.md](references/dashboard-template.md). Don't write your own layout, CSS, or script.

1. Copy the template's `<head>`, `<style>` and `<script>` exactly. Change only the `<title>`.
2. Fill the masthead: workspace name, page title, window, scope, and when it was updated.
3. Use only the template's patterns: Today (exactly 3 lines; keep its label unless this skill names another), Figures (2 to 4), Rows, Groups, Dated entries, Table, Trend, Meter, and Empty. Delete every pattern you don't use and every template comment. Never leave `{{...}}` placeholders.
4. Use the same four states everywhere, as a class on the row and on its pill: `s-ok` (shipped, delivered, on track), `s-warn` (partial, at risk, quiet), `s-bad` (blocked, slipped, off track, no tracked work), `s-info` (new, neutral, suggested).
5. Every item links to its source. Put evidence in the row's `.trail` as `.src` chips: the tool name in `<i>`, then a readable label (PR #412, LIN-88, #channel, a call title and date, a ticket subject). Never show opaque IDs.
6. Action buttons copy a ready prompt for the user to paste into Claude. Put the exact message in `data-prompt`, written so it starts the right skill on its own (for example `Write a Devplan spec for &quot;SCIM provisioning&quot;...`). Escape quotes as `&quot;`.
7. Escape `&`, `<` and `>` in text from sources.
8. Footer: set the refresh line from the scheduled task ("weekdays at 7:47"), or "Run it again any time" if there is none. Point "Invite teammates" at the workspace members page (see `devplan-product-context`).

Before publishing, check once that every element you opened is closed, in order, and every `li` sits inside a `ul`. On every refresh, rebuild the whole page from the template rather than patching the old HTML.

## Publish

- **Claude:** publish an HTML artifact with this dashboard's name as its title. If one exists from an earlier run (setup saves the links), update that artifact instead of creating another. If your artifact tool adds its own page wrapper, publish what's inside `<head>` and `<body>` without the wrapper tags.
- **Claude Code or Codex:** write `devplan-<skill-name>.html` to the working directory, replacing the previous copy, and give the path.
- **In chat**, after publishing: two or three lines with the most important finding and one suggested next step. Don't repeat the dashboard.
<!-- /shared:dashboard-format -->
