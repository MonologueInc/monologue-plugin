# Monologue plugin

The official agent plugin for [Monologue](https://www.monologue.to). Search, review, and share your private voice notes from Codex, Claude Code, Cursor, Grok, Gemini CLI, and any client that supports the Agent Plugins specification.

Monologue connects over OAuth to `https://api.monologue.to/mcp`. Every result is scoped to the authenticated Monologue account. The only write action is turning a note's public share link on or off, and it needs a separate permission you approve.

## What it can do

- List recent notes with pagination.
- Search notes by text and date range.
- Retrieve a note, optionally including its transcript.
- Read a note someone shared with you or a public note opened by its share link.
- Turn a note's public share link on or off, if you approve the `notes:write` permission.
- Prepare for meetings, create follow-ups, and synthesize weekly reviews.

## Install

### Codex

```sh
codex plugin marketplace add MonologueInc/monologue-plugin
codex plugin add monologue@monologue
```

### Claude Code

```sh
claude plugin marketplace add MonologueInc/monologue-plugin
claude plugin install monologue@monologue
```

The Claude plugin lives in [`claude/`](claude/), a self-contained copy that holds only file types Claude's plugin directory accepts. Its skills, commands, logo, and license are copies of the shared files, and `make validate` fails if they drift.

### Cursor

Install Monologue from the Cursor Marketplace when the listing is approved. For local development, clone this repository and symlink it into Cursor's plugin directory:

```sh
git clone https://github.com/MonologueInc/monologue-plugin.git
mkdir -p ~/.cursor/plugins
ln -s "$(pwd)/monologue-plugin" ~/.cursor/plugins/monologue
```

### Grok

Install Monologue from the Grok plugin marketplace once the listing is approved. The Grok manifest is [`.grok-plugin/plugin.json`](.grok-plugin/plugin.json); it uses the same skills, commands, and [`.mcp.json`](.mcp.json) as Claude Code.

### Gemini CLI

```sh
gemini extensions install https://github.com/MonologueInc/monologue-plugin
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
| `get_shared_note` | Read a note shared with the user, or a public note by its share link. |
| `set_note_share` | Turn a note's public share link on or off. Owner only; needs `notes:write`. |

The plugin cannot create, edit, or delete notes. Sharing is the only change it can make, and only when the user asks for it.

## Authentication and privacy

The first MCP request opens Monologue's browser-based OAuth flow. Reading needs the `notes:read` scope. Sharing needs `notes:write`, which you approve on the consent screen; without it, the share tool returns an error and nothing changes. `offline_access` keeps you signed in. Credentials are managed by the host client and are not stored in this repository. Revoke access at any time under **Settings → Connected apps** in the Monologue web app.

- [Privacy policy](https://www.monologue.to/privacy)
- [Terms of service](https://www.monologue.to/terms)
- [Support](https://www.monologue.to/docs/support/contact-support)
- [MCP documentation](https://www.monologue.to/docs/integrations/mcp)

## Development

```sh
make validate
make validate-network
claude plugin validate claude --strict --profile directory
```

Marketplace submission materials live in [`submission/`](submission/). See [`CONTRIBUTING.md`](CONTRIBUTING.md) for release requirements.

## License

[MIT](LICENSE)
