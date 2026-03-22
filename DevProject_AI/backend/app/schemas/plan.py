from pydantic import BaseModel
from typing import List


class PlanRequest(BaseModel):
    requirement: str


class PlanResponse(BaseModel):
    requirement_summary: str
    clarifying_questions: List[str]
    assumptions: List[str]
    suggested_mvp_scope: List[str]
    proposed_architecture: List[str]
    data_model_entities: List[str]
    api_draft: List[str]
    implementation_plan: List[str]
    risks_and_dependencies: List[str]
    recommended_next_steps: List[str]
