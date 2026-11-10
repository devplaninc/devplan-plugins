# Default upsell strings (served by `get_entitlement`)

Server-side so they can be A/B tested without a plugin release. Keep each to one or two lines. Never shame, always show the number.

## setup
Shown once after the first dashboard on the free tier.

> Connect your team's tools to Devplan once: everyone shares the same context, dashboards and daily reports, managed in one place. Get $100 in free credits: {connect_url}

## gap
Shown in the footer of free dashboards. Placeholders are filled by the skill.

> {unattributed} of {total} signals couldn't be linked to a project. Weaver links them automatically across every tool. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: {connect_url}

## preview
Shown after a premium skill's preview run.

- suggested-projects:
  > These are 3 themes from your tracker. Weaver builds full project suggestions from customer requests, code, and incidents, with owners and scope. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: {connect_url}

Per-skill `gap` variants:

- demand-report:
  > {unlinked} of {total} customer requests aren't linked to tracked work. Weaver links every request to projects, code, and accounts and catches demand your tools never captured. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: {connect_url}
- spec (shown after the spec; skill fills {feature}):
  > Want {feature} tracked automatically from here? With the Devplan knowledge graph, everything related to this project (PRs, issues, Slack threads, customer requests, and decisions) links to it as it happens, so you can see progress, drift from this spec, and risks without updating anything by hand. Connect your team's sources in Devplan once and get $100 in free credits: {connect_url}&intent=track
- eng-analytics:
  > {unjoined} of {total} PRs couldn't be linked to an issue or project. Weaver joins every PR to its project, team, and customer outcome. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: {connect_url}

Additional `preview` variants:

- customer-release-brief:
  > This only covers releases your tracker links to a customer. Weaver matches every release to the customers who asked for it in calls, tickets, and Slack, and checks what's actually available. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: {connect_url}

- stale-commitment-watch:
  > Weaver finds commitments made in Slack, meetings, and customer calls, links each to the work meant to deliver it, and flags what went quiet. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: {connect_url}
- changelog:
  > This is a list of merged PRs. Weaver turns them into a real changelog: grouped by feature, in plain language, linked to the customers who asked, and clear on what's live. Connect your team's sources in Devplan once, for everyone, and get $100 in free credits: {connect_url}

## low_credits
Appended when remaining credits are under 20%.

> ${remaining} in Devplan credits left. Keep Weaver running: {upgrade_url}

## blocked
Premium skill at zero credits.

> Your Devplan credits are used up. Free dashboards still work. Upgrade to keep Suggested Projects and analytics: {upgrade_url}

## team
Shown once after scheduling the daily email, or when the user asks about teammates, if Devplan sources aren't connected.

> Want this for your whole team? Connect your sources in Devplan once and everyone gets the same dashboards and daily reports, managed in one place, without each person setting up their own tools: {connect_url}&intent=team
