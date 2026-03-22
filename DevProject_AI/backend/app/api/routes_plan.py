# All /plan/* API endpoints.
# Handles request validation, runs MCP tools, and delegates plan generation to planner_service.
# Endpoints: /generate-with-context, /generate-tasks

from fastapi import APIRouter, HTTPException

from app.schemas.plan import ContextualPlanRequest, PlanResponse
from app.services.planner_service import generate_plan
from app.services.task_service import generate_tasks
from app.schemas.task import TaskResponse
from app.mcp_tools.repo_tool import read_repo_context
from app.mcp_tools.docs_tool import fetch_docs_context
from app.mcp_tools.shell_tool import run_shell_context

router = APIRouter(prefix="/plan", tags=["plan"])

MAX_REQUIREMENT_LENGTH = 4000


def _validate_requirement(requirement: str) -> None:
    if not requirement or not requirement.strip():
        raise HTTPException(status_code=400, detail="requirement must not be empty.")
    if len(requirement.strip()) < 10:
        raise HTTPException(status_code=400, detail="requirement is too short to generate a useful plan.")
    if len(requirement.strip()) > MAX_REQUIREMENT_LENGTH:
        raise HTTPException(status_code=400, detail=f"requirement exceeds {MAX_REQUIREMENT_LENGTH} characters.")


@router.post("/generate-tasks", response_model=TaskResponse)
def create_tasks(plan: PlanResponse):
    if not plan.requirement_summary or not plan.implementation_plan:
        raise HTTPException(status_code=400, detail="Plan must have a requirement summary and implementation plan before generating tasks.")
    try:
        return generate_tasks(plan)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/generate-with-context", response_model=PlanResponse)
def create_contextual_plan(payload: ContextualPlanRequest):
    _validate_requirement(payload.requirement)
    combined: list = list(payload.mcp_context or [])

    if payload.directory:
        try:
            combined.extend(read_repo_context(payload.directory))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Repo context failed: {e}")

    for source in payload.sources or []:
        try:
            combined.append(fetch_docs_context(source))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Docs context failed ({source}): {e}")

    for command in payload.commands or []:
        try:
            combined.append(run_shell_context(command))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Shell context failed ({command}): {e}")

    try:
        return generate_plan(payload.requirement, combined or None)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
