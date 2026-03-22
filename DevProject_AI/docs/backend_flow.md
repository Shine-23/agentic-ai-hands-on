# Backend Flow — DevProject AI

## Overview
How a request travels through the backend from the user to Claude and back.

---

## Plan Generation Flow

```
User sends POST /plan/generate-with-context
            │
            ▼
        main.py
   (CORS check, routes to /plan router)
            │
            ▼
   api/routes_plan.py
   (validates requirement length, runs MCP tools)
            │
       ┌────┴─────────────────────────┐
       ▼                              ▼
 mcp_tools/                   schemas/plan.py
 repo_tool.py                 (MCPContext objects built
 docs_tool.py                  from tool outputs)
 shell_tool.py
 [any failure → 400 HTTPException]
       │
       └──────────────┐
                      ▼
        services/planner_service.py
        (builds user message with MCP context appended,
         calls Claude, parses JSON response)
                      │
                ┌─────┴──────────────────────┐
                ▼                            ▼
   services/claude_service.py          (on failure)
   (singleton Anthropic client,      raises ValueError
    extracts text, parses JSON)      → 502 HTTPException
                │
                ▼
         PlanResponse (JSON)
         returned to the user
```

---

## Task Generation Flow

```
User sends POST /plan/generate-tasks  (with PlanResponse body)
            │
            ▼
   api/routes_plan.py
   (validates plan has summary + implementation_plan)
            │
            ▼
   services/task_service.py
   (sends relevant plan sections to Claude,
    parses and validates ticket JSON)
            │
       ┌────┴───────────────────────────┐
       ▼                               ▼
services/claude_service.py        (on failure)
(same singleton client,         raises ValueError
 extracts text, parses JSON)    → 502 HTTPException
       │
       ▼
 TaskResponse (JSON) — list of Ticket objects
 returned to the user
```

---

## History Flow

```
Save:   POST /history/save   → stores PlanRecord + TicketRecord rows in PostgreSQL
List:   GET  /history        → returns list of PlanSummary (paginated, newest first)
Load:   GET  /history/{id}   → returns PlanDetail with plan JSON + tickets
Delete: DELETE /history/{id} → cascade deletes plan + its tickets (204 No Content)
```

---

## Layer by Layer

| Layer | File | Job |
|-------|------|-----|
| 1. Entry | `main.py` | Start server, CORS, lifespan (create_all), health check |
| 2. Config | `core/config.py` | Load and validate env vars from `.env` |
| 3. Routes | `api/routes_plan.py` | Plan and task endpoints — validate, run tools, call service |
| 4. Routes | `api/routes_history.py` | History CRUD — save, list, load, delete |
| 5. Tools | `mcp_tools/` | Gather context (repo, docs, shell) — all raise on failure |
| 6. Schemas | `schemas/plan.py` | `ContextualPlanRequest`, `PlanResponse`, `MCPContext` |
| 7. Schemas | `schemas/task.py` | `Ticket` (with field validation), `TaskResponse` |
| 8. Schemas | `schemas/history.py` | `SavePlanRequest`, `PlanSummary`, `PlanDetail` |
| 9. DB | `db/models.py` | `PlanRecord`, `TicketRecord` ORM models |
| 10. DB | `db/database.py` | Engine, session factory, `get_db` dependency |
| 11. Planner | `services/planner_service.py` | Build prompt, call Claude, parse plan |
| 12. Tasks | `services/task_service.py` | Call Claude, parse and validate tickets |
| 13. Claude | `services/claude_service.py` | Singleton Anthropic client, JSON extraction |
| 14. Prompt | `agent_prompt.py` | Loads system prompt from `ENGINEERING_PLANNING_AGENT.md` |

---

## Key Rules
- MCP tool failures are **fatal to the request** — repo, docs, and shell errors return `400` so the user knows their context was not applied
- Claude failures (bad JSON, API error) raise `ValueError` → `502 HTTPException` — no silent fallbacks
- All environment variables are validated at startup via `core/config.py` — missing keys crash the server immediately with a clear message
- Agent behaviour is controlled by `ENGINEERING_PLANNING_AGENT.md` — edit that file to change how Claude plans (server restart required)
- Task ticket fields are validated by Pydantic — invalid `priority`, `labels`, `estimate`, or `id` format are rejected at parse time
