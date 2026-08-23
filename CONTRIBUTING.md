# Contributing

Issues and pull requests are welcome. Keep changes portable across Codex, Claude Code, Cursor, Gemini CLI, and the Agent Plugins specification.

Before opening a pull request:

1. Run `make validate`.
2. Run `make validate-network` when changing endpoints, public URLs, or authentication metadata.
3. Run `claude plugin validate . --strict` when changing Claude manifests.
4. Update every vendor manifest and `CHANGELOG.md` for a release.
5. Never commit credentials, OAuth challenge tokens, or real note content.

Use Conventional Commit prefixes such as `feat:`, `fix:`, and `chore:`.
