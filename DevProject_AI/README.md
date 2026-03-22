# DevProject AI

An AI-powered engineering planning assistant that converts rough product requirements into task breakdowns, architecture notes, API drafts, and implementation plans.

---

## Problem
Developers often start with a product idea but lack a structured engineering plan to implement it. The gap between "I have an idea" and "I know what to build first" slows teams down and leads to poor architectural decisions made under pressure.

DevProject AI fills that gap — acting as a senior engineering collaborator that thinks through scope, architecture, and risk before a single line of code is written.

---

## Users
- Solo developers
- Startup teams
- Tech leads
- Engineering managers
- Hackathon builders

---

## Core Features

| Feature | Description |
|---|---|
| Requirement analysis | Extracts goals, users, features, and constraints from raw input |
| Scope definition | Separates MVP from future enhancements |
| Architecture planning | Proposes a stack-aware high-level architecture |
| API contract drafting | Drafts endpoints with methods, payloads, and auth rules |
| Task decomposition | Breaks work into milestones, tasks, and subtasks |
| Risk review | Surfaces ambiguity, unknowns, and integration risks |
| Implementation sequencing | Recommends practical build order |

---

## Custom Agent
**Engineering Planning Agent** — defined in `.claude/agents/ENGINEERING_PLANNING_AGENT.md`

The agent follows the workflow defined in `.claude/skills/SKILL.md` and is powered by the Claude API.

---

## MCP usage
MCP tools extend the agent with live context:

| Tool category | Purpose |
|---|---|
| Repo / file tools | Read existing code and structure before planning |
| Docs tools | Pull in specs, READMEs, or external documentation |
| Issue tracker tools | Check existing tickets to avoid duplicating planned work |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Lovable |
| Backend | FastAPI (Python) |
| AI layer | Claude API (Anthropic) |
| Database | PostgreSQL / SQLite |
| Auth | JWT / OAuth2 |
| Containerization | Docker |
| Deployment | Railway |
| Env management | python-dotenv |

---

## Project Structure

```
DevProject_AI/
├── .claude/
│   ├── CLAUDE.md                          # Claude Code instructions
│   ├── skills/
│   │   └── SKILL.md                       # Agent workflow definition
│   └── agents/
│       └── ENGINEERING_PLANNING_AGENT.md  # Agent role and behavior
├── backend/
│   ├── app/               # FastAPI app and agent logic
│   │   └── agent_prompt.py  # Agent system prompt
│   ├── main.py            # Entry point
│   └── requirements.txt
├── frontend/              # Lovable frontend
├── docs/
│   └── NOTES.md
└── README.md
```

---

## Related Files
- [`.claude/skills/SKILL.md`](.claude/skills/SKILL.md) — full agent workflow
- [`.claude/agents/ENGINEERING_PLANNING_AGENT.md`](.claude/agents/ENGINEERING_PLANNING_AGENT.md) — agent role and system prompt definition
- [`backend/app/agent_prompt.py`](backend/app/agent_prompt.py) — agent system prompt used in code
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md) — Claude Code project instructions
