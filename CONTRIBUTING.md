# Contributing

## Repo layout

```
.claude-plugin/marketplace.json      Claude marketplace (Codex also reads this)
.agents/plugins/marketplace.json     Codex marketplace with install and auth policy
plugins/devplan/
  .claude-plugin/plugin.json         Claude manifest
  plugin.json                        Portable manifest + OpenAI extension (Codex/ChatGPT)
  .mcp.json                          Devplan MCP, Claude format
  mcp.json                           Devplan MCP, portable format with OAuth (DCR)
  skills/                            The skills
shared/
  dashboard-template.html            The dashboard design every dashboard skill uses
  blocks/                            Text shared across skills
scripts/sync.py                      Copies shared blocks and the template into the skills
TESTING.md                           Release test script
```

## Maintainer notes

- Edit shared text in `shared/`, then run `python3 scripts/sync.py`. Don't edit the copies inside skills between `<!-- shared:... -->` markers or in `references/dashboard-template.md`.
- Keep `.mcp.json` and `mcp.json` in sync. Claude reads the first, Codex the second.
- Keep the version in sync in four places: both plugin manifests and both version fields in `.claude-plugin/marketplace.json`. Bump all four on every release.
- Skills use newer server tools (`get_workspace_context`, `save_workspace_context`, `create_project`) when they exist and fall back to existing tools until then. Nothing needs to change in the plugin when they ship.
- Keep skill descriptions short and keep their trigger phrases: every description is loaded into every session. Check the cost with `claude plugin details devplan@devplan`.
- Never put real customer or workspace numbers in skill examples. Models echo examples into output.
- No lifecycle hooks: hooks make the plugin ineligible for OpenAI's public directory.
- Before every release, run `python3 scripts/sync.py` and `claude plugin validate plugins/devplan`, then follow `TESTING.md`.
