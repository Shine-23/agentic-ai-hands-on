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
| Development tickets | Generates structured tickets with acceptance criteria and story points |
| Plan history | Saves, loads, and deletes plans with their tickets |

---

## MCP Tools
Three tools enrich the AI plan with real project context:

| Tool | Purpose |
|---|---|
| `repo_tool` | Scans a local directory or clones a public GitHub repo |
| `docs_tool` | Fetches documentation from a URL or local file |
| `shell_tool` | Runs shell commands and captures output (e.g. `pip list`) |

All three tools feed their output into Claude before the plan is generated. If any tool fails the request returns a `400` error immediately — context is never silently skipped.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML / CSS / JS |
| Backend | FastAPI (Python) |
| AI layer | Claude API (Anthropic) — claude-sonnet-4-6 |
| Database | PostgreSQL |
| Deployment | Docker + Railway |
| Env management | python-dotenv |

---

## Project Structure

```
DevProject_AI/
├── .claude/
│   ├── CLAUDE.md                              # Claude Code instructions
│   ├── skills/
│   │   └── SKILL.md                           # Agent workflow definition (9 steps)
│   └── agents/
│       ├── ENGINEERING_PLANNING_AGENT.md      # Planner agent role and behavior
│       └── TASK_GENERATOR_AGENT.md            # Task generator agent role and behavior
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py                      # Env loading
│   │   ├── api/
│   │   │   ├── routes_plan.py                 # /plan/* endpoints
│   │   │   └── routes_history.py              # /history/* endpoints
│   │   ├── schemas/
│   │   │   ├── plan.py                        # Plan request/response models
│   │   │   ├── task.py                        # Ticket models
│   │   │   └── history.py                     # History models
│   │   ├── db/
│   │   │   ├── database.py                    # SQLAlchemy engine and session
│   │   │   └── models.py                      # PlanRecord, TicketRecord ORM models
│   │   ├── services/
│   │   │   ├── claude_service.py              # Claude API interactions
│   │   │   ├── planner_service.py             # Plan generation logic
│   │   │   └── task_service.py                # Ticket generation logic
│   │   ├── mcp_tools/
│   │   │   ├── repo_tool.py                   # Repo / GitHub scanner
│   │   │   ├── docs_tool.py                   # Docs / URL fetcher
│   │   │   └── shell_tool.py                  # Shell command runner
│   │   └── agent_prompt.py                    # Agent system prompt loader
│   ├── main.py                                # Entry point + CORS + lifespan
│   ├── .env                                   # API keys (gitignored)
│   └── requirements.txt
├── frontend/
│   ├── index.html                             # UI structure
│   ├── style.css                              # Dark theme styles
│   └── script.js                             # API calls and plan/ticket rendering
├── docs/
│   ├── agent.md                               # Agent documentation
│   ├── skill.md                               # Skill workflow documentation
│   ├── mcp_tools.md                           # MCP tools documentation
│   └── backend_flow.md                        # End-to-end request flow
├── .env.example                               # Environment variable template
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check (includes DB status) |
| POST | `/plan/generate-with-context` | Generate plan with optional repo, docs, and shell context |
| POST | `/plan/generate-tasks` | Generate development tickets from a plan |
| GET | `/history` | List all saved plans |
| GET | `/history/{id}` | Load a saved plan with its tickets |
| POST | `/history/save` | Save a plan and its tickets |
| DELETE | `/history/{id}` | Delete a saved plan and its tickets |

---

## Quick Start

### Local development (no Docker)
```bash
# 1. Clone the repo
git clone https://github.com/Shine-23/agentic-ai-hands-on
cd DevProject_AI

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Configure environment variables
cp ../.env.example .env
# Edit .env — set ANTHROPIC_API_KEY and DATABASE_URL

# 5. Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE devproject_ai;"

# 6. Start the backend
uvicorn main:app --reload

# 7. Open the frontend
# Open frontend/index.html directly in your browser (no build step needed)
```

### Local development (Docker)
```bash
# Copy and fill in your API key
cp .env.example backend/.env
# Edit backend/.env — set ANTHROPIC_API_KEY (DATABASE_URL is handled by docker-compose)

docker compose up --build
# Visit http://localhost:8000
```

### Deploy to Railway
1. Push this repo to GitHub
2. Create a new Railway project → **Deploy from GitHub repo**
3. Set the **Root Directory** to `DevProject_AI`
4. Add a **PostgreSQL** plugin — Railway sets `DATABASE_URL` automatically
5. Add environment variable: `ANTHROPIC_API_KEY=your-key`
6. Deploy — Railway detects `railway.toml` and uses the Dockerfile automatically

---

## Related Files
- [`docs/agent.md`](docs/agent.md) — agent purpose, sample inputs and outputs
- [`docs/skill.md`](docs/skill.md) — 9-step planning workflow
- [`docs/mcp_tools.md`](docs/mcp_tools.md) — MCP tools with sample inputs and outputs
- [`docs/backend_flow.md`](docs/backend_flow.md) — end-to-end request flow
- [`.claude/skills/SKILL.md`](.claude/skills/SKILL.md) — full agent workflow
- [`.claude/agents/ENGINEERING_PLANNING_AGENT.md`](.claude/agents/ENGINEERING_PLANNING_AGENT.md) — planner agent role definition
- [`.claude/agents/TASK_GENERATOR_AGENT.md`](.claude/agents/TASK_GENERATOR_AGENT.md) — task generator agent role definition
- [`backend/app/agent_prompt.py`](backend/app/agent_prompt.py) — agent system prompt used in code
