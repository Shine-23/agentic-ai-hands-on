# MCP Tools — Purpose, Inputs & Outputs

## Overview
The 3 MCP tools enrich the AI planning request with real context from your project.
Instead of generating a generic plan, Claude receives your actual code, docs, and environment
before producing the engineering plan.

> **Important:** All three tools are **fail-fast** — if a tool fails (bad URL, clone error,
> blocked command), the request returns a `400` error immediately. This ensures you always know
> when your context was not applied, rather than receiving a plan based on no context at all.

---

## 1. Repo Tool (`repo_tool.py`)
**Purpose:** Reads your actual project files so the AI plans around your existing code, not from scratch.

**Input:**
```
directory: "https://github.com/user/repo"
```
or
```
directory: "C:\my-project"
```

**What it does internally:**
- For GitHub URLs: clones the repo with `git clone --depth=1` into a temp directory
- For local paths: reads the directory directly
- Scans `.py`, `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml` files (max 20, max 10 KB each)
- Skips junk directories: `.git`, `node_modules`, `__pycache__`, `venv`, `.venv`, `dist`, `build`, etc.
- Cleans up temp clone after scanning
- Raises an error if no matching files are found

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
or a local file path:
```
sources: "/path/to/spec.md"
```

**What it does internally:**
- For URLs: fetches the page and strips HTML tags (skipping `<script>`, `<style>`, `<head>`)
- For local files: reads the file directly
- Reads in 4 KB chunks up to 10 KB — never loads large pages fully into memory
- Raises an error if the page is empty or JavaScript-rendered (no extractable text)

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
- Runs the shell command with a 10-second timeout
- Captures both stdout and stderr — stderr is included with a `[stderr]` label
- Prefixes output with `[exit code N]` when the command fails (non-zero exit)
- **Blocks dangerous commands** — `rm -rf`, `del /f`, `format`, `shutdown`, `curl`, `wget`,
  and other destructive patterns are rejected before execution

**Output fed to Claude:**
```
[TOOL] pip list
fastapi        0.135.1
uvicorn        0.42.0
anthropic      0.86.0
pydantic       2.12.5
```

**Effect on plan:** Claude won't tell you to install FastAPI — it already knows you have it. It will suggest only what's missing.

---

## Using All 3 Together

```json
{
  "requirement": "Add JWT authentication",
  "directory": "https://github.com/user/repo",
  "sources": ["https://fastapi.tiangolo.com"],
  "commands": ["pip list"]
}
```

Claude gets your code + the docs + your environment → the most specific, accurate plan possible.
