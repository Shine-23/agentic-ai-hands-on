from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.plan import PlanRequest, PlanResponse
from app.services.planner_service import generate_plan
from app.agent_prompt import ENGINEERING_PLANNING_AGENT_PROMPT

router = APIRouter(prefix="/plan", tags=["plan"])


class PromptPreviewResponse(BaseModel):
    agent_prompt: str


@router.get("/agent-prompt", response_model=PromptPreviewResponse)
def preview_agent_prompt():
    return {"agent_prompt": ENGINEERING_PLANNING_AGENT_PROMPT}


@router.post("/generate", response_model=PlanResponse)
def create_plan(payload: PlanRequest):
    return generate_plan(payload.requirement)
