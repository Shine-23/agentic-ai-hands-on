from app.agent_prompt import ENGINEERING_PLANNING_AGENT_PROMPT
from app.schemas.plan import PlanResponse
from app.services.claude_service import (
    get_claude_client,
    extract_text_from_response,
    safe_parse_plan_json,
)


def build_messages(requirement: str) -> dict:
    return {
        "system": ENGINEERING_PLANNING_AGENT_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": (
                    "Create an engineering plan for this product requirement:\n\n"
                    f"{requirement}"
                ),
            }
        ],
    }


def _mock_response(requirement: str) -> PlanResponse:
    return PlanResponse(
        requirement_summary=f"The user wants to build: {requirement}",
        clarifying_questions=[
            "Is this intended for a single team or multiple organizations?",
            "Do users need role-based access control?",
            "Should the first version support third-party login?",
        ],
        assumptions=[
            "Assuming MVP scope for a small engineering team.",
            "Assuming FastAPI backend with PostgreSQL.",
            "Assuming JWT-based authentication.",
        ],
        suggested_mvp_scope=[
            "User authentication",
            "Project creation and management",
            "Issue submission and tracking",
            "Slack alert integration for issue events",
            "Basic dashboard for viewing issues",
        ],
        proposed_architecture=[
            "Frontend: Lovable or lightweight UI",
            "Backend: FastAPI (Python)",
            "Database: PostgreSQL",
            "AI layer: Claude API (Anthropic)",
            "Deployment: Docker + Railway",
        ],
        data_model_entities=[
            "User",
            "Organization",
            "Project",
            "Issue",
            "Notification",
        ],
        api_draft=[
            "POST /auth/register — register a new user",
            "POST /auth/login — authenticate a user",
            "GET /projects — list projects",
            "POST /projects — create a project",
            "POST /issues — submit a new issue",
            "GET /issues/{id} — fetch issue details",
            "POST /notifications/slack/test — test Slack webhook",
        ],
        implementation_plan=[
            "Milestone 1: Project setup and auth",
            "Milestone 2: Project and issue CRUD",
            "Milestone 3: Slack notification service",
            "Milestone 4: Testing and deployment prep",
        ],
        risks_and_dependencies=[
            "Slack webhook reliability and configuration",
            "Permissions model complexity if multi-tenant",
            "Auth and session handling must be secure from day one",
            "Claude API token usage and cost if scaled",
        ],
        recommended_next_steps=[
            "Confirm MVP scope and tenant model with stakeholders",
            "Design initial database schema",
            "Implement auth endpoints first",
            "Build project and issue APIs next",
        ],
    )


def generate_plan(requirement: str) -> PlanResponse:
    payload = build_messages(requirement)

    try:
        client = get_claude_client()
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=payload["system"],
            messages=payload["messages"],
        )
        text = extract_text_from_response(response)
        plan_data = safe_parse_plan_json(text)
        return PlanResponse(**plan_data)

    except Exception as e:
        print(f"Claude API error: {e}")
        return _mock_response(requirement)
