---
name: eng-analytics
description: Build an Engineering Analytics dashboard of cycle time, PR throughput, work in progress, review load, and planned versus unplanned work, by team, repo, and project. Use for "engineering metrics", "cycle time", "how fast are we shipping", "throughput", "review bottlenecks", "team productivity", or "DORA".
---

# Engineering Analytics

How the engineering system is flowing. Read-only. Report team and system metrics. Don't rank individual engineers unless the user explicitly asks, and even then show context alongside the numbers.

## How this runs

Open with one friendly line and the plan:

> 1. Pull PRs and tickets
> 2. Work out the metrics
> 3. Build your dashboard

Start each step with a short progress line ("Step 2 of 3: ..."). Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan connected, then follow `devplan-setup` from step 1. Stop this skill there.
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Window

Default: the last 30 days, compared with the 30 before, plus 8 weeks of weekly trend. Honor any window, team, or repo the user gives.

## 2. Data

Use `query_workspace_graph`. Timestamps are epoch milliseconds; write computed numbers into the query.

- Pull requests: `openedAt`, `mergedAt`, `closedAt`, `status`, `isDraft`, `repo`, with authors and reviewers.
- Tickets: status and creation time, for work in progress.
- Changes linked to projects (`LINKED_TO`), for planned versus unplanned work.

Devplan has already linked PRs to tickets, projects, and people, so compute by project and repo directly. Leave bot PRs out of every metric (authors ending in `[bot]`, dependabot, renovate), and say how many you excluded. Use teams from the company context when it names them.

## 3. Metrics

- **Cycle time:** PR opened to merged. Median and 85th percentile.
- **Throughput:** PRs merged per week.
- **Work in progress:** open non-draft PRs, and PRs open longer than 7 days.
- **Review load:** reviews per reviewer, and PRs merged with no recorded review.
- **Planned work:** share of merged changes linked to a project versus unplanned.
- **Review wait:** only if Devplan provides first-review times. Otherwise leave it out and say so in one line.

Add 3 findings that explain the biggest changes from the prior period, each with example PRs.

## 4. Dashboard

Title: "Engineering Analytics".

1. **Today:** the three findings, one sentence each.
2. **Figures:** median cycle time, PRs merged, open PRs, planned share, each with its change from the prior period (`up` when the change is good, `down` when it's bad).
3. **Trend:** weekly PRs merged for 8 weeks, and weekly median cycle time.
4. **By repo** (table): merged, median and p85 cycle time, open, oldest open.
5. **By project** (table): merged changes, active contributors, last activity.
6. **Findings:** rows with example PRs in the trail.
7. **Long-running PRs:** rows for PRs open longer than 7 days, with author, age, and reviewers.

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
