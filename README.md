# Monologue plugin

The official agent plugin for [Monologue](https://www.monologue.to). Search and review your private voice notes from Codex, Claude Code, Cursor, Gemini CLI, and any client that supports the Agent Plugins specification.

Monologue connects over OAuth to `https://api.monologue.to/mcp`. The integration is read-only and every result is scoped to the authenticated Monologue account.

## What it can do

- List recent notes with pagination.
- Search notes by text and date range.
- Retrieve a note, optionally including its transcript.
- Prepare for meetings, create follow-ups, and synthesize weekly reviews.

## Install

### Codex

```sh
codex plugin marketplace add EveryInc/monologue-plugin
codex plugin add monologue@monologue
```

### Claude Code

```sh
claude plugin marketplace add EveryInc/monologue-plugin
claude plugin install monologue@monologue
```

### Cursor

Install Monologue from the Cursor Marketplace when the listing is approved. For local development, clone this repository and symlink it into Cursor's plugin directory:

```sh
git clone https://github.com/EveryInc/monologue-plugin.git
mkdir -p ~/.cursor/plugins
ln -s "$(pwd)/monologue-plugin" ~/.cursor/plugins/monologue
```

### Gemini CLI

```sh
gemini extensions install https://github.com/EveryInc/monologue-plugin
```

Gemini's extension gallery discovers this repository through the `gemini-cli-extension` GitHub topic.

### Agent Plugins clients

The portable entry points are [`plugin.json`](plugin.json) and [`mcp.json`](mcp.json).

## Available MCP tools

| Tool | Purpose |
| --- | --- |
| `list_recent_notes` | List the authenticated user's recent notes. |
| `search_notes` | Search the user's notes by text and optional date filters. |
| `get_note` | Retrieve one owner-scoped note and optionally its transcript. |

The plugin cannot create, edit, delete, or share notes.

## Authentication and privacy

The first MCP request opens Monologue's browser-based OAuth flow. Access is limited to the `notes:read` scope. Credentials are managed by the host client and are not stored in this repository.

- [Privacy policy](https://www.monologue.to/privacy)
- [Terms of service](https://www.monologue.to/terms)
- [Support](https://www.monologue.to/docs/support/contact-support)
- [MCP documentation](https://www.monologue.to/docs/integrations/mcp)

## Development

```sh
make validate
make validate-network
claude plugin validate . --strict
```

Marketplace submission materials live in [`submission/`](submission/). See [`CONTRIBUTING.md`](CONTRIBUTING.md) for release requirements.

## License

[MIT](LICENSE)
