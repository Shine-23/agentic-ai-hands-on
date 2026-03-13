# Claude Code Starter

A hands-on demo project for learning how to configure and use [Claude Code](https://claude.ai/claude-code) — Anthropic's AI-powered CLI for software development.

## What This Project Covers

| Concept | Description |
|---|---|
| `CLAUDE.md` | Global and project-level instructions that shape Claude's behavior |
| `.claude/` config | Directory structure for skills, commands, and project settings |
| Custom skills | Reusable AI behaviors you can invoke in any conversation |
| Custom commands | Slash-style commands (e.g. `/explain-code`) triggered during sessions |
| MCP configuration | Connecting external tools to Claude via the Model Context Protocol |
| Sample app | Simple JavaScript files used to test code explanation and summarization |

## Project Structure

```
claude-code-starter/
├── CLAUDE.md                          # Global instructions for Claude
├── mcp.json                           # MCP server configuration
├── sample-app/
│   ├── app.js                         # Entry point using utils
│   └── utils.js                       # Helper functions (add, multiply)
└── .claude/
    ├── CLAUDE.md                      # Project-level Claude instructions
    ├── skills/
    │   └── summarize-project/
    │       └── SKILL.md               # Reusable skill: summarize the repo
    └── commands/
        └── explain-code.md            # Slash command: explain selected code
```

## Getting Started

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/claude-code) installed
- An Anthropic API key configured

### Run Claude in this project

```bash
cd claude-code-starter
claude
```

Claude will automatically read `CLAUDE.md` and `.claude/CLAUDE.md` for context.

## Using the Custom Commands & Skills

### `/explain-code`
Explains selected code in plain English — what it does, its inputs/outputs, and main logic.

**How to use:** Select code in your editor, then type `/explain-code` in the Claude Code session.

### `summarize-project` skill
Reads the repository structure and generates a short, beginner-friendly project summary.

**How to use:** Ask Claude to use the `summarize-project` skill in your session.

## MCP Configuration

The `mcp.json` file connects the `chrome-devtools-mcp` server, allowing Claude to interact with Chrome DevTools for browser debugging tasks.

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp"]
    }
  }
}
```

To use MCP servers, Claude Code must be launched in the project directory where `mcp.json` is present.

## Key Concepts Explained

**`CLAUDE.md`** — A markdown file Claude reads at the start of every session. Use it to set tone, coding standards, or project-specific instructions.

**Skills** — Stored in `.claude/skills/`, these are reusable behaviors defined in a `SKILL.md` file with a `name` and `description` frontmatter. Claude can invoke them on request.

**Commands** — Stored in `.claude/commands/`, these are slash commands (e.g. `/explain-code`) that trigger specific prompts when typed during a session.

**MCP (Model Context Protocol)** — A standard for connecting Claude to external tools like browsers, databases, or APIs.

---

## Prompts

Use these prompts inside a Claude Code session (`claude`) to explore the project hands-on.

### CLAUDE.md & Project Context
- "What instructions are you following for this project?"
- "What does the CLAUDE.md file in this repo tell you to do?"
- "What's the difference between the root CLAUDE.md and the one inside .claude/?"

### Code Explanation
- "Explain what `sample-app/app.js` does in simple terms."
- "What does the `add` function in `utils.js` take as input and return as output?"
- "Walk me through how `app.js` and `utils.js` work together."

### Project Summarization
- "Summarize this project for someone who has never used Claude Code before."
- "Use the `summarize-project` skill to describe this repo."
- "What is the purpose of each folder in this project?"

### Custom Commands & Skills
- "What custom commands are available in this project?"
- "Run `/explain-code` on the `multiply` function in `utils.js`."
- "What does the `summarize-project` skill do and how is it defined?"

### MCP & Configuration
- "What MCP servers are configured in this project?"
- "What would the `chrome-devtools-mcp` server allow you to do?"
- "How would you add a new MCP server to this project?"

### Extending the Project
- "Add a `subtract` function to `utils.js` and use it in `app.js`."
- "Create a new custom command called `/review-code` that checks code for potential bugs."
- "Write a new skill called `generate-tests` that creates unit tests for a given file."
- "Update the root CLAUDE.md to enforce a rule: always use `const` instead of `let`."
