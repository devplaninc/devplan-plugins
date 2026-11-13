---
name: stale-commitments
description: Find product and engineering commitments, promises, and target dates that went quiet, slipped, remain unfinished, or became blocked, and name who needs to act. Use for "stale commitments", "what slipped", "overdue", "what went quiet", "follow-through", "missed dates", "what did we promise", or "what needs a decision".
---

# Stale Commitments

Promises the team made that are slipping. Read-only: never update work or contact owners unless the user asks after seeing the results.

## How this runs

Open with one friendly line and the plan:

> 1. Find commitments and dates
> 2. Check where each one stands
> 3. Build the list

Start each step with a short progress line ("Step 2 of 3: ..."). Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan connected, then follow `devplan-setup` from step 1. Stop this skill there.
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Scope

Default: commitments made or reaffirmed in the last 60 days. A start date bounds when a commitment was made or reaffirmed, not when an old record was last touched.

## 2. Find commitments

Use `list_workspace_projects`, `query_workspace_graph`, and `search_entities`:

- Projects and stories with due dates that passed or fall within 7 days.
- Explicit commitments in discussion topics, meeting notes, and call notes: "we'll ship by", "I'll follow up", "ETA", "by Friday", promised follow-ups to customers.
- Delay and misalignment risk insights.

Connect each commitment to its project, linked PRs and tickets, risks, and latest activity.

## 3. Judge

- **Slipped** (`s-bad`): the date passed and the work isn't done.
- **Blocked** (`s-bad`): marked blocked, or waiting on a named dependency.
- **Quiet** (`s-warn`): no update, PR, or discussion for 7+ days on something still open.
- **At risk** (`s-warn`): due within 7 days with evidence it won't make it.

Exclude commitments that were explicitly dismissed, superseded, or descoped. Rank customer promises, cross-team dependencies, and dated project goals above internal chores.

## 4. Dashboard

Title: "Stale Commitments".

1. **Today:** the three commitments that most need a decision.
2. **Figures:** slipped, blocked, quiet, customer promises at risk.
3. **Decide now:** rows needing a decision, each with the owner and the specific decision (recommit, re-date, descope, or unblock).
4. **Slipped**, **Blocked**, **Quiet**, **At risk:** rows with what was promised, by whom, when, the original date, current state with evidence, and days overdue or idle.
5. **Customer promises:** any of the above made to a customer.

Every item links to the commitment's source and its current state.

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
