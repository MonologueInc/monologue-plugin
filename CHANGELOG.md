# Changelog

## 1.1.0 — 2026-11-17

- Add the Grok adapter (`.grok-plugin/plugin.json`).
- Document public share links: with the `notes:write` permission, `set_note_share` turns a note's public share link on or off, and `get_shared_note` reads shared and public notes.
- Add OpenAI review test cases, publication notes, a support URL, and a composer icon to the Codex manifest.
- Remove `skills`, `commands`, and `mcpServers` from the portable `plugin.json`, which the Agent Plugins schema does not allow. Portable clients find `skills/` and `mcp.json` on their own.
- Point repository URLs at `MonologueInc/monologue-plugin`.

## 1.0.0 — 2026-08-23

- Add portable Agent Plugins manifests.
- Add Codex, Claude Code, Cursor, and Gemini CLI adapters.
- Add read-only Monologue MCP integration and OAuth configuration.
- Add meeting preparation, meeting follow-up, weekly review, and general context skills.
- Add marketplace submission packets and automated validation.
