# Task Generator Agent service.
# Takes a PlanResponse and uses Claude to convert it into structured development tickets.
# Agent prompt is read from .claude/agents/TASK_GENERATOR_AGENT.md — edit that file to change behaviour.

import json
from pathlib import Path

from pydantic import ValidationError

from app.schemas.plan import PlanResponse
from app.schemas.task import TaskResponse, Ticket
from app.services.claude_service import (
    extract_text_from_response,
    get_claude_client,
    safe_parse_plan_json,
)

TASK_AGENT_PROMPT = (
    Path(__file__).resolve().parents[3]
    / ".claude/agents/TASK_GENERATOR_AGENT.md"
).read_text(encoding="utf-8")


def generate_tasks(plan: PlanResponse) -> TaskResponse:
    """
    Send the plan to Claude and return a structured list of development tickets.
    Raises ValueError on parse or validation failure so the caller can surface the error.
    """
    # Only send the sections relevant to task generation — avoids oversized prompts
    relevant = {
        "requirement_summary": plan.requirement_summary,
        "suggested_mvp_scope": plan.suggested_mvp_scope,
        "implementation_plan": plan.implementation_plan,
        "api_draft":           plan.api_draft,
        "data_model_entities": plan.data_model_entities,
    }
    plan_text = json.dumps(relevant, indent=2)

    user_message = (
        "Convert this engineering plan into structured development tickets:\n\n"
        f"{plan_text}"
    )

    client = get_claude_client()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=TASK_AGENT_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    text = extract_text_from_response(response)

    try:
        data = safe_parse_plan_json(text)
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Task agent returned invalid JSON: {e}")

    try:
        tickets = [Ticket(**t) for t in data.get("tickets", [])]
    except ValidationError as e:
        raise ValueError(f"Task agent returned invalid ticket data: {e}")

    return TaskResponse(tickets=tickets)
