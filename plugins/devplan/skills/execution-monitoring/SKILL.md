---
name: execution-monitoring
description: Execution Monitoring dashboard: active projects from Devplan, Linear, and Jira, what slipped or is blocked, inferred work by theme, and a searchable changelog of what shipped. Use for "execution monitoring", "project status", "how are our projects going", "what's at risk", "what slipped", "overdue", "what's blocked", "what shipped", "changelog", "release notes", or "start a new project".
---

# Execution Monitoring

What the team is running, what's slipping, and what shipped. Read-only: never change projects, tickets, or owners unless the user asks.

## How this runs

Open with one friendly line and the plan:

> 1. Load projects from every tracker
> 2. Check activity, commitments, and risks
> 3. Gather what shipped
> 4. Build your Execution Monitoring dashboard

Start each step with a short progress line ("Step 2 of 4: ..."). Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan, then ask setup's first question, "Do you have a Devplan account?", with its three options (**Yes, connect it**, **No, create one**, **What is Devplan?**), and follow `devplan-setup` from step 1. Stop this skill there. Don't give connect steps or commands of your own, and don't offer to do the task without Devplan (no local drafts, notes-based plans, or git summaries).
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Projects from every tracker

Window: the last 14 days, compared with the 14 before.

Collect work from every project tracker Devplan has, and keep where each item came from:

- **Devplan projects:** `list_workspace_projects` (not done, not archived; page through all of them).
- **Linear projects and issues, Jira epics and stories, and any other tracker Devplan ingests** (GitHub Projects, Asana, Shortcut): use `search_entities` and `query_workspace_graph` for tracker entities, and `fetch_external_entities` for details where needed. Map Jira epics and Linear projects to projects, and Jira stories and Linear issues to their work items.
- **Check tracker freshness:** `MATCH (t:Ticket) RETURN t.provider, max(t.createdAt)`. If a tracker's newest ticket is older than 14 days, it has stopped syncing: say so in the notice and give its section the Empty pattern with a reconnect link, rather than reporting no activity.
- Merge duplicates: a Devplan project linked to a Linear project or Jira epic is one project. Note every source it appears in.

Start from the graph, not the project list: run the activity query in section 2 first, then fetch only those project IDs with `fetch_internal_entities_by_ids` (compact, up to 25 per call). `list_workspace_projects` returns small pages, so paging every project is slow. Keep only projects with activity in the last 14 days (linked changes, PRs, ticket moves, or discussion). Projects with none appear only if they're slipped or blocked (section 2).

**Inferred work:** work Devplan detected without a plan. Use the project's `inferred` flag or `origin: "inferred"` when Devplan returns one; otherwise treat linked activity with no requirements document and no tracker project as inferred.

## 2. Activity, commitments, and risks

For each project:

- **Activity:** linked changes and signals in the window. Timestamps are epoch milliseconds; write the computed number in place of `$since`.
  ```
  MATCH (x)-[:LINKED_TO]->(p:Project) WHERE (x:Change OR x:Signal) AND x.periodEnd >= $since
  RETURN p.projectId, labels(x)[0] AS kind, count(x) AS n, max(x.periodEnd) AS last
  ```
  Project nodes have no titles; join to `list_workspace_projects` by ID. Add ticket movement from the tracker.
- **Progress:** status, owner, and due date from the project record or tracker, which is more current than the graph's status. Completion from the graph's Project node or the tracker's issue counts.
- **Risks:** fetch active projects with `fetch_internal_entities_by_ids` (`contentMode: "evidence"`, up to 10 at a time) for assessed progress, risks, and evidence. Add active risk insights tied to the work.
- **Drift:** work linked to the project that its spec doesn't cover, or spec scope with no work after its planned start.

**Commitments.** Also find dated commitments from the last 60 days: due dates on projects, epics, stories, and issues that passed or fall within 7 days, and explicit internal commitments in discussions and meeting notes ("we'll ship by", "ETA", "by Friday"). Customer promises belong in the Demand Report; leave them out here. Exclude commitments explicitly dismissed, superseded, or descoped.

Judge each project and commitment:

- **On track** (`s-ok`): activity in the window, no high-severity risk, progress consistent with the due date.
- **At risk** (`s-warn`): due within 7 days with evidence it won't make it, a medium or high risk, or slowing activity.
- **Slipped** (`s-bad`): the date passed and the work isn't done.
- **Blocked** (`s-bad`): marked blocked, or waiting on a named dependency.
- **Inferred** (`s-info`): work happening without a plan.

Planned status isn't proof of delivery. Base the state on evidence.

## 3. What shipped

Use `query_workspace_graph` for changes in the last 14 days (`MATCH (c:Change) WHERE c.periodEnd >= $since`), then `fetch_internal_entities_by_ids` (compact, 25 per call) for their summaries, and `MATCH (c:Change)-[:USED]->(x) RETURN c.changeId, x.repo, x.sha, x.number` for links. Use `search_entities` (`change`) only to filter by topic with their PRs, projects, and the features they created, updated, or deprecated. Group by product area from `list_product_feature_catalog`. Skip bot authors, dependency bumps, docs-only, and test-only changes. Merge changes that make up one improvement into one entry, written in plain language: what someone can now do, or what got better. State delivery: merged, deployed, enabled for some, or generally available. Merged code isn't proof customers have it; say "merged" unless Devplan shows a deploy, flag, or release.

## 4. Dashboard

Title: "Execution Monitoring".

1. **Summary:** 3 to 5 concise bullets on the main activity in the window: where the team's effort went, what landed, what slipped. Plain text, no links.
2. **Figures:** active projects, slipped or blocked, at risk, inferred themes.
3. **Projects:** the section header gets a primary **New project** button. One group per project with activity in the last 14 days, plus any slipped or blocked commitment, ordered slipped, blocked, at risk, then on track. A commitment that isn't tied to a project gets its own row in the same list. The parent row: name linked to its source, the source in the side line ("Linear project", "Jira epic", "Devplan project"), one-line summary of where it stands, owner, due date and days overdue when slipped, completion, last activity, state pill, and evidence. Slipped, blocked, and at-risk rows get **Draft nudge** (`Draft a short Slack message to <owner> about "<item>", due <date>: <state and evidence>. Ask whether to recommit, re-date, descope, or what would unblock it.`) or **Re-plan** (`Help me re-plan "<item>". It was due <date> and is <state>: <evidence>. Give me options to recommit, re-date, or descope.`). Child rows: risks and drift, each with evidence. Projects with drift get **Update spec**.
4. **Tracker callout:** if Linear, Jira, or another tracker isn't connected or has stopped syncing, put one notice directly below Projects (not at the top, and not as its own section) saying which tracker and since when, with a **Reconnect** button linking to https://app.devplan.com.
5. **Inferred work:** start with one line explaining the section: "Work Devplan sees happening without a project or ticket behind it, grouped by theme." Then one row per theme: a short name, a concise description of the work, who's doing it, how much activity, and evidence. No buttons.
6. **Changelog:** at the bottom. Dated entries for the last 14 days, newest first, with a search box (`placeholder="Search changes"`), an Area chip row (one chip per product area), and a Person chip row (one chip per author, bots excluded, departed people marked "(left)"). Each entry: date, area label, plain-language description followed by the author's name (`<span class="m">· Name</span>`), evidence, and a state pill (`s-ok` generally available, `s-info` merged or deployed, `s-warn` enabled for some). Give every entry `data-area` set to its product area and `data-person` set to its author's display name; separate several authors with `|`.

Button prompts (`data-prompt`):

- **New project:** `Write a Devplan spec for a new project. Ask me what it is first.`
- **Update spec** (drift): `Update the Devplan spec for "<project name>". Work has drifted from it: <the drift, with 2 or 3 sources>.`

Empty states: no code changes means "Connect a repository in Devplan to fill in the changelog". A missing tracker is the callout under Projects, not an empty section.

In chat, offer: "Want me to draft the nudges for what slipped?" Also offer a plain markdown copy of the last day's changelog for Slack, Notion, or release notes. For a spec, follow the `spec` skill.

<!-- shared:dashboard-format -->
## Dashboard format

Build the page from [references/dashboard-template.md](references/dashboard-template.md). Don't write your own layout, CSS, or script.

1. Copy the template's `<head>`, `<style>` and `<script>` exactly. Change only the `<title>`.
2. Fill the masthead: workspace name, page title, window, scope, and "Last refreshed" with the time this run finished.
3. Use only the template's patterns: Summary, Figures, Rows, Groups, Folds, Dated entries, Table, Trend, Horizontal bars, View toggle, Meter, Timeline, Tabs, and Empty. Every bar in Trend and Horizontal bars gets a `data-tip` with its label and value ("Nov 3 · 22 PRs") so hovering shows the number. Use Summary and Figures only where this skill asks for them. Delete every pattern you don't use and every template comment. Never leave `{{...}}` placeholders.
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
