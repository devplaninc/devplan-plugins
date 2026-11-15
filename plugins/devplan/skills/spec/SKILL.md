---
name: spec
description: Turn an idea, request, or suggested or inferred project into a spec with scope, technical approach, and estimate, after a few discovery questions, and track it in Devplan. Use for "write a spec", "write a Devplan spec", "plan this feature", "new project", "technical plan", "how should we build", "how long will this take", "estimate this", "PRD", "scope this project", or "update the spec".
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
2. If Devplan isn't connected, or a call fails with a sign-in error, say in one line that this needs Devplan, then ask setup's first question, "Do you have a Devplan account?", with its three options (**Yes, connect it**, **No, create one**, **What is Devplan?**), and follow `devplan-setup` from step 1. Stop this skill there. Don't give connect steps or commands of your own, and don't offer to do the task without Devplan (no local drafts, notes-based plans, or git summaries).
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

**Estimate** (see "How to estimate" below)
- PRs required, as a low-high range, with the pieces they come from and the comparable projects used.
- Engineering effort and calendar time as separate ranges, with a confidence level.
- The one-line basis: PRs per engineer-week, cycle time, and comparables.
- The 2 or 3 factors most likely to move the estimate.
- If remaining scope is undefined, say the estimate isn't supportable yet and what would make it so.

**Open questions and sources**
- Open decisions with an owner if known.
- Sources: readable names, dates, and links.

<!-- shared:estimating -->
## How to estimate

Estimate from the team's git history in Devplan, not from ideal hours. Use the last 90 days and leave bots out (authors ending in `[bot]`, dependabot, renovate). Timestamps are epoch milliseconds; write the computed number in place of `$since`.

1. **Team pace from git.**
   ```
   MATCH (a:Person)-[:AUTHORED]->(pr:PullRequest)
   WHERE pr.mergedAt >= $since AND NOT coalesce(a.name,'') ENDS WITH '[bot]'
   RETURN count(DISTINCT a) AS engineers, count(DISTINCT pr) AS prs,
     percentileCont((pr.mergedAt - pr.openedAt)/3600000.0, 0.5) AS p50_hours,
     percentileCont((pr.mergedAt - pr.openedAt)/3600000.0, 0.85) AS p85_hours
   ```
   PRs per engineer-week = prs ÷ engineers ÷ weeks in the window.
2. **PRs per project, from comparable work.** Count the PRs behind each project's linked changes. Recent changes often link to commits rather than PRs, so count both, and convert commits to PRs with the workspace's ratio of merged PRs to commits over the same window (close to 1 when the team squash-merges).
   ```
   MATCH (c:Change)-[:LINKED_TO]->(p:Project) WHERE c.periodEnd >= $since
   MATCH (c)-[:USED]->(x) WHERE x:PullRequest OR x:GitCommit
   RETURN p.projectId,
     count(DISTINCT CASE WHEN x:PullRequest THEN x END) AS prs,
     count(DISTINCT CASE WHEN x:GitCommit THEN x END) AS commits
   ORDER BY prs + commits DESC LIMIT 50
   ```
   Join project IDs to `list_workspace_projects` for titles. Pick the 2 or 3 projects closest in area and scope as comparables.
3. **PRs this work needs.** Break the scope into pieces (from the technical approach, or the project's description), estimate PRs for each piece from the comparables, and add them up as a low-high range. For work already in progress, subtract the PRs already linked to it.
4. **Convert to time.**
   - Effort in engineer-weeks = PRs ÷ PRs per engineer-week.
   - Calendar time = the larger of (effort ÷ engineers on it) and (the longest chain of PRs that must land one after another × p85 cycle time).
   - Plan on the low PR count and median pace. Use the high PR count and p85 cycle time as the risk case.
5. **Show the basis in one line,** in this shape, with this workspace's numbers: "Based on N PRs from M engineers over 90 days (X PRs per engineer-week; cycle time A hours median, B hours at p85). Comparable projects took C to D PRs." Never reuse numbers from this example.

Never invent precision. With no comparable project, give a wide range and say what would narrow it.
<!-- /shared:estimating -->

## Output

- In Claude, publish the spec as a document artifact titled with the feature name, so the user can edit and share it. If documents are unavailable, publish an HTML artifact.
- In Codex or Claude Code, write `devplan/spec-<feature-slug>.md` in the working directory and give the path. The first time you create the `devplan/` folder inside a git repository, suggest adding `devplan/` to `.gitignore`.

## 4. Track it in Devplan

Do this right after the spec is written, without asking. Every spec is tracked.

Never call a Devplan write tool to test whether it works, and never with placeholder or test content. Every write carries the real spec. Before any update, fetch the project in full and use the field values the server returned.

1. **Find an existing project.** If the spec is for a project that already exists (the request named one, or `list_workspace_projects` has one with the same intent), update it: fetch its requirements with their `updatedAt`, then call `update_project` with `action: "update_requirements"`, the full spec as `content`, and the matching `expectedDocumentUpdatedAt`. Refetch and retry once on a conflict.
   - **Inferred project with no requirements document yet** (Devplan found it in the code and nobody has written a spec for it): there is nothing to update, and creating a new project would duplicate it. If the server offers a way to add a first spec to an existing project, use it. If not, don't create anything silently. Ask: "Devplan found this project in your code, but it can't take a spec yet. Track this spec as a new planned project?" with options **Create a planned project**, **Keep the spec here only**. If they choose to create one, follow step 2 and say in one line that the inferred project stays as it is.
2. **Otherwise create one.** If a `create_project` tool is available, call it with the title, a one-line summary, the full spec as markdown, the estimate (PRs, engineer-weeks, and calendar weeks as ranges, confidence, and the one-line basis), the evidence it cites, `origin: "plugin-spec"`, and an idempotency key made from the title and today's date. If not, call `start_feature_planning` with the full spec as `requirements`, then check `check_feature_planning_status` once or twice for the project link. Don't wait more than about a minute; if it's still running, say it's being created.
3. **Tell the user in one line, with the link:** "Tracked in Devplan: <link>. PRs, tickets, and conversations that touch it will link to it as they happen, and Execution Monitoring will show its progress and risks."
4. **If it fails,** say so in one line and offer to try again. The spec itself is still saved.

If the workspace has only one or two members, add one quiet line after the link: "Want your team on it? [Invite teammates](<members page>)." Build the members link as described in `devplan-product-context`. Skip it otherwise.

Then offer one next step: "Want me to break this into stories?" or, if Devplan is generating them, "Devplan is drafting stories from it now."
