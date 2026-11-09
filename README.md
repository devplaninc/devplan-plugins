# Devplan plugin for Claude and Codex

Daily Radar, Demand Report, Spec, Engineering Analytics and more, built from your team's tools. Connect Devplan to upgrade every skill to Weaver's knowledge graph.

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

| Skill | Tier | Without Devplan sources | With Devplan sources |
|---|---|---|---|
| `devplan-setup` | Free | Detects and connects your tools, sets up a Project and a scheduled radar | Same |
| `devplan-product-context` | Free | Ambient: grounds everyday product questions in your connected tools | Grounds them in Weaver's graph |
| `daily-radar` | Free | Built from GitHub, Linear or Jira, Slack | Weaver graph, full attribution |
| `demand-report` | Free | Recurring demand, uncaptured asks and blockers from support, calls, Slack, tracker | Deduplicated and linked to projects and code |
| `spec` | Free | Discovery questions, product and technical plan, estimate from tracker history | Full product graph, estimates from real velocity |
| `eng-analytics` | Free | Cycle time, review latency, throughput, WIP from GitHub and tracker | Every PR joined to project and team, full flow |
| `suggested-projects` | Premium | Preview: 3 themes | Full suggestions with evidence and owners |
| `customer-release-brief` | Premium | Preview: tracker-linked releases only | Releases matched to every customer who asked, with drafts |
| `stale-commitment-watch` | Premium | Preview: overdue and blocked tracker items | Commitments from Slack, meetings and calls, tracked to the work |
| `changelog` | Premium | Preview: merged PRs by repo | Plain-language changelog by feature, availability verified |

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
