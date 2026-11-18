# Testing the Devplan plugin

Every skill needs the Devplan connector. Test with a workspace that has at least one analyzed repo, plus Slack and a tracker if you can. For the new-user path, use an email that has never been used on Devplan.

Run `python3 scripts/sync.py` and `claude plugin validate plugins/devplan` before every release.

## Test script

Use a new chat for each step.

1. **Setup, new user.** Disconnect Devplan (or use a fresh account) and say "Set up Devplan". Check:
   - the welcome lists what they'll get, then the 5 steps
   - "What is Devplan?" explains in four lines; "No, create one" shows the five onboarding steps (account, company, repo plus other sources, graph build, come back) and the sign-up link
   - the connect steps match the surface you're on, word for word (Claude: Plugins > Devplan > Connect; Claude Code: sign-in link or `/mcp` > plugin:devplan:devplan; Codex: `codex mcp add devplan --url ...`)
   - no sign-in tips beyond those, and no pointer to the Devplan website for connecting
2. **Setup, connected.** Say "Set up Devplan" with Devplan connected. Check:
   - the workspace summary names what Devplan can see and which dashboards are ready
   - company context is shown from Devplan, or drafted with "(inferred)" marks, and the one-click "Looks good, all of it"
   - the radar focus question asks for focus areas (not projects) and is skipped when Claude already knows them
   - the tour gives product and technical example questions and ends with one exact message to try first
   - one confirmation builds every ready dashboard, one at a time
   - in Claude, it creates **one** scheduled task at 7:47 and 12:47 on weekdays with email on, with only Devplan attached where the tool allows, and says what the task can access
   - in ChatGPT and the Codex app, it builds **one** "Devplan" Site with four tabs and **one** scheduled task at both times; the tab is remembered in the URL hash
   - in Claude Code and Codex CLI, it doesn't offer scheduling and suggests "Refresh my Devplan dashboards"
   - with Sites unavailable, the combined page lands at `devplan/devplan.html`; in Claude Code, dashboards land in `devplan/` as full pages (open one from disk: no broken characters)
   - the tour ends with a single, quiet Invite teammates line
3. **Graph still building.** On a workspace that just connected its first repo, run setup. It should explain that dashboards fill in as analysis finishes, and every dashboard should show the notice instead of empty filler.
4. **Each dashboard.** "Run my Daily Radar", "How are our projects going?", "Build my demand report", "How fast are we shipping?". For each, check:
   - it uses the template: ink masthead, then only the summary and figures that skill asks for (Radar, Demand, and Cycle have no figures; Demand and Eng have no summary), then sections
   - summary bullets are short, with no links
   - evidence is closed by default behind "Evidence · N", pills show titles (no PR numbers), and the link opens and closes
   - every finding, risk, ask, or needs-attention item has an action button that copies a working prompt
   - an empty section names the source to connect or the next thing to try, with a button
   - every item links to a real source, with readable labels and no IDs
   - bots don't appear as people
   - light and dark mode, and phone width, look right
   - the footer's Invite teammates link opens your workspace's members page
5. **Your daily radar.** Run it in a chat where Claude knows your role and focus areas, then in one where it doesn't. The first has scope "For <name>" and puts your items first in Needs your attention; the second shows the team view and offers to tailor it. Every Needs your attention row has an action button; the last section is "In motion".
6. **Demand Report.** No summary or figures. Themes are built from every Devplan suggested project (none dropped; single-account ones go to Isolated asks), and a second run keeps the same theme names unless new asks arrived. Sections in order: Themes (Existing projects, then Devplan suggested projects under each), Isolated asks, Adoption blockers, Customer promises, Market and competitors. Market items are all within the last 2 weeks. Click Write spec and Draft follow-up, paste into a new chat, and check each starts with that context.
7. **Execution Monitoring.** Summary bullets with no links. Projects is one list ordered slipped, blocked, at risk, on track, with Draft nudge or Re-plan on every slipped, blocked, or at-risk row; it includes Linear projects and Jira epics with their source named, and only those active in the last 2 weeks. A disconnected or stale tracker shows as one callout with Reconnect directly below Projects, not its own section. Inferred work is grouped by theme with a one-line explanation and no buttons. Paste each prompt and check the flow.
8. **Changelog search.** At the bottom of Execution Monitoring, type in the search box and click an area chip. Entries filter, and "No matches." shows when nothing fits.
9. **Spec.** "Write a spec for <a real upcoming feature>". Check it asks one question at a time, stops at 2 to 5, writes the spec, and then tracks it in Devplan without asking, with a link. Run it again for an existing project and check it updates that project instead of creating a duplicate. Run it for an inferred project with no spec yet and check it asks before creating a planned project. It must never call a write tool with test content.
10. **Cycle Planning.** "Plan the next 6 weeks". Check it asks timeframe, then engineers (offering the active count), shows three distinct directions with a recommendation, and the plan's capacity adds up with an explicit 20% buffer. Planning a quarter splits it into cycles, each with a theme, goal, and project list in the summary; the timeline shows every committed item across the weeks; each project is closed by default, opens on click, and shows its estimate.
11. **Product context.** Ask an ordinary product question ("why are we building X?") without naming a skill. Check the answer cites sources and has no marketing.
12. **Scheduled refresh.** Trigger the scheduled task manually. Each dashboard updates in place (same link) and shows the new "Last refreshed" time. Trigger it again right away: nothing is republished and the reply is "No changes since the last refresh." With Devplan disconnected, the live version stays and the reply says it failed.
13. **Not connected.** With Devplan disconnected, in a normal (interactive) session, say "catch me up", "how are our projects going", "what slipped this week", "what are customers asking for", "plan the next 6 weeks" and "write a spec for X". Each should load its skill and ask "Do you have a Devplan account?" with setup's three options, with no fallback offer and no invented commands.

## When the server tools ship

When each ships, re-run:

- `get_workspace_context` / `save_workspace_context`: steps 2 and 4 (context loads, members link is exact, settings persist).
- `create_project`: step 9 (no stories generated unless asked, no duplicates on retry).
- `get_workspace_status`: steps 2 and 3.
- Project `inferred` flag and PR review times: steps 4 and 7.
