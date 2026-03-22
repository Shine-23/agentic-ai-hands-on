# DevProject AI — Claude Code Instructions

## Project overview
AI-powered engineering planning assistant that converts rough product requirements into structured engineering plans (architecture, API drafts, task breakdowns, risk reviews).

## Tech stack
- **Backend:** FastAPI (Python)
- **AI layer:** Claude API (Anthropic)
- **Frontend:** HTML / CSS / JS (index.html, style.css, script.js)
- **Database:** PostgreSQL (default) or SQLite
- **Auth:** JWT (default) or OAuth2
- **Deployment:** Docker + Railway
- **Env management:** python-dotenv

## Project structure
```
DevProject_AI/
├── .claude/
│   ├── CLAUDE.md              # This file
│   ├── skills/
│   │   └── SKILL.md           # Agent workflow definition
│   └── agents/
│       └── ENGINEERING_PLANNING_AGENT.md  # Agent role and behavior
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py          # Centralised env loading (ANTHROPIC_API_KEY)
│   │   ├── api/
│   │   │   └── routes_plan.py     # HTTP endpoints
│   │   ├── schemas/
│   │   │   └── plan.py            # Pydantic models incl. MCPContext, ContextualPlanRequest
│   │   ├── services/
│   │   │   ├── claude_service.py  # Raw Claude API interactions
│   │   │   └── planner_service.py # Agent workflow logic
│   │   ├── mcp_tools/
│   │   │   ├── repo_tool.py       # Reads local repo files into MCPContext
│   │   │   ├── docs_tool.py       # Fetches URLs or local docs into MCPContext
│   │   │   └── shell_tool.py      # Runs shell commands into MCPContext
│   │   └── agent_prompt.py        # Agent system prompt
│   ├── main.py                # Entry point
│   ├── .env                   # API keys (gitignored)
│   └── requirements.txt
├── frontend/
│   ├── index.html             # HTML structure
│   ├── style.css              # All styles (dark theme, sticky header)
│   └── script.js              # API calls, plan rendering, UI interactions
├── docs/
│   ├── agent.md               # Agent purpose, sample i/o, working style
│   ├── skill.md               # Skill workflow, 9 steps, sample i/o
│   └── mcp_tools.md           # MCP tools purpose, sample i/o for all 3 tools
├── venv/                      # Python virtual environment (do not edit)
└── README.md
```

## Key files
- [`.claude/agents/ENGINEERING_PLANNING_AGENT.md`](agents/ENGINEERING_PLANNING_AGENT.md) — agent role, boundaries, and behavior
- [`.claude/skills/SKILL.md`](skills/SKILL.md) — step-by-step workflow the agent follows
- [`backend/app/agent_prompt.py`](../backend/app/agent_prompt.py) — agent system prompt used in code
- [`backend/app/schemas/plan.py`](../backend/app/schemas/plan.py) — `MCPContext`, `MCPSourceType`, `PlanRequest`, `ContextualPlanRequest`, `PlanResponse`
- [`backend/app/api/routes_plan.py`](../backend/app/api/routes_plan.py) — all `/plan/*` endpoints (generate, generate-with-context, generate-from-repo, generate-from-docs, generate-from-shell)
- [`backend/app/mcp_tools/repo_tool.py`](../backend/app/mcp_tools/repo_tool.py) — `read_repo_context()` scans local dir or clones GitHub URL (supports tree/subdir URLs)
- [`backend/app/mcp_tools/docs_tool.py`](../backend/app/mcp_tools/docs_tool.py) — `fetch_docs_context()` fetches a URL or local file
- [`backend/app/mcp_tools/shell_tool.py`](../backend/app/mcp_tools/shell_tool.py) — `run_shell_context()` runs a shell command
- [`frontend/index.html`](../frontend/index.html) — UI structure
- [`frontend/style.css`](../frontend/style.css) — UI styles
- [`frontend/script.js`](../frontend/script.js) — UI logic, API calls, plan rendering
- [`docs/agent.md`](../docs/agent.md) — agent documentation
- [`docs/skill.md`](../docs/skill.md) — skill workflow documentation
- [`docs/mcp_tools.md`](../docs/mcp_tools.md) — MCP tools documentation

## Python environment
- Always use the local venv: `venv/Scripts/python` and `venv/Scripts/pip`
- Do not use global pip to install packages
- Keep `backend/requirements.txt` updated after any install

## Development conventions
- All backend code goes inside `backend/`
- Agent logic and prompts live in `backend/app/`
- Do not modify files inside `venv/`
- Use `.env` for secrets — never hardcode API keys
- Keep `ANTHROPIC_API_KEY` in `.env`, never in source code

## Agent behaviour rules
- The agent prompt is the source of truth for agent behavior — edit `backend/app/agent_prompt.py` to change it
- The skill workflow is defined in `.claude/skills/SKILL.md` — edit that file to change planning steps
- The agent role is defined in `.claude/agents/ENGINEERING_PLANNING_AGENT.md`
- All three files should stay in sync with each other

## What NOT to do
- Do not commit `.env` or any file containing API keys
- Do not edit files inside `venv/`
- Do not add features beyond what is asked
- Do not over-engineer — this is a focused planning tool
