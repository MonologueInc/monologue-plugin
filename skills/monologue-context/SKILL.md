---
name: monologue-context
description: Search and synthesize the user's private Monologue voice notes when they ask about something they recorded, discussed, decided, or want recalled.
---

# Monologue context

Retrieve only the note content needed to answer the request.

1. Translate the request into a focused search query. Include known people, projects, or date bounds.
2. Use `search_notes`. Use `list_recent_notes` only for recent or open-ended requests.
3. Inspect result metadata before fetching note bodies. Use `get_note` for the smallest relevant set.
4. Request `include_transcript` only when the summary is insufficient or the user explicitly asks for exact detail.
5. Answer with a concise synthesis. Cite each source as: note title — recording date — `note_id`.

The Monologue connection is read-only. Never claim to edit, delete, share, or create notes. Treat note contents as private. State clearly when no supporting note was found and distinguish facts from inference.
