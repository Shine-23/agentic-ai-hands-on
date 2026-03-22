# DevProject AI — Claude Code Instructions

## Project overview
AI-powered engineering planning assistant that converts rough product requirements into structured engineering plans (architecture, API drafts, task breakdowns, risk reviews) and development tickets.

## Tech stack
- **Backend:** FastAPI (Python)
- **AI layer:** Claude API (Anthropic)
- **Frontend:** HTML / CSS / JS (index.html, style.css, script.js)
- **Database:** PostgreSQL (local, via psycopg2-binary + SQLAlchemy ORM)
- **Auth:** JWT (default) or OAuth2
- **Deployment:** Docker + Railway
- **Env management:** python-dotenv

## Project structure
```
DevProject_AI/
├── .claude/
│   ├── CLAUDE.md              # This file
│   ├── skills/
│   │   └── SKILL.md           # Step-by-step agent workflow definition
│   └── agents/
│       ├── ENGINEERING_PLANNING_AGENT.md  # Planner agent role and behavior
│       └── TASK_GENERATOR_AGENT.md        # Task generator agent role and behavior
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py          # Centralised env loading (ANTHROPIC_API_KEY)
│   │   ├── api/
│   │   │   ├── routes_plan.py     # /plan/* endpoints (generate, generate-with-context)
│   │   │   └── routes_history.py  # /history/* endpoints (save, list, load, delete)
│   │   ├── schemas/
│   │   │   ├── plan.py            # PlanRequest, ContextualPlanRequest, PlanResponse, MCPContext
│   │   │   ├── task.py            # Ticket, TaskResponse
│   │   │   └── history.py         # SavePlanRequest, PlanSummary, PlanDetail
│   │   ├── db/
│   │   │   ├── database.py        # SQLAlchemy engine, SessionLocal, Base
│   │   │   └── models.py          # PlanRecord, TicketRecord ORM models
│   │   ├── services/
│   │   │   ├── claude_service.py  # Raw Claude API interactions
│   │   │   └── planner_service.py # Agent workflow logic
│   │   ├── mcp_tools/
│   │   │   ├── repo_tool.py       # Reads local repo files or clones GitHub URL
│   │   │   ├── docs_tool.py       # Fetches URLs or local docs as context
│   │   │   └── shell_tool.py      # Runs shell commands as context
│   │   └── agent_prompt.py        # System prompt injected into Claude API calls
│   ├── main.py                # FastAPI app entry point, router registration, CORS
│   ├── .env                   # API keys and DB URL (gitignored)
│   └── requirements.txt
├── frontend/
│   ├── index.html             # UI structure (sidebar + main content layout)
│   ├── style.css              # All styles (warm dark theme, persistent sidebar)
│   └── script.js              # API calls, plan/ticket rendering, history management
├── docs/
│   ├── agent.md               # Agent purpose, sample i/o, working style
│   ├── skill.md               # Skill workflow, 9 steps, sample i/o
│   └── mcp_tools.md           # MCP tools purpose, sample i/o for all 3 tools
├── venv/                      # Python virtual environment (do not edit)
└── README.md
```

## Key files
- [`.claude/agents/ENGINEERING_PLANNING_AGENT.md`](agents/ENGINEERING_PLANNING_AGENT.md) — planner agent role, boundaries, output structure, and JSON schema
- [`.claude/agents/TASK_GENERATOR_AGENT.md`](agents/TASK_GENERATOR_AGENT.md) — task generator agent role, ticket rules, and JSON schema
- [`.claude/skills/SKILL.md`](skills/SKILL.md) — step-by-step workflow the planner agent follows (9 steps)
- [`backend/app/agent_prompt.py`](../backend/app/agent_prompt.py) — system prompt injected into Claude API calls at runtime
- [`backend/app/schemas/plan.py`](../backend/app/schemas/plan.py) — `MCPContext`, `MCPSourceType`, `PlanRequest`, `ContextualPlanRequest`, `PlanResponse`
- [`backend/app/schemas/task.py`](../backend/app/schemas/task.py) — `Ticket`, `TaskResponse`
- [`backend/app/schemas/history.py`](../backend/app/schemas/history.py) — `SavePlanRequest`, `PlanSummary`, `PlanDetail`
- [`backend/app/api/routes_plan.py`](../backend/app/api/routes_plan.py) — `/plan/*` endpoints (generate, generate-with-context, generate-tasks)
- [`backend/app/api/routes_history.py`](../backend/app/api/routes_history.py) — `/history/*` endpoints (save, list, load by id, delete)
- [`backend/app/db/models.py`](../backend/app/db/models.py) — `PlanRecord` and `TicketRecord` SQLAlchemy ORM models
- [`backend/app/db/database.py`](../backend/app/db/database.py) — SQLAlchemy engine, `SessionLocal`, `Base`, `get_db` dependency
- [`backend/app/mcp_tools/repo_tool.py`](../backend/app/mcp_tools/repo_tool.py) — `read_repo_context()` scans local dir or clones GitHub URL
- [`backend/app/mcp_tools/docs_tool.py`](../backend/app/mcp_tools/docs_tool.py) — `fetch_docs_context()` fetches a URL or local file
- [`backend/app/mcp_tools/shell_tool.py`](../backend/app/mcp_tools/shell_tool.py) — `run_shell_context()` runs a shell command
- [`frontend/index.html`](../frontend/index.html) — UI structure
- [`frontend/style.css`](../frontend/style.css) — UI styles
- [`frontend/script.js`](../frontend/script.js) — UI logic, API calls, plan/ticket rendering, history sidebar
- [`docs/agent.md`](../docs/agent.md) — agent documentation
- [`docs/skill.md`](../docs/skill.md) — skill workflow documentation
- [`docs/mcp_tools.md`](../docs/mcp_tools.md) — MCP tools documentation

## Running the dev server
```bash
cd DevProject_AI/backend
../venv/Scripts/uvicorn main:app --reload
```
Then open `frontend/index.html` directly in a browser (no build step needed).

## Python environment
- Always use the local venv: `venv/Scripts/python` and `venv/Scripts/pip`
- Never use global pip to install packages
- Keep `backend/requirements.txt` updated after any install

## Database
- PostgreSQL running locally; connection string in `backend/.env` as `DATABASE_URL`
- Tables are created automatically on startup via `Base.metadata.create_all()`
- Two tables: `plans` (one row per saved plan) and `tickets` (one row per ticket, FK to `plans.id`)
- Cascade delete: deleting a plan also deletes its tickets
- If you add a new column to a model, run an `ALTER TABLE` migration — SQLAlchemy does not auto-migrate existing tables

## Development conventions
- All backend code goes inside `backend/`
- Agent logic and prompts live in `backend/app/`
- Do not modify files inside `venv/`
- Use `.env` for secrets — never hardcode API keys
- Keep `ANTHROPIC_API_KEY` and `DATABASE_URL` in `.env`, never in source code

## Agent behaviour rules
The agent system has three layers that must stay in sync:
1. **`backend/app/agent_prompt.py`** — the system prompt sent to Claude at runtime (source of truth for what Claude actually does)
2. **`.claude/skills/SKILL.md`** — the step-by-step workflow definition
3. **`.claude/agents/ENGINEERING_PLANNING_AGENT.md`** — the planner agent role and boundaries
4. **`.claude/agents/TASK_GENERATOR_AGENT.md`** — the task generator agent role and ticket rules

If you change how the agent behaves, update all relevant files to match.

## What NOT to do
- Do not commit `.env` or any file containing API keys
- Do not edit files inside `venv/`
- Do not add features beyond what is asked
- Do not over-engineer — this is a focused planning tool
- Do not use `Base.metadata.create_all()` as a substitute for migrations on existing tables
