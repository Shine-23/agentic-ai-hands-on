# Agentic AI — Hands-On

A hands-on learning repository for building agentic AI applications with [Claude Code](https://claude.ai/claude-code) and the [Anthropic API](https://docs.anthropic.com). This repo contains three progressive projects — from learning Claude Code fundamentals to building a production-ready AI planning assistant.

---

## Projects

| Project | Description |
|---|---|
| [`claude-code-starter/`](claude-code-starter/) | Learn Claude Code configuration: CLAUDE.md, skills, commands, and MCP |
| [`practice-folder/`](practice-folder/) | Recreate website designs using Tailwind CSS and iterative screenshot comparison |
| [`DevProject_AI/`](DevProject_AI/) | AI-powered engineering planning assistant built with FastAPI and the Claude API |

---

## 1. Claude Code Starter

A beginner-friendly demo for exploring how Claude Code is configured and extended.

**What I learnt:**
- How `CLAUDE.md` shapes Claude's behavior at global and project level
- How to create custom **skills** (reusable AI behaviors)
- How to create custom **slash commands** (e.g. `/explain-code`)
- How to connect external tools via **MCP** (Model Context Protocol)

**Sample prompts to explore:**
- `"Explain what sample-app/app.js does in simple terms."`
- `"Use the summarize-project skill to describe this repo."`
- `"What MCP servers are configured and what can they do?"`

---

## 2. Practice Folder — Website Design Recreation

An exercise project for pixel-accurate website recreation using Tailwind CSS and Puppeteer.

**What I learnt:**
- How to structure `.claude/rules/` for modular Claude instructions
- How to run an iterative screenshot → compare → fix loop with Claude
- How to use Puppeteer for automated page capture

**Workflow:**
1. Provide a reference screenshot
2. Claude generates an `index.html` using Tailwind CSS (via CDN)
3. Puppeteer captures the rendered page
4. Claude compares and fixes mismatches (spacing, fonts, colors, layout)
5. Repeat until within ~2–3px of the reference

---

## 3. DevProject AI — Engineering Planning Assistant

An AI-powered assistant that converts rough product requirements into structured, implementation-ready engineering plans.

**Problem it solves:** The gap between "I have an idea" and "I know what to build first." DevProject AI acts as a senior engineering collaborator — thinking through scope, architecture, and risk before a single line of code is written.

**Target users:** Solo developers, startup teams, tech leads, engineering managers, hackathon builders.

### Features

| Feature | Description |
|---|---|
| Requirement analysis | Extracts goals, users, features, and constraints from raw input |
| Scope definition | Separates MVP from future enhancements |
| Architecture planning | Proposes a stack-aware high-level architecture |
| API contract drafting | Drafts endpoints with methods, payloads, and auth rules |
| Task decomposition | Breaks work into milestones, tasks, and subtasks |
| Risk review | Surfaces ambiguity, unknowns, and integration risks |
| Implementation sequencing | Recommends a practical build order |

### Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| AI layer | Claude API (Anthropic) |
| Frontend | Lovable |
| Database | PostgreSQL / SQLite |
| Auth | JWT / OAuth2 |
| Containerization | Docker |
| Deployment | Railway |
| Env management | python-dotenv |

### Custom Agent

The **Engineering Planning Agent** is defined in [`.claude/agents/ENGINEERING_PLANNING_AGENT.md`](DevProject_AI/.claude/agents/ENGINEERING_PLANNING_AGENT.md). It follows a 9-step workflow:

1. Requirement analysis
2. Assumptions
3. Scope definition
4. Architecture planning
5. Data modeling
6. API drafting
7. Task decomposition
8. Risk review
9. Final structured output (JSON with 10 fields)

---

## Key Concepts

**`CLAUDE.md`** — A markdown file Claude reads at the start of every session. Sets tone, coding standards, and project-specific instructions. Supports three layers: personal (`~/.claude/CLAUDE.md`), project (`.claude/CLAUDE.md`), and enterprise.

**Skills** — Reusable AI behaviors stored in `.claude/skills/<name>/SKILL.md`. Invoked by asking Claude to use them by name.

**Commands** — Slash commands stored in `.claude/commands/<name>.md`. Triggered during a session by typing `/command-name`.

**Agents** — AI assistants defined in `.claude/agents/<name>.md` that perform multi-step tasks using tools, file reads, and reasoning.

**MCP (Model Context Protocol)** — A standard for connecting Claude to external tools like browsers, databases, issue trackers, and APIs. Configured in `mcp.json`.

---

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/claude-code) installed
- An [Anthropic API key](https://console.anthropic.com/)
- Node.js (for `practice-folder`)
- Python 3.10+ (for `DevProject_AI`)

---
