# Monologue

Use the Monologue MCP server to search and retrieve the user's voice notes. Access is read-only and scoped to the authenticated user's account.

- Use `list_recent_notes` to discover recent notes.
- Use `search_notes` when the user supplies a subject, person, date, or phrase.
- Use `get_note` only after identifying a relevant note. Request the transcript only when necessary.
- Cite the note title, recording date, and `note_id` when presenting information from a note.
- Separate explicit facts from your own inference. Never invent missing note content.
- Do not expose private note content beyond what the user asked for.
