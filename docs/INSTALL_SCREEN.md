# Onboarding: final step "Add Devplan to your AI"

Shown at the end of Devplan onboarding, after the user connects a repository. The graph keeps building in the background.

## Header

**Add Devplan to your AI**
Your dashboards, specs, and product answers, inside the AI you already use.

## Tabs

### Claude (web and desktop)
1. Go to **Customize > Plugins > Add > Add marketplace** and paste:
   `devplaninc/devplan-plugins` [Copy]
2. Find **Devplan** and select **Add**.
3. In a new chat, say **"Set up Devplan"**. You're already signed in, so connecting is one click.

[GIF: 20 seconds]

### Claude Code
```
/plugin marketplace add devplaninc/devplan-plugins
/plugin install devplan@devplan
```
[Copy] Then say **"Set up Devplan"**.

### ChatGPT and Codex desktop
1. Open **Plugins**, add a marketplace, and paste `devplaninc/devplan-plugins` [Copy]
2. Install **Devplan**.
3. Say **"Set up Devplan"** and connect when asked.

### Codex CLI
```
codex plugin marketplace add devplaninc/devplan-plugins
```
[Copy] Then type `/plugins` and install **Devplan**.

## Footer

"Not using an AI app? Open Devplan in your browser" (link to the web app).

## Tracking

Fire `install_screen_viewed` with `{tab, connected_sources}`. Measure activation as the first Devplan MCP call from that user within 24 hours.
