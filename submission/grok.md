# Grok submission packet

Grok reads [`.grok-plugin/plugin.json`](../.grok-plugin/plugin.json), the `skills/` and `commands/` folders, and [`.mcp.json`](../.mcp.json).

1. Submit the marketplace form at `https://x.ai/bot/marketplace/submit-a-plugin`. Use `https://github.com/MonologueInc/monologue-plugin` as the repository and `https://www.monologue.to/bimi/logo.svg` as the logotype (1:1, with a background plate).
2. Open a pull request to `xai-org/plugin-marketplace` that adds a remote entry to `.grok-plugin/marketplace.json`. Pin `source.sha` to a full 40-character commit on `main`. Then run `python3 scripts/generate-plugin-index.py`, `python3 scripts/validate-catalog.py`, and `python3 scripts/generate-plugin-index.py --check`.
3. For a release, bump the pinned `sha`.

Never put reviewer credentials in the form's public fields or in this repository.
