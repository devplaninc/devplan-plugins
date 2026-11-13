# Testing the Devplan plugin

Every skill needs the Devplan connector. Test with a workspace that has at least one analyzed repo, plus Slack and a tracker if you can. For the new-user path, use an email that has never been used on Devplan.

Run `python3 scripts/sync.py` and `claude plugin validate plugins/devplan` before every release.

## Test script

Use a new chat for each step.

1. **Setup, new user.** Disconnect Devplan (or use a fresh account) and say "Set up Devplan". Check:
   - the welcome lists what they'll get, then the 5 steps
   - "What is Devplan?" explains in four lines; "No, create one" shows the five onboarding steps (account, company, repo plus other sources, graph build, come back) and the sign-up link
   - the connect steps match the surface you're on
2. **Setup, connected.** Say "Set up Devplan" with Devplan connected. Check:
   - the workspace summary names what Devplan can see and which dashboards are ready
   - company context is shown from Devplan, or drafted with "(inferred)" marks, and the one-click "Looks good, all of it"
   - the radar focus question is skipped when Claude already knows your role
   - one confirmation builds every ready dashboard, one at a time, and creates **one** weekday scheduled task with email on
   - the tour ends with a single, quiet Invite teammates line
3. **Graph still building.** On a workspace that just connected its first repo, run setup. It should explain that dashboards fill in as analysis finishes, and every dashboard should show the notice instead of empty filler.
4. **Each dashboard.** "Run my Daily Radar", "How are our projects going?", "Build my demand report", "What slipped this week?", "What shipped today?", "How fast are we shipping?". For each, check:
   - it uses the template: ink masthead, three-line Today, figures, then sections
   - every item links to a real source, with readable labels and no IDs
   - bots don't appear as people
   - light and dark mode, and phone width, look right
   - the footer's Invite teammates link opens your workspace's members page
5. **Daily Radar personalization.** Run it in a chat where Claude knows your role and projects, then in one where it doesn't. The first should open with "For you"; the second shows the team view and offers to tailor it.
6. **Demand Report.** Themes are parents, suggested projects are children with Write spec buttons. The market section has dated, linked competitor and trend items. Click Write spec, paste into a new chat, and check the spec starts with that context.
7. **Execution Monitoring.** Projects are ordered off track, at risk, quiet, on track. Inferred projects have Write spec, drifted ones Update spec, and the header has New project. Paste each prompt and check the spec flow.
8. **Changelog search.** Type in the search box and click an area chip. Entries filter, and "No matches." shows when nothing fits.
9. **Spec.** "Write a spec for <a real upcoming feature>". Check it asks one question at a time, stops at 2 to 5, writes the spec, and then tracks it in Devplan without asking, with a link. Run it again for an existing project and check it updates that project instead of creating a duplicate.
10. **Cycle Planning.** "Plan the next 6 weeks". Check it asks timeframe, then engineers (offering the active count), shows three distinct directions with a recommendation, and the plan's capacity adds up: in progress + new + stretch + buffer equals the capacity figure, and the "How this was sized" table shows its inputs.
11. **Product context.** Ask an ordinary product question ("why are we building X?") without naming a skill. Check the answer cites sources and has no marketing.
12. **Scheduled refresh.** Trigger the scheduled task manually. Each dashboard updates in place (same link), and the final message reads as a short email.

## When the server tools ship

See `docs/SERVER_SPEC.md`. When each ships, re-run:

- `get_workspace_context` / `save_workspace_context`: steps 2 and 4 (context loads, members link is exact, settings persist).
- `create_project`: step 9 (no stories generated unless asked, no duplicates on retry).
- `get_workspace_status`: steps 2 and 3.
- Project `inferred` flag and PR review times: steps 4 and 7.
