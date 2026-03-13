# Agentic AI

## What is CLAUDE.md ?

`CLAUDE.md` is a configuration or instruction file used when working with Claude AI tools. It contains guidelines that help the AI understand how to interact with a project. It acts like a navigation guide or steering direction for the AI, helping it understand how to behave in the project. 

The file can include information such as:
- project structure
- coding guidelines
- preferred tools or frameworks
- instructions on how the AI should assist with the codebase

## What is .claude directory ?

The .claude directory is a folder used to store configuration and support files for Claude AI tools when working in a project.
The .claude directory helps organize all AI-related settings and keeps them separate from the main application code.

Claude can use instructions from three different CLAUDE.md layers that merge together.

- Personal Layer (~/.claude/CLAUDE.md): User’s global preferences that apply to all projects.

- Project Layer (.claude/CLAUDE.md): Project-specific instructions stored inside the repository.

- System / Enterprise Layer: Organization-level rules managed by the system or company.

## Auto-Memory

Claude has an auto-memory feature that allows it to remember information across sessions.

- Memory is stored in: `~/.claude/projects/<project-hash>/memory/MEMORY.md`
- Claude reads the first part of this file when a new session starts.
- During a session, it can store useful notes such as patterns, debugging insights, and preferences.
- Additional topic files (e.g., `debugging.md`, `patterns.md`) can be linked from MEMORY.md.

This memory is separate from `CLAUDE.md`, which contains instructions.

## Agents

Agents are AI assistants designed to perform specific tasks automatically.
They can understand instructions, use tools, and execute multiple steps to complete a task.

An agent can:
- read and analyze files
- generate or modify code
- run commands
- automate workflows

## Skills (Custom Slash Commands)

Skills are custom slash commands that extend Claude’s capabilities.
They allow you to create reusable commands that perform specific tasks automatically.
Where they are stored:

- `.claude/skills/<name>/SKILL.md` → project-level skills

- `~/.claude/skills/<name>/SKILL.md` → personal skills

- `.claude/commands/<name>.md` → legacy command format