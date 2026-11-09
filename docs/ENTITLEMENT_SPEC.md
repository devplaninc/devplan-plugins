# Devplan MCP: entitlement and metering spec

The plugin repo is public. All gating, metering and upsell copy live server-side in the Devplan MCP. Skills only read what the server returns.

## Tiers

| Tier | How you get it | Free skills | Premium skills |
|---|---|---|---|
| `free` | Devplan sign-in, no sources connected | Connector mode | Preview |
| `credits` | Connected at least one source in Devplan. $100 credit granted once per workspace | Graph mode | Full, metered |
| `paid` | Paid Devplan workspace | Graph mode | Full |

When credits hit zero, a `credits` workspace behaves as `free` for free skills and `blocked` for premium skills.

## Tool: `get_entitlement`

Every skill calls this first. The call also logs a skill invocation for analytics.

Input:

```json
{ "skill": "daily-radar", "surface": "claude-ai | claude-code | codex" }
```

Output:

```json
{
  "tier": "free | credits | paid",
  "mode": "connectors | graph",
  "access": "full | preview | blocked",
  "credits": { "granted_usd": 100, "remaining_usd": 63.20 },
  "connected_sources": ["github", "linear"],
  "connect_url": "https://app.devplan.com/connect?src=plugin&skill=daily-radar",
  "upgrade_url": "https://app.devplan.com/billing?src=plugin&skill=daily-radar",
  "upsell": {
    "setup": "string or null",
    "gap": "string with {unattributed} {total} placeholders, or null",
    "preview": "string or null",
    "low_credits": "string or null",
    "blocked": "string or null"
  }
}
```

Rules:

- `mode` applies to free skills: `graph` when tier is `paid`, or `credits` with remaining balance.
- `access` applies to premium skills: `full` for paid or credits with balance, `preview` for free, `blocked` for credits at zero.
- All `upsell` strings are null when tier is `paid`.
- Include `low_credits` in `upsell.gap` and `upsell.preview` when remaining is under 20%.
- URLs carry `src=plugin` and `skill` so conversion is attributable per skill and surface.

## Tool: `report_skill_result` (optional, recommended)

```json
{
  "skill": "daily-radar",
  "mode": "connectors",
  "signals_total": 31,
  "signals_unattributed": 14,
  "sources_used": ["github", "linear", "slack"]
}
```

This is the input to the key funnel analysis: conversion rate by the size of the attribution gap the user saw.

## Tools: `get_workspace_context` and `save_workspace_context`

Saved company context is the main reason to sign in. Setup writes it once; every skill reads it at the start, on every surface.

`get_workspace_context` (no input) returns:

```json
{
  "company_description": "string",
  "target_customers": "string",
  "competitors": "string",
  "company_goals": "string",
  "product_overview": "string",
  "additional_context": "string",
  "settings": {
    "team_channels": ["#eng"],
    "customer_channels": ["#customers"],
    "repos": ["org/repo"],
    "tracker_scope": ["Linear team ENG"],
    "time_zone": "America/Los_Angeles"
  },
  "updated_at": "ISO-8601"
}
```

Empty fields are empty strings. A workspace with no saved context returns all fields empty, not an error.

`save_workspace_context` takes the same shape. Fields left out are unchanged. Returns the saved context.

Rules:

- The five company fields map to the existing workspace context in the Devplan web app (Company description, Target customers, Competitors, Company goals, Additional context). Product overview is new. Edits in either place show up in the other.
- Available on the `free` tier. Never metered.
- Store text and settings only. Skills never send customer content, tickets, or code here.

## Metering

- Meter graph-backed tool calls (`query_workspace_graph`, `search_entities`, `start_feature_planning`, and others) in dollars per call or per tokens of graph context returned. Price so that $100 covers about 2 to 3 weeks of daily use by a 10-person team.
- `get_entitlement` and `report_skill_result` are never metered.
- Return a structured error with `upsell.blocked` text from any metered tool at zero balance, so a skill that skips the entitlement check still upsells.

## Auth

- OAuth with dynamic client registration (DCR) is required for Codex (`mcp.json` declares `client.mode: "dcr"`) and works with Claude remote connectors.
- The same Devplan account powers the web onboarding and the plugin. If the user signed in during onboarding, the OAuth consent screen should be one click.
