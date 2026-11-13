---
name: changelog
description: Build a searchable product changelog of what actually changed, grouped by product area in plain language, with each change's delivery state. Use for "changelog", "release notes", "what shipped today", "what shipped this week", "what changed in the product", "when did we ship", or "ship log".
---

# Changelog

What changed in the product, searchable. Read-only: never publish to a public site, post, or send. Draft only.

## How this runs

Open with one friendly line and the plan:

> 1. Find what changed
> 2. Describe it in plain language
> 3. Build your changelog

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

The dashboard keeps a rolling 30 days so it's worth searching, with the latest working day as the focus (the last 24 hours, or since Friday on Mondays). Honor any window, product area, or audience the user gives. Audience defaults to internal. For customer-facing notes, write for customers and drop internal-only changes.

## 2. Find what changed

Use `query_workspace_graph` and `search_entities` (`change`) for changes in the window with their PRs, projects, and the features they created, updated, or deprecated. Group by product area from `list_product_feature_catalog`. Skip bot authors, dependency bumps, docs-only, and test-only changes.

## 3. Write entries

- Merge changes that make up one improvement into a single entry.
- Write each entry in plain language: what someone can now do, or what got better. One or two sentences, not the implementation.
- State delivery: merged, deployed, enabled for some, or generally available. Merged code isn't proof customers have it; say "merged" unless Devplan shows a deploy, flag, or release.
- Link the project and any customer requests it answers.

## 4. Dashboard

Title: "Changelog".

1. **Today:** the three changes from the latest working day that matter most.
2. **Figures:** changes in the latest working day, in the last 7 days, and in 30 days; areas touched.
3. **Changes:** dated entries for the full 30 days, newest first, with a search box (`placeholder="Search changes"`) and one chip per product area. Each entry: date, area label, plain-language description with links to the PRs and project, and a state pill (`s-ok` generally available, `s-info` merged or deployed, `s-warn` enabled for some).
4. **Not yet available:** merged but not enabled or deployed, so nobody announces them early.

Give every entry `data-area` set to its product area so the chips filter it.

In chat, also offer a plain markdown copy of the latest day's changes for Slack, Notion, or a release-notes page.

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
