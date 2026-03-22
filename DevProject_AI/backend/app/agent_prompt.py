# System prompt for the Engineering Planning Agent.
# Reads from .claude/agents/ENGINEERING_PLANNING_AGENT.md at startup — that file is the
# single source of truth for agent behaviour. Edit it to change tone, output structure, or rules.
#
# Path resolution: this file lives at backend/app/agent_prompt.py
#   parents[0] = backend/app/
#   parents[1] = backend/
#   parents[2] = DevProject_AI/   <-- project root where .claude/ lives
#
# NOTE: the prompt is read once on startup. Restart the server after editing the .md file.

from pathlib import Path

_prompt_path = Path(__file__).resolve().parents[2] / ".claude/agents/ENGINEERING_PLANNING_AGENT.md"

if not _prompt_path.exists():
    raise FileNotFoundError(
        f"Engineering Planning Agent prompt not found at: {_prompt_path}\n"
        "Ensure ENGINEERING_PLANNING_AGENT.md exists in .claude/agents/"
    )

ENGINEERING_PLANNING_AGENT_PROMPT = _prompt_path.read_text(encoding="utf-8")
