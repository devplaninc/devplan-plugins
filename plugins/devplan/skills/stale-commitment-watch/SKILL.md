---
name: stale-commitment-watch
description: Find product and engineering commitments, promises, and target dates that went quiet, slipped, remain unfinished, or became blocked, and name who needs to act. Use for "stale commitments", "what slipped", "overdue", "what went quiet", "follow-through", "missed dates", "what did we promise", or "what needs a decision".
---

# Stale Commitment Watch (premium, test build)

Read-only. Never update work or contact owners unless the user asks after seeing the results.

Apply `devplan-product-context` to gather context quietly.

## How this runs

Open with one friendly line and the plan, for example:

> 1. Load your context and check your tools
> 2. Find commitments and dates
> 3. Check where each one stands
> 4. Build the list

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

## Scope

Default: commitments made or reaffirmed in the last 60 days. A requested start date bounds when a commitment was made or reaffirmed, not when an old record was last touched. Exclude older promises with no recommitment in the window.

## Full run

1. **Find commitments.** Use `list_workspace_projects`, `query_workspace_graph`, and `search_entities` for projects, stories, and target dates, plus explicit commitments in discussions, meetings, and customer conversations.
2. **Connect each to its current state:** project, story, linked PRs, risks, and the latest activity.
3. **Judge the state:**
   - **Slipped:** the date passed and the work isn't done.
   - **Quiet:** no update, PR, or discussion for 7+ days on something still open.
   - **Blocked:** marked blocked, or waiting on a named dependency.
   - **At risk:** due within 7 days with evidence it won't make it.
4. Exclude commitments that were explicitly dismissed, superseded, or descoped. Rank customer promises, cross-team dependencies, and dated project goals above internal chores.

Output, titled "Stale Commitments":

1. **Decide now:** items needing a decision, each with the owner and the specific decision (recommit, re-date, descope, or unblock).
2. **Slipped**, **Blocked**, **Quiet**, **At risk:** each with what was promised, by whom, when, the original date, current state with evidence, and days overdue or idle.
3. **Customer promises:** any of the above made to a customer, listed separately.

## Preview run

Do not use Devplan tools in preview. Requires a tracker connector. If none, run `devplan-setup`.

1. From the tracker only, list projects and issues with a due or target date that passed, and items marked blocked, in the window.
2. Show up to 10, most overdue first, each with owner, original date, days overdue, and a link.
3. Do not search Slack, meetings, or customer conversations for promises in preview, and do not guess at blockers. Say: "Tracker dates only. Promises made in Slack, meetings, and customer calls aren't checked."
4. End with:

> Weaver finds commitments made in Slack, meetings, and customer calls, links each to the work meant to deliver it, and flags what went quiet. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: https://app.devplan.com/connect?src=plugin&skill=stale-commitment-watch

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

## Output

Every item links to the commitment's source and its current state. Publish an HTML artifact titled "Stale Commitments" when you can, otherwise write `devplan-stale-commitments-YYYY-MM-DD.html` and give the path. Self-contained, light and dark mode, mobile-readable.
