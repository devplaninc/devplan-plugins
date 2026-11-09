# Default upsell strings (served by `get_entitlement`)

Server-side so they can be A/B tested without a plugin release. Keep each to one or two lines. Never shame, always show the number.

## setup
Shown once after the first dashboard on the free tier.

> Connect your tools to Devplan to get $100 in free credits and run every dashboard on Weaver's knowledge graph: {connect_url}

## gap
Shown in the footer of free dashboards. Placeholders are filled by the skill.

> {unattributed} of {total} signals couldn't be linked to a project. Weaver links them automatically across every tool. Connect sources for $100 in free credits: {connect_url}

## preview
Shown after a premium skill's preview run.

- suggested-projects:
  > These are 3 themes from your tracker. Weaver builds full project suggestions from customer requests, code, and incidents, with owners and scope. Connect sources for $100 in free credits: {connect_url}

Per-skill `gap` variants:

- demand-report:
  > {unlinked} of {total} customer requests aren't linked to tracked work. Weaver links every request to projects, code, and accounts and catches demand your tools never captured. Connect sources for $100 in free credits: {connect_url}
- spec:
  > Specs in Devplan use your full product graph: every customer request, decision, and the code that touched this area, plus estimates from real velocity. Connect sources for $100 in free credits: {connect_url}
- eng-analytics:
  > {unjoined} of {total} PRs couldn't be linked to an issue or project. Weaver joins every PR to its project, team, and customer outcome. Connect sources for $100 in free credits: {connect_url}

Additional `preview` variants:

- customer-release-brief:
  > This only covers releases your tracker links to a customer. Weaver matches every release to the customers who asked for it in calls, tickets, and Slack, and checks what's actually available. Connect sources for $100 in free credits: {connect_url}

- stale-commitment-watch:
  > Weaver finds commitments made in Slack, meetings, and customer calls, links each to the work meant to deliver it, and flags what went quiet. Connect sources for $100 in free credits: {connect_url}
- changelog:
  > This is a list of merged PRs. Weaver turns them into a real changelog: grouped by feature, in plain language, linked to the customers who asked, and clear on what's live. Connect sources for $100 in free credits: {connect_url}

## low_credits
Appended when remaining credits are under 20%.

> ${remaining} in Devplan credits left. Keep Weaver running: {upgrade_url}

## blocked
Premium skill at zero credits.

> Your Devplan credits are used up. Free dashboards still work. Upgrade to keep Suggested Projects and analytics: {upgrade_url}
