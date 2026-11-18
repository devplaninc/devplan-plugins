---
name: eng-analytics
description: Build an Engineering Analytics dashboard of PR throughput, cycle time, review load, and work in progress, daily or weekly, by person and repo. Use for "engineering metrics", "cycle time", "how fast are we shipping", "throughput", "review bottlenecks", "team productivity", or "DORA".
---

# Engineering Analytics

How the engineering system is flowing. Read-only. The per-person summary is there to show load and where help is needed, not to rank: list people alphabetically, never call anyone the best or worst, and keep context (reviews given, on-call, large PRs) next to the numbers.

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
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan, then ask setup's first question, "Do you have a Devplan account?", with its three options (**Yes, connect it**, **No, create one**, **What is Devplan?**), and follow `devplan-setup` from step 1. Stop this skill there. Don't give connect steps or commands of your own, and don't offer to do the task without Devplan (no local drafts, notes-based plans, or git summaries).
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Window

Default: two views. **Daily:** the last 30 days by day, compared with the 30 days before. **Weekly:** the last 8 weeks by week. State both time frames with exact dates. Honor any window, team, or repo the user gives.

## 2. Data

Use `query_workspace_graph`. Timestamps are epoch milliseconds; write computed numbers into the query.

- Pull requests: `openedAt`, `mergedAt`, `closedAt`, `status`, `isDraft`, `repo`, with authors and reviewers.
- Tickets: status and creation time, for work in progress.
- Review events with timestamps (first review, approval), if Devplan has them.

Devplan has already linked PRs to people, so compute by repo and person directly. Leave bot PRs out of every metric (authors ending in `[bot]`, dependabot, renovate), and say how many you excluded. Bots don't count as reviewers either: a PR reviewed only by `claude[bot]` or similar has no human review. Authors not in `list_workspace_members` have left; mark them "(left)" in the by-person table. Compute medians and weekly buckets inside the graph query (`percentileCont`, a week index from the window start) rather than pulling every PR, since results are capped at 200 rows. Use teams from the company context when it names them.

## 3. Metrics

- **Cycle time:** PR opened to merged. Median and 85th percentile.
- **Throughput:** PRs merged per week.
- **Work in progress:** open non-draft PRs, and PRs open longer than 7 days.
- **Review load:** reviews per reviewer, and PRs merged with no recorded review.
- **By person:** for each engineer active in the window, PRs merged, median cycle time, open PRs, and reviews given on others' PRs (exclude self-reviews).
- **For each view:** PRs merged and median cycle time per bucket (day or week), and PRs merged per person and per repo over that view's window. Compute buckets in the graph query from the window start (`toInteger((pr.mergedAt - $start) / 86400000)` for days, `/ 604800000` for weeks).

Add up to 3 findings that explain the biggest changes from the prior period, each with example PRs and one concrete suggestion for what to do about it.

## 4. Dashboard

Title: "Engineering Analytics". Masthead window: "Last 30 days · <dates>". No summary.

1. **View toggle** (Daily and Weekly) right under the masthead, with each view's exact time frame beside it. It switches the four charts below; the figures and tables stay on the 30-day window and say so.
2. **Figures:** PRs merged, median cycle time, p85 cycle time, and share merged without human review, each with its change from the prior 30 days (`up` when the change is good, `down` when it's bad).
3. **Throughput** (Trend): PRs merged per day or per week.
4. **Cycle time** (Trend): median cycle time per day or per week, in hours.
5. **PRs merged by person** and **PRs merged by repo** (Horizontal bars), side by side on wide screens, for the selected view's window.
6. **Findings:** rows with example PRs behind the Evidence link. Each has an action button with the suggestion as a ready prompt, for example **Fix review wait** (`Help me cut our review wait. PRs wait <N> hours for a first review, mostly in <repo>. Draft a review rotation and a Slack message proposing it to the team.`) or **Investigate** (`Why did cycle time in <repo> rise from <A> to <B> hours since <date>? Look at <2 or 3 PR titles>.`).
7. **By person** (table): name, PRs merged, median cycle time, open PRs, reviews given. Alphabetical.
8. **By repo** (table): merged, median and p85 cycle time, open, oldest open.
9. **Long-running PRs:** rows for PRs open longer than 7 days, with author, age, reviewers, and a **Draft nudge** button.

Every bar shows its value on hover (`data-tip`).

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
