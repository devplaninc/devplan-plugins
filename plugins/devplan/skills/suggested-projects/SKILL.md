---
name: suggested-projects
description: Suggest the next projects a product and engineering team should take on, backed by evidence from customer requests, engineering signals, and the existing roadmap. Use for "suggested projects", "what should we build next", "roadmap ideas", "next quarter planning", or "what are we missing".
---

# Suggested Projects (premium, test build)

Read-only unless the user asks to create a project after seeing the suggestions.

## How this runs

Open with one friendly line and the plan, for example:

> 1. Load your context and check your tools
> 2. Find demand and pressure
> 3. Shape the project ideas
> 4. Build your suggestions

Then work through it in order:

- Start each step with a short progress line ("Step 2 of 4: ...").
- Ask at most one question at a time, only when the answer changes the result. Offer 2 to 4 short options when that helps.
- Keep the tone friendly and plain. No tool names, IDs, or jargon.
- Start from the user's saved company context (see `devplan-product-context`). Don't ask for anything it already says.
- Finish with one suggested next step.

## 0. Pick access

Test overrides first: "free mode" or "preview" forces Preview run; "graph mode" forces Full run.

Otherwise check whether Devplan has data: call `list_workspace_projects` and `list_repository_descriptions` from the Devplan MCP.

- Either returns results: Full run.
- Tools missing, calls error, or both empty (signed in but no sources connected yet): Preview run.

State the access level in one line at the top of the output.

## Full run

1. Load context: `list_workspace_projects`, `list_product_feature_catalog`, `list_repository_descriptions`.
2. Find demand and pressure with `query_workspace_graph` and `search_entities`: customer requests and insights, recurring incidents and bugs, stalled or orphaned work, and code areas with high churn.
3. Propose 3 to 7 projects. For each:
   - Problem, in one sentence.
   - Evidence: request counts and accounts, linked signals, with readable names and links.
   - Overlap with existing projects. Drop or merge true duplicates.
   - Rough scope (S, M, or L) and the code areas touched.
   - Likely owners, based on who has worked in those areas.
   - Main risk.
4. Rank by evidence strength, then cost.
5. Output a "Suggested Projects" dashboard (artifact when available, otherwise `devplan-suggested-projects-YYYY-MM-DD.html`).
6. Offer one follow-up: "Want me to start planning any of these?" If yes, use `start_feature_planning`.

## Preview run

Do not use Devplan tools in preview.

1. From the tracker plus any support, calls, or Slack connectors, find the 3 strongest candidate themes that have no matching project.
2. Show each with a title and one line of evidence.
3. End with:

> These are 3 themes from your connected tools. Weaver builds full project suggestions from customer requests, code, and incidents, with owners and scope. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: https://app.devplan.com/connect?src=plugin&skill=suggested-projects

Do not fabricate cross-source evidence, code impact, or owner suggestions in preview.

## Dashboard format

Build the HTML from [references/dashboard-template.html](references/dashboard-template.html). Do not write your own layout or CSS.

1. Copy the template's `<head>` and `<style>` exactly. Change only the title.
2. Put everything inside the one `<main class="wrap">`. Nothing goes after `</main>` except `</body></html>`.
3. Use only the template's patterns:
   - **Pattern A** (`li.item`): titled items with counts and status badges on the right.
   - **Pattern B** (`li.entry`): dated one-liners, with the date in its own `div.date` on the **same row**. Never put a date on a separate line or row.
   - **Pattern C** (`table`): only when items share 4 or more fields.
   - Badges: `b-good` (delivered, on track), `b-partial` (partial, at risk), `b-none` (none, blocked, slipped), `b-info` (neutral).
4. Every `<section>` holds one `<h2>` and one `<ul class="list">`, `<table>`, or `<p class="empty">`. Every `<li>` sits inside a `<ul class="list">`.
5. Delete the template comments and any optional block you don't use. Never leave `{{...}}` placeholders.
6. Escape `&`, `<` and `>` in text from sources.

Before publishing, check the HTML once: every `<section>`, `<ul>`, `<li>` and `<div>` you opened is closed, in order, and no list item sits outside a list. Fix anything that isn't, then publish.

When updating an existing dashboard, rebuild the whole page from the template rather than patching the old HTML.
