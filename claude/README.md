# Monologue for Claude

Search, review, and share your [Monologue](https://www.monologue.to) voice notes from Claude Code.

This folder is the Claude plugin. It connects over OAuth to Monologue's hosted MCP server at `https://api.monologue.to/mcp`, and every result is scoped to the signed-in Monologue account. The only write action is turning a note's public share link on or off, and it needs the separate `notes:write` permission you approve on the consent screen.

## Install

```sh
claude plugin marketplace add MonologueInc/monologue-plugin
claude plugin install monologue@monologue
```

The first MCP request opens Monologue's sign-in page in your browser.

## What it includes

- MCP tools: `list_recent_notes`, `search_notes`, `get_note`, `get_shared_note`, and `set_note_share`.
- Skills: `monologue-context`, `meeting-prep`, `meeting-follow-up`, and `weekly-review`.
- Commands: `/monologue:meeting-prep`, `/monologue:meeting-follow-up`, and `/monologue:weekly-review`.

The plugin cannot create, edit, or delete notes. You can revoke access at any time under **Settings → Connected apps** in the Monologue web app.

## Links

- [Privacy policy](https://www.monologue.to/privacy)
- [Terms of service](https://www.monologue.to/terms)
- [Support](https://www.monologue.to/docs/support/contact-support)
- [MCP documentation](https://www.monologue.to/docs/integrations/mcp)

## License

[MIT](LICENSE.txt)
