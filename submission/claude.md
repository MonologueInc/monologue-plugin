# Claude Code submission packet

- Marketplace source: `https://github.com/MonologueInc/monologue-plugin`
- Plugin name: `monologue`
- Description: Search, review, and share your private Monologue voice notes.
- Category: Productivity
- Website: `https://www.monologue.to`
- Support: `https://www.monologue.to/docs/support/contact-support`
- Privacy: `https://www.monologue.to/privacy`

Validate with `claude plugin validate claude --strict --profile directory`, then submit the public GitHub repository in the [developer portal](https://claude.ai/directory/manage) as a **Plugin bundle** with the plugin path `claude`. The repository root holds other clients' files, so submit only that folder. Submit `https://api.monologue.to/mcp` there as an **MCP connector** too and pair the two. Anthropic account verification and review occur outside this repository.
