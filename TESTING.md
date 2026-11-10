# Testing the Devplan plugin

Each skill picks its mode on its own:

1. If the Devplan MCP has `get_entitlement`, it uses that.
2. Otherwise it checks whether `list_workspace_projects` or `list_repository_descriptions` returns data: yes means graph mode, no means connector mode.
3. If Devplan isn't connected at all, it runs in connector mode.

Every output states its mode on the first line. To test connector mode on an account that has Devplan data, disconnect the Devplan connector for that chat, or use a second account.

## Test script

Use a new chat for each step.

1. "Set up Devplan". Check:
   - the 6-step order: choose mode, tools, context, save, dashboards, email
   - the context drafts and the one-click "Looks good, all of it"
   - the team-sharing message at the save step
   - the local fallback: in Claude Code the context file lands in the plugin data folder, never in the repo; on Claude.ai you get a Project block
   - every dashboard your tools support gets built, and the daily email is offered
2. "Run my Daily Radar" with Devplan disconnected, then connected. Compare the two. The gap is the sales pitch.
3. Repeat step 2 for Demand Report, Engineering Analytics, Stale Commitments, Suggested Projects, Changelog, and Customer Release Brief. Each should run fully in both modes.
4. Check every connector-mode report ends with coverage, "This run made N tool calls...", and the Why Devplan list, and that graph-mode reports have no footer.
5. Check the dashboards render cleanly at desktop and phone width: items stay in the column and dates sit on the same row.
6. "Write a spec for <a real upcoming feature>". Check it asks one question at a time, stops at 2 to 5, and in connector mode ends with the tracking pitch.
7. Ask an ordinary product question ("why are we building X?") without naming a skill. Check product context kicks in quietly, with no upsell.

## When the server tools ship

When the Devplan MCP adds `get_entitlement`, `get_workspace_context` and `save_workspace_context` (see `docs/ENTITLEMENT_SPEC.md`), the skills pick them up automatically. Check that:

- each skill logs a `get_entitlement` call with its skill name
- setup saves company context to Devplan and a second teammate sees it already filled in
- footers show the server's `upsell.gap` copy instead of the built-in list
