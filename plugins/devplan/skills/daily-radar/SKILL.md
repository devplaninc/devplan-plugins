---
name: daily-radar
description: Build a personal Daily Radar ("Your daily radar") dashboard of what shipped, what's moving, what's stuck, and what needs the user's attention, tailored to their role, team, and projects. Use for "daily radar", "what happened yesterday", "team status", "standup prep", "what's blocked", "what needs my attention", or "catch me up".
---

# Your daily radar

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
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan, then ask setup's first question, "Do you have a Devplan account?", with its three options (**Yes, connect it**, **No, create one**, **What is Devplan?**), and follow `devplan-setup` from step 1. Stop this skill there. Don't give connect steps or commands of your own, and don't offer to do the task without Devplan (no local drafts, notes-based plans, or git summaries).
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Who it's for

The radar is personal. Work out, in this order:

1. **Who they are.** From memory and earlier conversations: name, email, role, team. A scheduled run's instructions may name them and their focus; use that.
2. **What they care about.** The radar focus areas saved during setup or named in a scheduled run's instructions (product areas, teams, or themes, not project lists). Add from memory: customers they handle, people they work with, and anything they've said they want to watch. Map focus areas to work through the feature catalog and the projects and repos linked to those areas.
3. **Their footprint in Devplan.** Match their email to `list_workspace_members` and to a person in the graph. From the graph, find projects they own, PRs they authored or review, and work linked to their projects.

Use this to order and filter, not to hide: their items come first, the team's important items follow. If you know nothing about them, show the team view and end with: "Want this tailored to you? Tell me your role and the areas to focus on."

Don't save anything new to memory.

## 2. Window

Default: the last 24 hours. On Monday, since Friday 00:00 local. Honor any window the user gives.

## 3. Gather

Use `query_workspace_graph`, `search_entities`, and `list_workspace_projects`. Devplan has already attributed activity to people and projects across every source, so don't re-derive attribution.

- **Shipped:** merged PRs and changes in the window, with their projects and features.
- **Moving:** PRs opened, tickets started, projects with new linked activity.
- **Stuck:** open PRs older than 2 days, tickets in progress with no activity for 3+ days, active risk insights, projects whose due date is close and completion is low.
- **Talk:** discussion topics and meeting notes in the window with decisions, blockers, escalations, or customer issues. Skip chatter.
- **For them:** PRs waiting on their review, new risks and slips in their focus areas and on work they own, mentions of their areas or customers in discussions and calls.
- **Insights for their role:** active risk insights and open feature-request insights from the graph (`MATCH (i:Insight) WHERE (i.kind='risk' AND i.status='active') OR (i.kind='feature_request' AND i.status IN ['not_started','planned','in_progress'])`), filtered by `roleIds` to the user's role: founders and executives get `product_leader`, `engineering_leader`, `sales`, and `marketing`; product managers `product_manager`; engineering managers `engineering_manager`; and so on. Fetch them with `fetch_internal_entities_by_ids` (compact, a few at a time; large insights truncate) for their name, description, evidence, and suggested action. Rank by severity or business impact, then evidence count, then how recently they were updated.

Example graph queries. Timestamps are epoch milliseconds: compute the window start from today's date and write the number in place of `$since`.

```
MATCH (p:Person)-[:AUTHORED]->(pr:PullRequest) WHERE pr.mergedAt >= $since
RETURN p.name, pr.prId, pr.repo, pr.mergedAt ORDER BY pr.mergedAt DESC LIMIT 100

MATCH (x)-[:LINKED_TO]->(proj:Project) WHERE (x:Change OR x:Signal) AND x.periodEnd >= $since
RETURN proj.projectId, count(x) AS activity, max(x.periodEnd) AS last ORDER BY activity DESC LIMIT 50
```

If a date-filtered `search_entities` call comes back empty, search again without the date filter and keep results whose source date falls in the window; recent sources often aren't indexed by source time.

People who wrote PRs but aren't in `list_workspace_members` have left. Their open PRs are a Needs your attention item (decide: close, hand off, or finish), not noise.

Project nodes have no titles, and their graph status can lag; take titles, status, and owners from `list_workspace_projects`, joined by ID. People in the graph are often named by their git username, so match them by email or `gitUsername`, and show the name from `list_workspace_members` when you can. Leave out bots (names ending in `[bot]`, dependabot, renovate).

## 4. Dashboard

Title: "Your daily radar". Masthead scope: "For <first name>" when personalized, otherwise "Team view". No figures.

1. **Summary:** 3 to 5 concise bullets with the key updates since the last radar, led by what changed in the themes below. Plain text, no links.
2. **Needs your attention:** 3 to 6 themes scoped to the user's role and focus areas, about the bigger things: revenue and customers, product direction, launches, security and trust, team capacity. Build them from the role-filtered insights, then fold in what the last day added across customer calls, internal discussions, tickets, and code. One row per theme: a short name, one or two sentences on what's at stake and what changed recently, the owner if there is one, evidence (the insights' sources, calls, threads, PRs), and **always** one action button that moves the theme forward. Use the insight's own suggested action prompt when it has one; otherwise write one (Draft brief, Draft message, Plan coverage, Write spec). Roll small items (one stale PR, one missing review) into the theme they belong to or leave them out. A manager sees team-level themes; an individual contributor sees their own work. If nothing needs attention, use the Empty pattern.
3. **Product updates:** what changed in the product in the window, as dated entries grouped by area. Each entry names the specific change and says how it affects users, in plain language ("Assistants connected through MCP can now save a spec straight into a Devplan project, so specs written in Claude show up for the whole team"). Group internal-only work (dependency bumps, refactors) into one line that says there's no user-facing change. Mark changes not yet analyzed as such.
4. **In motion:** a group per active project, with its new activity as child rows.

Every item has its evidence behind the Evidence link.

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
