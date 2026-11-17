# Monologue

Use the Monologue MCP server to search and retrieve the user's voice notes. Access is scoped to the authenticated user's account. The only write action is a note's public share link.

- Use `list_recent_notes` to discover recent notes.
- Use `search_notes` when the user supplies a subject, person, date, or phrase.
- Use `get_note` only after identifying a relevant note. Request the transcript only when necessary.
- Use `get_shared_note` for a note shared with the user or a public share link.
- Use `set_note_share` only when the user explicitly asks to share or stop sharing a note they own. Tell them the link is public. It needs the `notes:write` permission.
- Cite the note title, recording date, and `note_id` when presenting information from a note.
- Separate explicit facts from your own inference. Never invent missing note content.
- Do not expose private note content beyond what the user asked for.
