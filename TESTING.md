# Test build (0.1.0-test)

This build does not call `get_entitlement`. Each skill picks its mode by calling `list_workspace_members` on the Devplan MCP:

- Works: graph mode (free skills) or full run (premium skills).
- Missing or errors: connector mode or preview run, with upsell copy inline.

## Force a path

Add one of these to any prompt:

- "free mode": connector mode or preview run, with no Devplan tools used.
- "graph mode": Weaver graph or full run.

Every output states its mode on the first line.

## Test script

1. "Set up Devplan". Check it shows the 5-step plan, goes one step at a time, offers the two sign-in options, drafts each of the six context parts and asks about them one at a time, and marks inferred lines. `get_workspace_context` and `save_workspace_context` don't exist yet, so context should fall back to the Project block.
2. "Run my Daily Radar in free mode". Check the coverage footer numbers.
3. "Run my Daily Radar in graph mode". Compare against step 2. The gap between the two is your sales pitch.
4. Repeat steps 2 and 3 for Demand Report and Eng Analytics.
5. "Suggest projects in free mode", then in graph mode.
6. "Stale commitments in free mode" (preview), then in graph mode.
7. "Customer release brief in free mode", then in graph mode. Same for "changelog".
8. "Write a spec for <a real upcoming feature> in free mode". Check it asks one question at a time and stops at 2 to 5. Repeat in graph mode.
9. Ask an ordinary product question ("why are we building X?") without naming a skill. Check product context kicks in quietly, with no upsell.

## Before production

Swap step 0 in every skill back to `get_entitlement` (see the main build and `docs/ENTITLEMENT_SPEC.md`), remove the overrides, and move the upsell copy server-side.
