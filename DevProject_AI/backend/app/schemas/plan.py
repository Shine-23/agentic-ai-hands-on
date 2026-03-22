# Pydantic models for the plan API.
# MCPContext — context item passed to Claude (repo file, doc, shell output, URL)
# ContextualPlanRequest — the main plan generation request (requirement + optional context)
# PlanResponse — structured plan returned by the agent

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class MCPSourceType(str, Enum):
    repo = "repo"   # file from a local or cloned repo
    docs = "docs"   # local doc file
    url  = "url"    # fetched from a URL
    tool = "tool"   # output of a shell command


class MCPContext(BaseModel):
    source: str
    source_type: MCPSourceType = MCPSourceType.docs
    content: str


class ContextualPlanRequest(BaseModel):
    requirement: str
    directory: Optional[str] = None
    sources: Optional[List[str]] = None
    commands: Optional[List[str]] = None
    mcp_context: Optional[List[MCPContext]] = None


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
