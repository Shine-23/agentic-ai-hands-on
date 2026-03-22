# Backend Flow — DevProject AI

## Overview
How a request travels through the backend from the user to Claude and back.

---

## Request Flow

```
User sends POST /plan/generate-with-context
            │
            ▼
        main.py
   (receives request, CORS check, routes to /plan router)
            │
            ▼
   api/routes_plan.py
   (validates requirement, calls MCP tools, collects context)
            │
       ┌────┴────────────────────┐
       ▼                         ▼
 mcp_tools/                schemas/plan.py
 repo_tool.py              (MCPContext objects built
 docs_tool.py               from tool outputs)
 shell_tool.py
       │
       └────────────┐
                    ▼
        services/planner_service.py
        (builds the prompt + appends MCP context,
         calls Claude, parses response)
                    │
              ┌─────┴─────┐
              ▼           ▼
   services/claude_service.py    (on failure)
   (sends to Claude API,      _mock_response()
    extracts text,            returns fallback plan
    parses JSON)
              │
              ▼
        PlanResponse (JSON)
        returned to the user
```

---

## Layer by Layer

| Layer | File | Job |
|-------|------|-----|
| 1. Entry | `main.py` | Start the server, allow CORS |
| 2. Config | `core/config.py` | Load API key from `.env` |
| 3. Route | `api/routes_plan.py` | Receive request, validate, run tools |
| 4. Tools | `mcp_tools/` | Gather context (repo, docs, shell) |
| 5. Schema | `schemas/plan.py` | Shape the data (request/response models) |
| 6. Planner | `services/planner_service.py` | Build prompt, call Claude, parse result |
| 7. Claude | `services/claude_service.py` | Talk to the Anthropic API |
| 8. Prompt | `agent_prompt.py` | The system instructions Claude follows |

---

## Key Rules
- MCP tools are **non-fatal** — if a tool fails, it is skipped and logged, the request continues
- If Claude returns invalid JSON or the API call fails, `_mock_response()` is returned instead of crashing
- All environment variables are loaded once at startup via `core/config.py`
- The agent behaviour is controlled entirely by `agent_prompt.py` — edit that file to change how Claude plans
