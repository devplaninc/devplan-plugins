# Devplan MCP: what the plugin uses and needs

The plugin runs only on the Devplan MCP (`https://app.devplan.com/api/v1/mcp`, OAuth). It works today with the existing tools. Each new tool below is used as soon as it exists; until then the skills fall back as described. No plugin release is needed when they ship.

The plugin never builds Devplan URLs or IDs itself. Every link and ID comes from a Devplan response for the signed-in user's own workspace.

## Existing tools the skills use

| Tool | Used by |
|---|---|
| `list_workspace_projects` | Setup, Daily Radar, Execution Monitoring, Demand Report, Stale Commitments, Cycle Planning, Spec |
| `list_repository_descriptions` | Setup (graph readiness), Spec, product context |
| `list_workspace_members` | Setup, Daily Radar (match the user), Spec (team size) |
| `list_product_feature_catalog` | Demand Report, Changelog, Setup |
| `query_workspace_graph` | Every dashboard, Cycle Planning and Spec estimates |
| `search_entities` | Every dashboard, Spec |
| `fetch_internal_entities_by_ids` | Execution Monitoring (project risks), Spec |
| `update_project` | Spec (`update_requirements` for an existing project), Cycle Planning (`assign_roadmap_section`, on request) |
| `start_feature_planning`, `check_feature_planning_status` | Spec, to track a new spec until `create_project` exists |

## P0: before public launch

### 1. Sign-up returns the user to the AI app

A new user who clicks Connect in Claude, ChatGPT, or Codex can sign up from the sign-in page and land back in that app, connected. Sign-up keeps the original authorization request (return URL, state) and resumes it after the account and workspace exist. Web onboarding can be finished or skipped and still completes the authorization.

Done when: a brand-new email goes Connect, sign up, connect a repo, and is back in Claude connected, in Claude, ChatGPT, and Codex.

### 2. Dynamic client registration

ChatGPT and Codex require OAuth dynamic client registration. `mcp.json` declares `client.mode: "dcr"`.

### 3. Track every spec: `create_project`, and fix project writes over MCP

The Spec skill tracks every spec it writes as a Devplan project, without asking. Two problems block that today.

**3a. Project writes return 403 over MCP.** `start_feature_planning` returned `403 Forbidden` twice on Nov 12 to 13 from a signed-in Claude session, while every read tool worked with the same token. Find out whether it's role scoping, a missing OAuth scope, or a firewall rule on `/api/v1/mcp`, and fix it so any workspace member can create and update projects over MCP. Check `update_project` with `update_requirements` at the same time; the Spec skill uses it when the spec is for an existing project.

**3b. `create_project`.** Today the skill falls back to `start_feature_planning`, which also generates stories in the background and doesn't take an estimate or evidence. `create_project` saves the spec as written.

Input:

```json
{
  "title": "SCIM 2.0 user provisioning",
  "summary": "One line",
  "requirements_markdown": "The full spec",
  "estimate": {
    "prs": { "low": 22, "high": 34 },
    "engineer_weeks": { "low": 3, "high": 4.5 },
    "calendar_weeks": { "low": 4, "high": 6 },
    "confidence": "medium",
    "basis": "410 PRs from 4 engineers over 90 days; comparables: Zoom support (31 PRs), Goal attachments (12 PRs)"
  },
  "evidence": [ { "entityType": "insight", "id": "..." }, { "entityType": "customer_support_ticket", "id": "..." } ],
  "origin": "plugin-spec",
  "roadmap_section_id": "optional",
  "generate_stories": false,
  "idempotency_key": "string"
}
```

Returns `{ "projectId", "devplanUrl", "prd": { "id", "updatedAt" } }`.

- Any workspace member can call it. Owner defaults to the caller. Status `DRAFT`.
- Links the evidence to the project so it appears in the graph right away, and the project's own changes start linking from then on.
- Stores the estimate on the project so Execution Monitoring and Cycle Planning can compare it with actual PRs later.
- The same `idempotency_key` returns the existing project instead of creating a duplicate.
- `generate_stories: true` keeps today's story generation available on request.

Done when: "Write a spec for X" in Claude ends with a working Devplan link, a retry doesn't duplicate it, and "Update the spec for X" changes the same project.

### 4. Save and load company context: `get_workspace_context` and `save_workspace_context`

Company context is shared by the whole workspace, and every skill starts from it. Today setup can't save it and asks the user to paste it into Knowledge > Workspace. The response also gives the plugin the workspace's ID and links, which it needs for "Invite teammates".

`get_workspace_context` (no input) returns:

```json
{
  "workspace": {
    "id": "string",
    "name": "Acme",
    "app_url": "https://app.devplan.com/...",
    "members_url": "https://app.devplan.com/settings/workspace/<id>/members",
    "integrations_url": "https://app.devplan.com/..."
  },
  "company_description": "string",
  "target_customers": "string",
  "competitors": "string",
  "company_goals": "string",
  "product_overview": "string",
  "additional_context": "string",
  "settings": {
    "dashboards": { "daily-radar": "https://claude.ai/artifact/...", "execution-monitoring": "https://claude.ai/artifact/..." },
    "schedule": { "time": "07:47", "days": "weekdays" },
    "time_zone": "America/Los_Angeles"
  },
  "me": { "user_id": "string", "name": "string", "email": "string", "role": "string", "radar_focus": "string" },
  "updated_at": "ISO-8601",
  "updated_by": "user id"
}
```

`save_workspace_context` takes the same shape without `workspace`, plus `expected_updated_at`:

- Partial update: fields left out are unchanged.
- `me` is saved for the calling user only. `settings.dashboards` and `settings.schedule` are per user too (each person has their own artifacts and schedule); store them under the caller.
- If `expected_updated_at` doesn't match, return a conflict with the current context so the skill can merge and retry.
- Any workspace member can read. Any member can save the company fields; record `updated_by`.
- The company fields are the same fields as Knowledge > Workspace in the web app. Product overview is new. Edits in either place show up in the other.
- Empty fields are empty strings. A workspace with nothing saved returns empty fields, not an error.
- Text and settings only, up to about 20 KB per field.

Until this ships, the "Invite teammates" link goes to `https://app.devplan.com`, labeled "Invite teammates in Devplan", because the plugin has no reliable workspace ID.

Done when: context saved from Claude shows in Knowledge > Workspace and the reverse, a second teammate gets it from `get_workspace_context`, and every dashboard's "Invite teammates" opens that workspace's members page.

### 5. Tag inferred projects

Execution Monitoring and Cycle Planning treat projects Devplan inferred from the team's work differently from planned ones: inferred projects get a "Write spec" button to turn them into real plans. Nothing marks them today, so the skill guesses ("has linked activity but no requirements doc"), and the guess is wrong for some projects.

On `list_workspace_projects`, `fetch_internal_entities_by_ids` (project), and the graph's `Project` node, add:

- `origin`: one of `planned` (created by a person in Devplan), `inferred` (detected from work), `suggested` (proposed from insights), `plugin-spec` (created by the Spec skill), `slack` (created from Slack).
- `inferred` (bool): shorthand for `origin == "inferred"`.
- `inferredFrom`: for inferred projects, the main evidence (changes, signals, people) that led to it.
- `lastActivityAt`: latest linked change or signal.

Also: the graph's `Project.status` lags the project record (active projects show `UNKNOWN`, some `DONE` projects are still getting work). The skills read status from `list_workspace_projects` for now; sync the graph so both agree.

Done when: Execution Monitoring's "Inferred projects" section matches what the Devplan web app shows as inferred.

### 6. OpenAI directory readiness

- Serve the domain challenge token as plain text at `https://app.devplan.com/.well-known/openai-apps-challenge`.
- Add `readOnlyHint`, `destructiveHint`, and `openWorldHint` annotations to every tool.
- Hide the `COMPOSIO_*` tools from the OpenAI client. General-purpose executors aren't allowed.
- A reviewer test account with sample data and no MFA.

## P1: better estimates and dashboards

### 7. Link PRs to changes again

Spec and Cycle Planning estimate from PRs: the team's cycle time and throughput from git, and how many PRs comparable projects took. In the last 90 days, 0 of 399 changes link to a `PullRequest` (`Change-[:USED]->PullRequest`); they all link to `GitCommit` instead, so the skills convert commits to PRs with the workspace's PR-to-commit ratio. Restore the `Change -> PullRequest` link for new changes, or add `PullRequest-[:LINKED_TO]->Project`.

### 8. Pull request review times

`firstReviewAt` and `approvedAt` on `PullRequest`, so Engineering Analytics can show review wait and estimates can separate review time from coding time.

### 9. Project completion date

`completedAt` on projects, so comparables can be sized by elapsed time as well as PRs.

### 10. Workspace status

`get_workspace_status` returns each connected source with its selection and analysis state, and whether the initial product map is ready. Setup uses it to show what Devplan can see and what's still building. Until then, setup infers readiness from repos, projects, and a recent-activity search.

### 11. Create a project from Slack

A message action ("Create Devplan project") and a `/devplan project` command. Uses the thread as starting evidence, asks a few clarifying questions in the thread (the same discovery flow as the Spec skill), creates the project with `create_project` (`origin: "slack"`), and links the project and thread both ways.

## Later: free version

Paused while the plugin is Devplan-only: `get_entitlement`, `report_skill_result`, the credits ledger, and server-side upsell copy. The earlier spec is in the git history before v0.2.0.
