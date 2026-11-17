# Gemini CLI gallery

Gemini CLI's extension gallery indexes public GitHub repositories that contain a root `gemini-extension.json` and use the `gemini-cli-extension` topic.

Release checklist:

1. Keep `gemini-extension.json` at the repository root.
2. Publish a semantic version GitHub release matching the manifest version.
3. Keep the `gemini-cli-extension` GitHub topic attached.
4. Verify installation with `gemini extensions install https://github.com/MonologueInc/monologue-plugin`.

Gallery discovery runs on Google's schedule and can lag behind the repository release.
