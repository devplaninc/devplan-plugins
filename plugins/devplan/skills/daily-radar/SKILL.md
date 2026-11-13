---
name: daily-radar
description: Build a personal Daily Radar dashboard of what shipped, what's moving, what's stuck, and what needs the user's attention, tailored to their role, team, and projects. Use for "daily radar", "what happened yesterday", "team status", "standup prep", "what's blocked", "what needs my attention", or "catch me up".
---

# Daily Radar

A morning briefing for one person. Read-only: never post messages, change tickets, or comment on PRs.

## How this runs

Open with one friendly line and the plan:

> 1. Work out what matters to you
> 2. Gather the last day's activity
> 3. Build your radar

Start each step with a short progress line ("Step 2 of 3: ..."). Keep the tone plain. Ask at most one question, only when the answer changes the result. Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan connected, then follow `devplan-setup` from step 1. Stop this skill there.
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Who it's for

The radar is personal. Work out, in this order:

1. **Who they are.** From memory and earlier conversations: name, email, role, team. A scheduled run's instructions may name them and their focus; use that.
2. **What they care about.** From memory: projects they own or follow, customers they handle, people they work with, and anything they've said they want to watch. Add the radar focus saved during setup.
3. **Their footprint in Devplan.** Match their email to `list_workspace_members` and to a person in the graph. From the graph, find projects they own, PRs they authored or review, and work linked to their projects.

Use this to order and filter, not to hide: their items come first, the team's important items follow. If you know nothing about them, show the team view and end with: "Want this tailored to you? Tell me your role and what to watch."

Don't save anything new to memory.

## 2. Window

Default: the last 24 hours. On Monday, since Friday 00:00 local. Honor any window the user gives.

## 3. Gather

Use `query_workspace_graph`, `search_entities`, and `list_workspace_projects`. Devplan has already attributed activity to people and projects across every source, so don't re-derive attribution.

- **Shipped:** merged PRs and changes in the window, with their projects and features.
- **Moving:** PRs opened, tickets started, projects with new linked activity.
- **Stuck:** open PRs older than 2 days, tickets in progress with no activity for 3+ days, active risk insights, projects whose due date is close and completion is low.
- **Talk:** discussion topics and meeting notes in the window with decisions, blockers, escalations, or customer issues. Skip chatter.
- **For them:** PRs waiting on their review, their projects' new risks and slips, mentions of their projects or customers in discussions and calls.

Example graph queries. Timestamps are epoch milliseconds: compute the window start from today's date and write the number in place of `$since`.

```
MATCH (p:Person)-[:AUTHORED]->(pr:PullRequest) WHERE pr.mergedAt >= $since
RETURN p.name, pr.prId, pr.repo, pr.mergedAt ORDER BY pr.mergedAt DESC LIMIT 100

MATCH (x)-[:LINKED_TO]->(proj:Project) WHERE (x:Change OR x:Signal) AND x.periodEnd >= $since
RETURN proj.projectId, count(x) AS activity, max(x.periodEnd) AS last ORDER BY activity DESC LIMIT 50
```

Project nodes have no titles, and their graph status can lag; take titles, status, and owners from `list_workspace_projects`, joined by ID. People in the graph are often named by their git username, so match them by email or `gitUsername`, and show the name from `list_workspace_members` when you can. Leave out bots (names ending in `[bot]`, dependabot, renovate).

## 4. Dashboard

Title: "Daily Radar". Masthead scope: "For <first name>" when personalized, otherwise "Team view".

1. **Today:** the three things that matter most to this person today, one sentence each with a link.
2. **Figures:** shipped, in motion, stuck, and waiting on them (when personalized).
3. **For you** (when personalized): rows for their reviews, their projects' changes and risks, and mentions. Each says what they should do, if anything.
4. **Needs attention:** blocked, stale, and at-risk items for the team, with owner, age, and the evidence trail.
5. **Shipped:** dated entries, grouped by project or area.
6. **In motion by project:** a group per active project, with its new activity as child rows.

Every item links to its source.

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
