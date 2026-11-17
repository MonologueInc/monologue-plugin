# OpenAI submission packet

## Listing

The listing, review test cases, and release notes live in [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json) and import with the plugin ZIP. The root `plugin.json` has no `extensions.com.openai` object, so OpenAI reads these settings from the Codex manifest.

- Name: Monologue
- Category: Productivity
- Short description: Search and review your notes
- MCP server: `https://api.monologue.to/mcp` (OAuth with Dynamic Client Registration)
- Website: `https://www.monologue.to`
- Support: `https://www.monologue.to/docs/support/contact-support`
- Privacy: `https://www.monologue.to/privacy`
- Terms: `https://www.monologue.to/terms`
- Logo and composer icon: `assets/logo.png`

## Tool annotations

| Tool | readOnlyHint | destructiveHint | openWorldHint |
| --- | --- | --- | --- |
| `list_recent_notes` | true | false | false |
| `search_notes` | true | false | false |
| `get_note` | true | false | false |
| `get_shared_note` | true | false | false |
| `set_note_share` | false | true | true |

`set_note_share` publishes a note at a public URL or revokes a live link, so it is open-world and destructive. It is idempotent and needs `notes:write`. Verify the live annotations in the portal's tool scan before submitting.

## Test cases

The five positive and three negative cases in `.codex-plugin/plugin.json` use the fictional notes that the backend script `scripts/seed_directory_reviewer.py` seeds into the reviewer account. Run each one with that account before recording the walkthrough, and turn sharing off again after the share case.

## Portal-only checklist

- Submit from an OpenAI account with Apps Management Write permission and verified developer or business identity.
- Complete the MCP domain challenge at `/.well-known/openai-apps-challenge`. Set the portal's token as `OAUTH__OPENAI_APPS_CHALLENGE_TOKEN` on the API and deploy.
- Enter the reviewer account and the video walkthrough URL in **Review details**. Never commit them here.
- Approve `notes:write` when connecting so the share test case works.
