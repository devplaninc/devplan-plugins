---
name: demand-report
description: Build a Demand Report of what customers actually need, with competitor moves and market trends, and the projects each demand theme suggests. Ranks recurring capabilities, workflows, and adoption blockers by evidence, flags demand nobody is building, and turns each theme into suggested projects that start a spec in one click. Use for "demand report", "customer requests", "what are customers asking for", "feature requests", "voice of customer", "what should we build next", "suggested projects", "roadmap ideas", or "what are competitors doing".
---

# Demand Report

What customers need, what the market is doing, and what to build about it. Read-only: never reply to tickets, post in Slack, or create projects unless the user asks.

## How this runs

Open with one friendly line and the plan:

> 1. Collect customer evidence
> 2. Check the market and competitors
> 3. Find the demand themes and the projects they suggest
> 4. Build your Demand Report

Start each step with a short progress line ("Step 2 of 4: ..."). Ask at most one question, only when the answer changes the result. Finish with one suggested next step.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan connected, then follow `devplan-setup` from step 1. Stop this skill there.
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Scope

Default: customer evidence from the last 90 days, all customers. Honor any window, account, segment, or product area the user gives. Older evidence can corroborate a recent theme. Weight everything by the company goals in the company context.

## 2. Customer evidence

Use `search_entities` across `insight`, `customer_support_ticket`, `call_note`, `discussion_topic`, and `signal`, and `query_workspace_graph` for feature-request insights with their status, business impact, and supporting signals. Devplan has already deduplicated evidence and matched customers across tools.

If a search filtered by date comes back empty, search again without the date filter and filter by each result's source date yourself. Some sources aren't indexed by source time.

For each piece of evidence keep: account, requester, date, source, and a one-line paraphrase.

Then check the current response for each candidate theme with `list_workspace_projects`, `list_product_feature_catalog`, and recent changes: delivered, in progress, planned, or none.

## 3. Market and competitors

Use web search. Keep it to about six searches.

- **Competitors:** for each competitor in the company context (top 3 to 5), search for launches, pricing changes, and announcements in the scope window. Prefer the competitor's own changelog, blog, and docs.
- **Market trends:** two or three searches on the company's category and its target customers' buying criteria (for example "mid-market analytics buyers SSO requirement 2026").

Keep only items with a date and a source you can link. Market evidence changes the weight of a theme; it never creates one on its own:

- A competitor shipping what customers ask for raises urgency: mark the theme "competitive gap".
- A trend that makes a theme a buying requirement raises it.
- Market items that match no customer demand go in the market section only.

## 4. Themes

1. **Name themes as specific product implications:** a capability, a workflow, or an adoption blocker. Broad aspirations ("single source of truth") are context, not themes.
2. **Count corroboration strictly.** An account counts only when its evidence supports the named capability or blocker, not an adjacent pain. Don't merge separate remedies because they serve the same goal, and don't spend several ranks on facets of one blocker.
3. **Recurring vs isolated.** Two or more independent accounts make a theme. Single-account asks go in the isolated list.
4. **Adoption blockers need proof** that the issue blocked approval, adoption, or reliance, not just a wish.
5. **Rank** by independent accounts, then recency, then goal fit and market pressure. Return fewer themes rather than padding with weak evidence.

## 5. Suggested projects

For each of the top themes, propose 1 to 3 projects that would answer it:

- If an existing project already answers the theme, show that project instead of a suggestion: its name, state, and link.
- For each suggestion: a title, the problem in one sentence tied to a company goal where one fits, rough scope (S, M, or L), the code areas it touches (from repository descriptions and the feature catalog), likely owners from who has worked in those areas (leave blank rather than guess), and the main risk.
- Drop suggestions that duplicate planned work. Prefer the smallest project that changes the customer's experience.

## 6. Dashboard

Title: "Demand Report". Scope line: accounts and sources covered.

1. **Today:** the three demands that matter most right now, one sentence each.
2. **Figures:** demand themes, themes with no tracked work, accounts asking, suggested projects.
3. **Demand and suggested projects:** one group per theme, ranked. The parent row: theme name, type, accounts and mentions, current response as its state (`s-bad` no tracked work, `s-warn` partial or planned, `s-ok` delivered), and an evidence trail of customer and market sources. Child rows, labeled "Suggested projects": each suggested project with a **Write spec** button, or the existing project with its link.
4. **Market and competitors:** dated entries with search and chips for "Competitor" and "Trend", each linked to its source, with a state pill: "Gap" (`s-bad`), "Partial" (`s-warn`), "Context" (`s-info`).
5. **Adoption blockers:** rows with the proof they blocked approval or adoption.
6. **Isolated asks:** single-account requests worth watching.

The **Write spec** button's `data-prompt` must start the spec on its own:

```
Write a Devplan spec for "<project title>". It comes from the "<theme>" theme in my Demand Report: <N> accounts asking, including <2 or 3 account names>. Key evidence: <2 or 3 readable sources>.
```

In chat, after publishing, offer: "Want me to write a spec for one of these?" If yes, follow the `spec` skill.

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
