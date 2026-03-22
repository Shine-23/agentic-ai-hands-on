from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class MCPSourceType(str, Enum):
    repo = "repo"
    docs = "docs"
    tool = "tool"
    url = "url"
    file = "file"


class MCPContext(BaseModel):
    source: str
    source_type: MCPSourceType = MCPSourceType.docs
    content: str


class PlanRequest(BaseModel):
    requirement: str


class ContextualPlanRequest(BaseModel):
    requirement: str
    directory: Optional[str] = None
    sources: Optional[List[str]] = None
    commands: Optional[List[str]] = None
    mcp_context: Optional[List[MCPContext]] = None
    output_style: Optional[str] = "detailed"


class RepoPlanRequest(BaseModel):
    requirement: str
    directory: str


class DocsPlanRequest(BaseModel):
    requirement: str
    source: str


class ShellPlanRequest(BaseModel):
    requirement: str
    command: str


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
