# MCP Tools — Purpose, Inputs & Outputs

## Overview
The 3 MCP tools enrich the AI planning request with real context from your project.
Instead of generating a generic plan, Claude receives your actual code, docs, and environment
before producing the engineering plan.

---

## 1. Repo Tool (`repo_tool.py`)
**Purpose:** Reads your actual project files so the AI plans around your existing code, not from scratch.

**Input:**
```
directory: "https://github.com/Shine-23/agentic-ai-hands-on"
```
or
```
directory: "C:\my-project"
```

**What it does internally:**
- Clones the repo (or reads local folder)
- Scans `.py`, `.md`, `.json`, `.yaml`, `.toml` files (max 20)
- Passes file contents to Claude as context

**Output fed to Claude:**
```
[REPO] routes_plan.py
from fastapi import APIRouter...

[REPO] main.py
from fastapi import FastAPI...
```

**Effect on plan:** Claude sees your existing routes, models, and structure — so it won't suggest building something you already have.

---

## 2. Docs Tool (`docs_tool.py`)
**Purpose:** Fetches documentation so the AI gives library-specific advice, not generic recommendations.

**Input:**
```
sources: "https://fastapi.tiangolo.com"
```

**What it does internally:**
- Fetches the URL (or reads a local file)
- Strips HTML, extracts plain text
- Passes it to Claude as context

**Output fed to Claude:**
```
[URL] https://fastapi.tiangolo.com
FastAPI is a modern, fast web framework for building APIs
with Python based on standard Python type hints...
```

**Effect on plan:** Claude recommends FastAPI-specific patterns (e.g. `Depends()` for auth) instead of generic REST advice.

---

## 3. Shell Tool (`shell_tool.py`)
**Purpose:** Captures your environment state so the AI knows what's already installed and available.

**Input:**
```
commands: "pip list"
```

**What it does internally:**
- Runs the shell command
- Captures stdout/stderr
- Passes output to Claude as context

**Output fed to Claude:**
```
[TOOL] pip list
fastapi        0.104.1
uvicorn        0.24.0
anthropic      0.23.0
pydantic       2.5.0
```

**Effect on plan:** Claude won't tell you to install FastAPI — it already knows you have it. It will suggest only what's missing.

---

## Using All 3 Together

```json
{
  "requirement": "Add JWT authentication",
  "directory": "https://github.com/Shine-23/agentic-ai-hands-on",
  "sources": ["https://fastapi.tiangolo.com"],
  "commands": ["pip list"]
}
```

Claude gets your code + the docs + your environment → the most specific, accurate plan possible.
