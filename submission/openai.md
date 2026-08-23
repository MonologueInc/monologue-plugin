# OpenAI submission packet

## Listing

- Name: Monologue
- Category: Productivity
- Short description: Search and review your private Monologue voice notes.
- Long description: Connect Monologue to ChatGPT and Codex to find prior conversations, prepare for meetings, create follow-ups, and synthesize weekly themes. The integration is OAuth-authenticated, owner-scoped, and read-only.
- MCP server: `https://api.monologue.to/mcp`
- Website: `https://www.monologue.to`
- Support: `https://www.monologue.to/docs/support/contact-support`
- Privacy: `https://www.monologue.to/privacy`
- Terms: `https://www.monologue.to/terms`
- Logo: `assets/logo.png`

## Required server declarations

Declare each exposed MCP tool with `readOnlyHint: true`, `destructiveHint: false`, and the appropriate `openWorldHint`. Verify the final annotations in the live tool schema before submitting.

## Positive test cases

1. List my five most recent Monologue notes and show title, date, and note ID.
2. Find notes where I discussed onboarding and summarize the recurring themes.
3. Retrieve the latest note about Acme and identify explicitly assigned follow-ups.
4. Prepare me for a meeting with Jordan using notes from the last 90 days.
5. Review this week's notes and separate recorded commitments from suggested next steps.

## Negative test cases

1. Delete my latest Monologue note. Expected: explain that the integration is read-only and do not claim success.
2. Show another Monologue user's private notes. Expected: refuse; results are owner-scoped.
3. Guess the transcript of a note that search did not return. Expected: say that no supporting note was found and do not invent content.

## Portal-only checklist

- Submit from an OpenAI account with Apps Management Write permission and verified developer or business identity.
- Complete the MCP domain challenge at `/.well-known/openai-apps-challenge` using the token supplied by the portal.
- Provide a dedicated reviewer account only through the portal if requested.
- Re-run the live positive and negative tests and confirm tool annotations immediately before submission.
