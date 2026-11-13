---
name: spec
description: Turn an idea, request, suggested project, or inferred project into a grounded spec - problem, outcome, scope, success criteria, technical approach, and an effort estimate - after a short discovery conversation, then track it in Devplan automatically. Use for "write a spec", "write a Devplan spec", "plan this feature", "new project", "technical plan", "how should we build", "how long will this take", "estimate this", "PRD", "scope this project", or "update the spec".
---

# Spec

Take the user from an idea to one spec that covers the product plan, the technical plan, and the estimate, and track it in Devplan. Make it feel like a short discovery conversation with a sharp product partner, not a form.

## How this runs

Open with one friendly line and the plan:

> 1. Gather what's already known
> 2. Ask a few questions, one at a time
> 3. Write the spec
> 4. Track it in Devplan

Start each step with a short progress line ("Step 2 of 4: ..."). Keep the tone plain. Finish with one suggested next step.

Messages pasted from a Devplan dashboard ("Write a Devplan spec for ...", "Update the Devplan spec for ...") carry the project name and its evidence. Start from them; don't ask for what they already say.

<!-- shared:before-you-start -->
## Before you start

This skill runs on the user's Devplan workspace.

1. Check that the Devplan tools are available. If your client loads tools on demand, search for "devplan" first. Never call a Devplan tool just to find out whether it exists.
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan connected, then follow `devplan-setup` from step 1. Stop this skill there.
3. Load company and personal context with `devplan-product-context`.
4. If the workspace is still being built (Devplan is connected but `list_repository_descriptions` and `list_workspace_projects` both come back empty), work from what exists and don't pad. On a dashboard, show the template's notice ("Devplan is still analyzing your sources. This fills in automatically as it finishes."). Anywhere else, say it in one line.
<!-- /shared:before-you-start -->

## 1. Gather context before asking

Quietly collect what already answers the obvious questions: related and existing projects, customer requests and insights, prior decisions, the feature catalog, repository descriptions, code research, and recent changes in the area. If the request names an existing project ("Update the Devplan spec for ..."), fetch it in full first.

Never make the user tell you something the evidence already shows.

## 2. Discovery

Follow [references/discovery-gate.md](references/discovery-gate.md).

- Open with a short, evidence-informed reflection: what the problem seems to be, who has it, and what the evidence says. Not a blank "tell me more."
- Ask **one question at a time**, usually two to five in total. Each question must be one whose answer changes the spec.
- Use 2 to 4 short multiple-choice options when that makes a tradeoff concrete. Use the client's question tool if one exists.
- Challenge weak premises: if the evidence points to a different problem than the request assumes, say so and ask which to optimize for.
- If the user says "skip" or "just write it", stop asking and write a provisional spec with the open questions listed.

Before writing, restate the agreed problem, user, outcome, and key constraint in two or three sentences.

## 3. Write the spec

Use only the sections the work needs. Keep each tight.

**Product**
- Problem and who has it, with the evidence that shows it.
- Outcome and success criteria: what should move, and the early signal that would show it's wrong.
- Scope and non-goals. Name the smallest valuable version.
- Decisions, constraints, and assumptions (assumptions labeled as such).

**Technical**
- Current state: what exists in the code today. Repository facts only, with file or module names.
- Approach: components, data and API changes, migrations, rollout and flags.
- Testing and observability.
- Dependencies and risks.

Distinguish repository facts from proposed design. If you can't see the code (no repo descriptions and no local repository), say so and keep the technical section to approach-level choices and open questions.

**Estimate**
- Engineering effort and elapsed calendar time as separate ranges, with a confidence level.
- Basis: similar finished projects and the team's observed velocity in that area.
- The 2 or 3 factors most likely to move the estimate.
- If remaining scope is undefined, say the estimate isn't supportable yet and what would make it so. Never invent precision.

**Open questions and sources**
- Open decisions with an owner if known.
- Sources: readable names, dates, and links.

Output:

- In Claude, publish the spec as a document artifact titled with the feature name, so the user can edit and share it. If documents are unavailable, publish an HTML artifact.
- In Codex or Claude Code, write `spec-<feature-slug>.md` to the working directory and give the path.

## 4. Track it in Devplan

Do this right after the spec is written, without asking. Every spec is tracked.

1. **Find an existing project.** If the spec is for a project that already exists (the request named one, or `list_workspace_projects` has one with the same intent), update it: fetch its requirements with their `updatedAt`, then call `update_project` with `action: "update_requirements"`, the full spec as `content`, and the matching `expectedDocumentUpdatedAt`. Refetch and retry once on a conflict.
2. **Otherwise create one.** If a `create_project` tool is available, call it with the title, a one-line summary, the full spec as markdown, the estimate, and the evidence it cites. If not, call `start_feature_planning` with the full spec as `requirements`, then check `check_feature_planning_status` once or twice for the project link. Don't wait more than about a minute; if it's still running, say it's being created.
3. **Tell the user in one line, with the link:** "Tracked in Devplan: <link>. PRs, tickets, and conversations that touch it will link to it as they happen, and Execution Monitoring will show its progress and risks."
4. **If it fails,** say so in one line and offer to try again. The spec itself is still saved.

If the workspace has only one or two members, add one quiet line after the link: "Want your team on it? [Invite teammates](<members page>)." Build the members link as described in `devplan-product-context`. Skip it otherwise.

Then offer one next step: "Want me to break this into stories?" or, if Devplan is generating them, "Devplan is drafting stories from it now."
