from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agent_prompt import ENGINEERING_PLANNING_AGENT_PROMPT
from app.schemas.plan import (
    ContextualPlanRequest,
    DocsPlanRequest,
    PlanRequest,
    PlanResponse,
    RepoPlanRequest,
    ShellPlanRequest,
)
from app.services.planner_service import generate_plan
from app.mcp_tools.repo_tool import read_repo_context
from app.mcp_tools.docs_tool import fetch_docs_context
from app.mcp_tools.shell_tool import run_shell_context

router = APIRouter(prefix="/plan", tags=["plan"])


class PromptPreviewResponse(BaseModel):
    agent_prompt: str


def _validate_requirement(requirement: str) -> None:
    if not requirement or not requirement.strip():
        raise HTTPException(status_code=400, detail="requirement must not be empty.")
    if len(requirement.strip()) < 10:
        raise HTTPException(status_code=400, detail="requirement is too short to generate a useful plan.")


@router.get("/agent-prompt", response_model=PromptPreviewResponse)
def preview_agent_prompt():
    return {"agent_prompt": ENGINEERING_PLANNING_AGENT_PROMPT}


@router.post("/generate", response_model=PlanResponse)
def create_plan(payload: PlanRequest):
    _validate_requirement(payload.requirement)
    return generate_plan(payload.requirement)


@router.post("/generate-with-context", response_model=PlanResponse)
def create_contextual_plan(payload: ContextualPlanRequest):
    _validate_requirement(payload.requirement)
    combined: list = list(payload.mcp_context or [])

    if payload.directory:
        try:
            combined.extend(read_repo_context(payload.directory))
        except ValueError as e:
            print(f"Repo tool skipped: {e}")

    for source in payload.sources or []:
        try:
            combined.append(fetch_docs_context(source))
        except ValueError as e:
            print(f"Docs tool skipped ({source}): {e}")

    for command in payload.commands or []:
        try:
            combined.append(run_shell_context(command))
        except ValueError as e:
            print(f"Shell tool skipped ({command}): {e}")

    return generate_plan(payload.requirement, combined or None)


@router.post("/generate-from-repo", response_model=PlanResponse)
def create_plan_from_repo(payload: RepoPlanRequest):
    _validate_requirement(payload.requirement)
    try:
        mcp_context = read_repo_context(payload.directory)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return generate_plan(payload.requirement, mcp_context)


@router.post("/generate-from-docs", response_model=PlanResponse)
def create_plan_from_docs(payload: DocsPlanRequest):
    _validate_requirement(payload.requirement)
    try:
        mcp_context = [fetch_docs_context(payload.source)]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return generate_plan(payload.requirement, mcp_context)


@router.post("/generate-from-shell", response_model=PlanResponse)
def create_plan_from_shell(payload: ShellPlanRequest):
    _validate_requirement(payload.requirement)
    try:
        mcp_context = [run_shell_context(payload.command)]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return generate_plan(payload.requirement, mcp_context)
