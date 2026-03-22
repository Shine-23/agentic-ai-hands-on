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

## MCP Tools
Three tools enrich the AI plan with real project context:

| Tool | Purpose |
|---|---|
| `repo_tool` | Scans local directory or clones a GitHub repo (supports tree/subdir URLs) |
| `docs_tool` | Fetches documentation from a URL or local file |
| `shell_tool` | Runs shell commands and captures output (e.g. `pip list`) |

All three tools feed their output into Claude before the plan is generated.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML / CSS / JS |
| Backend | FastAPI (Python) |
| AI layer | Claude API (Anthropic) — claude-sonnet-4-5 |
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
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py                  # Env loading (ANTHROPIC_API_KEY)
│   │   ├── api/
│   │   │   └── routes_plan.py             # All /plan/* endpoints
│   │   ├── schemas/
│   │   │   └── plan.py                    # Pydantic models
│   │   ├── services/
│   │   │   ├── claude_service.py          # Claude API interactions
│   │   │   └── planner_service.py         # Agent orchestration
│   │   ├── mcp_tools/
│   │   │   ├── repo_tool.py               # Repo / GitHub scanner
│   │   │   ├── docs_tool.py               # Docs / URL fetcher
│   │   │   └── shell_tool.py              # Shell command runner
│   │   └── agent_prompt.py                # Agent system prompt
│   ├── main.py                            # Entry point + CORS
│   ├── .env                               # API keys (gitignored)
│   └── requirements.txt
├── frontend/
│   ├── index.html                         # UI structure
│   ├── style.css                          # Dark theme styles
│   └── script.js                          # API calls and plan rendering
├── docs/
│   ├── agent.md                           # Agent documentation
│   ├── skill.md                           # Skill workflow documentation
│   └── mcp_tools.md                       # MCP tools documentation
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/plan/generate` | Generate plan from requirement only |
| POST | `/plan/generate-with-context` | Generate plan with repo, docs, and shell context |
| POST | `/plan/generate-from-repo` | Generate plan from a repo directory |
| POST | `/plan/generate-from-docs` | Generate plan from a documentation source |
| POST | `/plan/generate-from-shell` | Generate plan from shell command output |
| GET | `/plan/agent-prompt` | Preview the agent system prompt |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Shine-23/agentic-ai-hands-on
cd DevProject_AI

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Add your API key
echo ANTHROPIC_API_KEY=your_key_here > .env

# 5. Start the backend
uvicorn main:app --reload

# 6. Open the frontend
# Double-click frontend/index.html in your browser
```

---

## Related Files
- [`docs/agent.md`](docs/agent.md) — agent purpose, sample inputs and outputs
- [`docs/skill.md`](docs/skill.md) — 9-step planning workflow
- [`docs/mcp_tools.md`](docs/mcp_tools.md) — MCP tools with sample inputs and outputs
- [`.claude/skills/SKILL.md`](.claude/skills/SKILL.md) — full agent workflow
- [`.claude/agents/ENGINEERING_PLANNING_AGENT.md`](.claude/agents/ENGINEERING_PLANNING_AGENT.md) — agent role definition
- [`backend/app/agent_prompt.py`](backend/app/agent_prompt.py) — agent system prompt used in code
