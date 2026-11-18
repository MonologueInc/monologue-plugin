# Contributing

Issues and pull requests are welcome. Keep changes portable across Codex, Claude Code, Cursor, Grok, Gemini CLI, and the Agent Plugins specification.

Before opening a pull request:

1. Run `make validate`.
2. Run `make validate-network` when changing endpoints, public URLs, or authentication metadata.
3. After changing `skills/`, Markdown commands, `assets/logo.png`, or `LICENSE`, copy them into `claude/` (the license as `claude/LICENSE.txt`). Run `claude plugin validate claude --strict --profile directory` when changing the Claude plugin.
4. Update every vendor manifest and `CHANGELOG.md` for a release.
5. Never commit credentials, OAuth challenge tokens, or real note content.

Use Conventional Commit prefixes such as `feat:`, `fix:`, and `chore:`.
