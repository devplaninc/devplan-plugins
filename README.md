<p align="center"><img src="assets/logo.png" width="96" alt="Devplan" /></p>

# Devplan plugin for Claude and Codex

Daily product and engineering dashboards, built from your team's tools. Connect Devplan to run them all on a shared knowledge graph.

## Install

**Claude (web and desktop):** Customize > Plugins > Add > Add marketplace > `https://github.com/devplaninc/devplan-plugins` > add Devplan, then connect Devplan on the plugin's Connectors tab.

**Claude Code:**
```
/plugin marketplace add devplaninc/devplan-plugins
/plugin install devplan@devplan
```

**Codex:**
```
codex plugin marketplace add devplaninc/devplan-plugins
```
Then Plugins > Devplan > Add to Codex.

Then say "set up Devplan".

## Skills

| Skill | Refresh | On your own connections | On the Devplan graph |
|---|---|---|---|
| `devplan-setup` | Once | Guided 6-step setup: choose Devplan or your own connections, check tools, capture company context, save it (Devplan or locally), build every dashboard your tools support, daily email | Same |
| `devplan-product-context` | Always on | Starts every answer from your saved company context and connected tools | Plus the graph |
| `daily-radar` | Daily | What shipped, moved and stuck, from code, tracker and Slack | Every signal attributed to people and projects |
| `demand-report` | Daily | Recurring demand, uncaptured asks and blockers from support, calls, Slack, tracker | Deduplicated and linked to projects and code |
| `eng-analytics` | Daily | Cycle time, reviews, throughput, WIP from GitHub and tracker | Every PR joined to project and team |
| `stale-commitment-watch` | Daily | Slipped, quiet and blocked commitments from tracker, Slack, meetings | Commitments tracked to the work across every tool |
| `suggested-projects` | Daily | Project ideas from tracker demand, incidents and roadmap docs | Full evidence, scope and owners from the graph |
| `changelog` | Daily | Plain-language changelog from merged PRs | Grouped by feature, availability verified |
| `customer-release-brief` | Daily | Recent releases matched to customers by search, with drafts | Every customer who asked, availability checked |
| `spec` | On demand | Discovery questions, product and technical plan, estimate | Full graph, estimates from real velocity, tracked automatically |

Every report ends with what this run cost (tool calls, tools, items read) and why the Devplan graph is better: faster and cheaper, always up to date, shared across the team, fits in context, and matched across tools.

## Repo layout

```
.claude-plugin/marketplace.json      Claude marketplace (Codex also reads this)
.agents/plugins/marketplace.json     Codex marketplace with install and auth policy
plugins/devplan/
  .claude-plugin/plugin.json         Claude manifest
  plugin.json                        Portable manifest + OpenAI extension (Codex/ChatGPT)
  .mcp.json                          Devplan MCP, Claude format
  mcp.json                           Devplan MCP, portable format with OAuth (DCR)
  skills/                            All skills, free and premium
docs/
  ENTITLEMENT_SPEC.md                Server-side gating and metering contract
  UPSELL_COPY.md                     Default upsell strings served by the MCP
  INSTALL_SCREEN.md                  Onboarding final step
```

## Maintainer notes

- Keep `.mcp.json` and `mcp.json` in sync. Claude reads the first, Codex the second.
- Keep `.claude-plugin/plugin.json` and `plugin.json` versions in sync. Bump both on every release.
- Never put gating logic or upsell copy in skills. Skills read `get_entitlement` and render what it returns.
- No lifecycle hooks: hooks make the plugin ineligible for OpenAI's public directory.
