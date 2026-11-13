# Devplan MCP: what the plugin uses and needs

The plugin runs only on the Devplan MCP (`https://app.devplan.com/api/v1/mcp`, OAuth). It works today with the existing tools. The new tools below make setup, context, and spec tracking better; every skill uses a new tool when it exists and falls back when it doesn't, so each one goes live as soon as it's deployed. No plugin release is needed.

## Existing tools the skills use

| Tool | Used by |
|---|---|
| `list_workspace_projects` | Setup, Daily Radar, Execution Monitoring, Demand Report, Stale Commitments, Spec |
| `list_repository_descriptions` | Setup (graph readiness), Spec, product context |
| `list_workspace_members` | Setup, Daily Radar (match the user), Spec (team size) |
| `list_product_feature_catalog` | Demand Report, Changelog, Setup |
| `query_workspace_graph` | Every dashboard |
| `search_entities` | Every dashboard, Spec |
| `fetch_internal_entities_by_ids` | Execution Monitoring (project risks), Spec |
| `update_project` (`update_requirements`) | Spec, when the spec is for an existing project |
| `start_feature_planning`, `check_feature_planning_status` | Spec, to track a new spec until `create_project` exists |

## P0: before public launch

### 1. Sign-up returns the user to the AI app

A new user who clicks Connect in Claude, ChatGPT, or Codex can sign up from the sign-in page and land back in that app, connected. Sign-up keeps the original authorization request (return URL, state) and resumes it after the account and workspace exist. Web onboarding can be finished or skipped and still completes the authorization.

Done when: a brand-new email goes Connect, sign up, connect a repo, and is back in Claude connected, in Claude, ChatGPT, and Codex.

### 2. Dynamic client registration

ChatGPT and Codex require OAuth dynamic client registration. `mcp.json` declares `client.mode: "dcr"`.

### 3. `create_project`: track a spec

Every spec the plugin writes is tracked in Devplan automatically. Today the skill falls back to `start_feature_planning`, which also generates stories in the background. `create_project` should save the spec as written.

Input:

```json
{
  "title": "SCIM 2.0 user provisioning",
  "summary": "One line",
  "requirements_markdown": "The full spec",
  "estimate": { "effort": "3-5 engineer-weeks", "calendar": "4-6 weeks", "confidence": "medium" },
  "evidence": [ { "entityType": "insight", "id": "..." }, { "entityType": "customer_support_ticket", "id": "..." } ],
  "origin": "plugin-spec",
  "generate_stories": false,
  "idempotency_key": "string"
}
```

Returns `{ "projectId", "devplanUrl", "prd": { "id", "updatedAt" } }`.

- Owner defaults to the calling user. Status `DRAFT`.
- Links the evidence to the project so it shows up in the graph right away.
- The same `idempotency_key` returns the existing project instead of creating a duplicate.

### 4. `get_workspace_context` and `save_workspace_context`

Company context is shared by the whole workspace and is where every skill starts.

`get_workspace_context` (no input) returns:

```json
{
  "workspace": {
    "id": "string",
    "name": "Acme",
    "app_url": "https://app.devplan.com/company/<id>",
    "members_url": "https://app.devplan.com/settings/workspace/<id>/members"
  },
  "company_description": "string",
  "target_customers": "string",
  "competitors": "string",
  "company_goals": "string",
  "product_overview": "string",
  "additional_context": "string",
  "settings": {
    "dashboards": { "daily-radar": "https://claude.ai/artifact/...", "execution-monitoring": "..." },
    "schedule": { "time": "07:47", "days": "weekdays" },
    "time_zone": "America/Los_Angeles"
  },
  "me": { "user_id": "string", "name": "string", "email": "string", "radar_focus": "string" },
  "updated_at": "ISO-8601"
}
```

`save_workspace_context` takes the same shape, minus `workspace`. Fields left out are unchanged. `me` fields are saved for the calling user only.

- The company fields map to Knowledge > Workspace in the web app. Product overview is new. Edits in either place show up in the other.
- Empty fields are empty strings. A workspace with nothing saved returns empty fields, not an error.
- Stores text and settings only.

`members_url` is what the dashboards link to for "Invite teammates". Until this ships, skills build `https://app.devplan.com/settings/workspace/<id>/members` from the number after `/company/` in a `devplanUrl`. Confirm that number is the workspace id; if it isn't, this tool is the only reliable source.

### 5. OpenAI directory readiness

- Serve the domain challenge token as plain text at `https://app.devplan.com/.well-known/openai-apps-challenge`.
- Add `readOnlyHint`, `destructiveHint`, and `openWorldHint` annotations to every tool.
- Hide the `COMPOSIO_*` tools from the OpenAI client. General-purpose executors aren't allowed.
- A reviewer test account with sample data and no MFA.

## P1: better dashboards

### 6. Workspace status

`get_workspace_status` returns each connected source with its selection and analysis state, and whether the initial product map is ready. Setup uses it to show what Devplan can see and what's still building. Until then, setup infers readiness from repos, projects, and a recent-activity search.

### 7. Project fields

On `list_workspace_projects` and the graph's `Project` node:

- `inferred` (bool): Devplan detected the project from work rather than a plan. Execution Monitoring currently guesses this from "has linked activity but no requirements document".
- `lastActivityAt` (timestamp): latest linked change or signal.

### 8. Pull request review times

`firstReviewAt` and `approvedAt` on `PullRequest`, so Engineering Analytics can show review wait. Until then it leaves review wait out and says so.

### 9. Create a project from Slack

A message action ("Create Devplan project") and a `/devplan project` command. Uses the thread as starting evidence, asks a few clarifying questions in the thread (the same discovery flow as the Spec skill), creates the project, and links the project and thread both ways.

## Later: free version

Paused while the plugin is Devplan-only: `get_entitlement`, `report_skill_result`, the credits ledger, and server-side upsell copy. The earlier spec is in the git history before v0.2.0.
