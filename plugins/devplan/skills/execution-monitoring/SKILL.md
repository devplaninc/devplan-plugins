---
name: execution-monitoring
description: Build an Execution Monitoring dashboard of every active project, planned or inferred by Devplan from the team's work, with its recent activity, progress, risks, and drift from its spec, plus a button to start a new project. Use for "execution monitoring", "project status", "how are our projects going", "what's at risk", "portfolio view", "delivery health", "what is the team actually working on", or "start a new project".
---

# Execution Monitoring

Every project the team is running, how it's actually going, and what's at risk. Read-only: never change projects, tickets, or owners unless the user asks.

## How this runs

Open with one friendly line and the plan:

> 1. Load your projects
> 2. Check activity, progress, and risks
> 3. Build your Execution Monitoring dashboard

Start each step with a short progress line ("Step 2 of 3: ..."). Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan connected, then follow `devplan-setup` from step 1. Stop this skill there.
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Projects

Call `list_workspace_projects` (not done, not archived; page through all of them). Include both kinds:

- **Planned projects:** projects with a spec or requirements in Devplan.
- **Inferred projects:** initiatives Devplan detected from the team's work without a plan. Use the project's own flag if it has one. Otherwise treat a project with linked activity but no requirements document as inferred.

Window for activity: the last 14 days, compared with the 14 before.

## 2. Activity, progress, and risks

For each project:

- **Activity:** linked changes and signals in the window, from the graph. Timestamps are epoch milliseconds; write the computed number in place of `$since`.
  ```
  MATCH (x)-[:LINKED_TO]->(p:Project) WHERE (x:Change OR x:Signal) AND x.periodEnd >= $since
  RETURN p.projectId, labels(x)[0] AS kind, count(x) AS n, max(x.periodEnd) AS last
  ```
  Project nodes have no titles; join to `list_workspace_projects` by ID.
- **Progress:** status, owner, and due date from the project record (`list_workspace_projects`), which is more current than the graph's status. Completion percent from the graph's Project node.
- **Risks:** for active projects, fetch the project with `fetch_internal_entities_by_ids` (`contentMode: "evidence"`, up to 10 at a time) for its assessed progress, risks, and evidence. Add active risk insights tied to its work.
- **Drift:** work linked to the project that its spec doesn't cover, or spec scope with no work after its planned start.

Judge each project's state:

- **On track** (`s-ok`): activity in the window, no high-severity risk, progress consistent with the due date.
- **At risk** (`s-warn`): a medium or high risk, slowing activity, or a due date close with low completion.
- **Off track** (`s-bad`): past due, blocked, or a high-severity risk with no mitigation.
- **Quiet** (`s-warn`): no linked activity for 7+ days on an active project.
- **Inferred** (`s-info`): work happening without a plan.

Planned status isn't proof of delivery. Base the state on evidence.

## 3. Dashboard

Title: "Execution Monitoring".

1. **Today:** the three project facts that matter most today.
2. **Figures:** active projects, at risk or off track, quiet, inferred.
3. **Projects:** the section header gets a primary **New project** button. One group per planned project, ordered off track, at risk, quiet, then on track. The parent row: project name linked to Devplan, one-line summary of where it stands, owner, due date, completion, last activity, state pill, and a trail of the most telling recent evidence. Child rows: its risks and drift items, each with evidence. Projects with drift get an **Update spec** button.
4. **Inferred projects:** rows for work Devplan sees without a plan: what it looks like, who's doing it, how much activity, and a **Write spec** button to make it a real project.
5. **Recently finished:** dated entries for projects that moved to done in the window.

Button prompts (`data-prompt`):

- **New project:** `Write a Devplan spec for a new project. Ask me what it is first.`
- **Write spec** (inferred): `Write a Devplan spec for "<inferred project name>". Devplan inferred it from recent work: <2 or 3 readable sources, people>.`
- **Update spec** (drift): `Update the Devplan spec for "<project name>". Work has drifted from it: <the drift, with 2 or 3 sources>.`

In chat, offer: "Want me to start a new project, or write a spec for one of the inferred ones?" If yes, follow the `spec` skill.

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
