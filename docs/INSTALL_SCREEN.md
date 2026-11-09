# Onboarding: final step "Add Devplan to your AI"

Shown after sign-in, whether the user connected sources or chose "Skip for now".

## Header

**Add Devplan to Claude or Codex**
Your dashboards run inside the AI you already use.

If the user connected sources, add a badge: "$100 in credits added."

## Tabs

### Claude (web and desktop)
1. Open **Settings > Customize > Plugins**.
2. On the **Added** tab, click **Add Marketplace > Add from a Repository** and paste:
   `https://github.com/devplaninc/devplan-plugins` [Copy]
3. Click **Sync**, then install **Devplan**.
4. When prompted, click **Connect** to sign in to Devplan. You're already signed in, so it's one click.
5. Ask Claude: **"Run my Daily Radar"**

[GIF: 20 seconds]

### Claude Code
```
/plugin marketplace add devplaninc/devplan-plugins
/plugin install devplan@devplan
```
[Copy] Then run `/mcp`, select **devplan**, and authenticate.

### Codex
```
codex plugin marketplace add devplaninc/devplan-plugins
```
[Copy] Then open **Plugins > Devplan > Add to Codex** and connect when prompted.

## Footer

"Not using Claude or Codex? Open Devplan in your browser" (link to the web app).

## Tracking

Fire `install_screen_viewed` with `{tab, connected_sources}`. Measure activation as the first `get_entitlement` call from that user within 24 hours.
