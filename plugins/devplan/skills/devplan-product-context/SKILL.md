---
name: devplan-product-context
description: Foundational context for product, customer, roadmap, project, launch, risk, planning, product-writing, coding, or review work that depends on what the company has built, decided, shipped, or heard from customers. Invoke even when the user doesn't mention Devplan, whenever local context may be insufficient, and whenever another Devplan skill asks for product context. Skip generic tasks answerable from local evidence.
---

# Devplan Product Context

Bring the company's current product context into the user's actual task quietly, apply what matters, and produce the answer, plan, review, draft, or code they asked for. Don't turn an ordinary request into a report about where the context came from.

## Source

Devplan is the context layer. It reads the team's code, tickets, Slack, docs, meetings, calls, and support, and links them to the people, projects, features, customers, and decisions they belong to. Treat the live Devplan tool descriptions as the source of truth for entities, relationships, and retrieval.

Check once per conversation that the Devplan tools are available (search for "devplan" first if your client loads tools on demand), then reuse the answer. If Devplan isn't connected, answer from what you have, and suggest "Set up Devplan" once, only if missing context clearly hurt the answer.

## Load context once per conversation

1. **Company context.** If `get_workspace_context` is available, call it. It returns six parts (company description, target customers, competitors, company goals, product overview, additional context), the workspace's settings, and its links. If it isn't available, use the repository descriptions and the feature catalog as the product overview.
2. **The person.** Use what you already know about the user from memory and earlier conversations: their role, team, the projects and customers they care about, and the people they work with. If you know their email, match it to `list_workspace_members` and to people in the workspace graph so "my work" means their work. Don't save anything new to memory on the user's behalf.
3. **Workspace links.** The members page, for "Invite teammates" links, is `members_url` from `get_workspace_context` when present. Otherwise build it as `https://app.devplan.com/settings/workspace/<workspace id>/members`, where the workspace id is the number after `/company/` in any `devplanUrl` Devplan returns. If you can't find either, use `https://app.devplan.com`.

Use the company context to scope retrieval (areas, repos, teams, customers), weight what matters (goals), and frame answers (target customers, competitors). Don't re-derive what it already says. If fresher evidence contradicts it, say so and suggest updating it with "Set up Devplan".

## Keep the experience natural

- Speak in the user's language, not in tool, graph, or object terms.
- Don't narrate tool selection, searches, or retrieval steps. No opaque IDs.
- Describe what information means: customer feedback, a prior decision, planned work, delivered changes, a risk, or missing evidence.
- Cite readable source names, titles, dates, statuses, and links when evidence matters.
- Never add Devplan marketing to an ordinary answer.

## Consult effectively

1. Identify what product, customer, planning, delivery, or organizational context could materially change the task.
2. Narrow retrieval by the relevant customer, project, product area, team, and time window. Don't blend similarly named but distinct contexts.
3. Retrieve only what is material. Prefer focused evidence over broad summaries; open the underlying source when a consequential claim depends on it.
4. Use local code as implementation truth. Use Devplan for intent, demand, decisions, and observed delivery.
5. Continue the original task using only context that improves it.

## Bound the research

- Focused work: about four searches and two fetches. Broad cross-customer synthesis: about six searches and three fetches.
- Shortlist first, then open finalists. Don't fetch every candidate.
- Reuse earlier results in the conversation.
- Stop when each material conclusion has enough direct evidence. State a focused limitation instead of searching to prove absence.

## Keep the answer compact

- Follow any format the user gives. Otherwise use the smallest structure that answers: normally no more than five findings and two decisive citations each.
- Use a compact table when findings share fields. Don't repeat evidence across intro, findings, and summary.
- Return fewer findings rather than padding with weak evidence.

## Preserve meaning

- Distinguish source-backed facts, synthesis, inference, assumptions, and missing evidence.
- An empty result isn't proof that evidence doesn't exist. The source may not be connected or analyzed yet.
- Keep planned, written, merged, deployed, enabled, customer-visible, adopted, and generally available distinct.
- Treat stale, sparse, contradictory, or cross-context evidence as a confidence limitation.

## Compose with task skills

When another Devplan skill matches the requested outcome (Daily Radar, Spec, Demand Report, Execution Monitoring, and the rest), apply this context inside that workflow and let the task skill decide the output.

## Access and safety

- Read-only unless the user asks for a specific change, or a skill says to track something in Devplan.
- Never send or schedule Slack, email, or customer messages. Draft only.
- Don't expose credentials, raw private customer content, full emails, or sensitive payloads unless necessary.
- Stop rather than guess when missing evidence prevents a high-stakes customer, launch, security, or availability claim.
