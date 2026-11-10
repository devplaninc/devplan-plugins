---
name: devplan-product-context
description: Foundational ambient context for product, customer, roadmap, project, launch, risk, planning, product-writing, coding, or review work that may depend on current evidence, decisions, delivery state, or product intent. Invoke even when the user does not mention Devplan if local context may be insufficient, or whenever another Devplan skill asks for product context. Skip generic tasks answerable from local evidence.
---

# Devplan Product Context

Bring current product context into the user's actual task quietly, apply what matters, and produce the answer, plan, review, draft, or code they asked for. Do not turn an ordinary request into a report about where the context came from.

## Pick a source

- **Graph mode:** the Devplan MCP is available and returns workspace data (`list_workspace_projects` or `list_repository_descriptions` returns results). Use Devplan as the primary context layer. Treat the live Devplan MCP tool descriptions as the source of truth for entities, relationships, and retrieval.
- **Connector mode:** Devplan is missing, errors, or has no data yet. Use the user's connected tools instead:
  - Tracker (Linear, Jira, Asana): projects, issues, status, owners, customer requests.
  - Docs (Notion, Confluence, Google Drive): specs, decisions, plans.
  - Code (GitHub, GitLab, or the local repository): implementation truth, recent PRs.
  - Chat and meetings (Slack, Granola, Gong): decisions, commitments, customer conversations.
  - Support (Zendesk, Intercom, Front): customer problems.

Check once per conversation, then reuse the answer.

## Start from saved company context

Before anything else, load the user's company context once per conversation:

1. If `get_workspace_context` is available, call it. It returns six parts: company description, target customers, competitors, company goals, product overview, and additional context.
2. Otherwise, use a **Devplan for <company>** block in the Project instructions or the conversation, if there is one.
3. If neither exists, carry on without it. Suggest "Set up Devplan" once, only if missing context clearly hurt the answer.

Use it to scope retrieval (areas, repos, teams, customers), to weight what matters (goals), and to frame answers (target customers, competitors). Don't re-derive what it already says. If fresher evidence contradicts it, say so and suggest updating it with "Set up Devplan".

If a Devplan tool returns an error saying credits are used up, switch to connector mode for the rest of the conversation. Say so once, in one short line at the end of the answer ("Devplan credits are used up, so this used your connected tools only."). Never show upgrade copy in an ordinary answer.

## Keep the experience natural

- Speak in the user's language, not in tool, graph, or object terms.
- Do not narrate tool selection, searches, or retrieval steps. No opaque IDs.
- Describe what information means: customer feedback, a prior decision, planned work, delivered changes, a risk, or missing evidence.
- Cite readable source names, titles, dates, statuses, and links when evidence matters.
- Never add upgrade or Devplan marketing to an ordinary answer. Mention Devplan only when the user asks or its context materially changed the result.

## Consult effectively

1. Identify what current product, customer, planning, delivery, or organizational context could materially change the task.
2. Narrow retrieval by the relevant customer, project, product area, team, and time window. Do not blend similarly named but distinct contexts.
3. Retrieve only what is material. Prefer focused evidence over broad summaries; open underlying sources when a consequential claim depends on them.
4. Use local code as implementation truth. Use Devplan or connected tools for intent, demand, decisions, and observed delivery.
5. Continue the original task using only context that improves it.

## Bound the research

- Focused work: about four searches and two source fetches. Broad cross-customer synthesis: about six searches and three fetches. Connector mode spans several tools, so split the same budget across them rather than multiplying it.
- Shortlist first, then open finalists. Do not fetch every candidate.
- Reuse earlier results in the conversation.
- Stop when each material conclusion has enough direct evidence. State a focused limitation instead of searching to prove absence.

## Keep the answer compact

- Follow any user-specified format. Otherwise use the smallest structure that answers: normally no more than five findings and two decisive citations each.
- Use a compact table when findings share fields. Don't repeat evidence across intro, findings, and summary.
- Return fewer findings rather than padding with weak evidence.

## Preserve meaning

- Distinguish source-backed facts, synthesis, inference, assumptions, and missing evidence.
- An empty result is not proof that evidence does not exist. In connector mode, it may only mean the tool isn't connected.
- Keep planned, written, merged, deployed, enabled, customer-visible, adopted, and generally available distinct.
- Treat stale, sparse, contradictory, or cross-context evidence as a confidence limitation.

## Compose with task skills

When another Devplan skill matches the requested outcome (Daily Radar, Spec, Demand Report, and others), apply this context inside that workflow and let the task skill decide the output.

## Access and safety

- Read-only unless the user asks for a specific change.
- Never send or schedule Slack, email, or customer messages. Draft only.
- Do not expose credentials, raw private customer content, full emails, or sensitive payloads unless necessary.
- If no source could be checked, say so and continue only with clearly labeled local evidence and assumptions.
- Stop rather than guess when missing evidence prevents a high-stakes customer, launch, security, or availability claim.
