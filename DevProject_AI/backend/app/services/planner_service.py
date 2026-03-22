# Core planning logic. Builds the prompt, calls Claude, parses the response.

from typing import List, Optional

from app.agent_prompt import ENGINEERING_PLANNING_AGENT_PROMPT
from app.schemas.plan import MCPContext, PlanResponse
from app.services.claude_service import (
    extract_text_from_response,
    get_claude_client,
    safe_parse_plan_json,
)


def _build_user_message(requirement: str, mcp_context: Optional[List[MCPContext]] = None) -> str:
    context_text = ""

    if mcp_context:
        formatted = [
            f"[{item.source_type.value.upper()}] {item.source}\n{item.content}"
            for item in mcp_context
        ]
        context_text = "\n\nAdditional MCP Context:\n" + "\n\n".join(formatted)
        context_text += (
            "\n\nIMPORTANT: Repo/doc context has been provided above. "
            "Base your entire plan on that codebase — not on any assumed or prior project. "
            "Reference specific files, modules, and patterns from the provided context."
        )

    return (
        "Create an engineering plan for this product requirement:\n\n"
        f"{requirement}"
        f"{context_text}"
    )


def generate_plan(requirement: str, mcp_context: Optional[List[MCPContext]] = None) -> PlanResponse:
    """
    Call Claude to generate a structured engineering plan.
    Raises ValueError if Claude returns invalid or unparseable output.
    """
    user_message = _build_user_message(requirement, mcp_context)

    client = get_claude_client()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=ENGINEERING_PLANNING_AGENT_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    text = extract_text_from_response(response)

    try:
        plan_data = safe_parse_plan_json(text)
    except (ValueError, KeyError) as e:
        raise ValueError(f"Plan agent returned invalid JSON: {e}")

    return PlanResponse(**plan_data)
