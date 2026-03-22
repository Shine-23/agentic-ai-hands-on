# System prompt for the Engineering Planning Agent.
# Reads from .claude/agents/ENGINEERING_PLANNING_AGENT.md — that file is the single source of truth.
# Edit that file to change the agent's behavior, tone, or output structure.

from pathlib import Path

ENGINEERING_PLANNING_AGENT_PROMPT = (
    Path(__file__).resolve().parents[2]
    / ".claude/agents/ENGINEERING_PLANNING_AGENT.md"
).read_text(encoding="utf-8")
