# Pydantic models for the plan history API.

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.plan import PlanResponse
from app.schemas.task import Ticket


class SavePlanRequest(BaseModel):
    plan: PlanResponse
    tickets: Optional[List[Ticket]] = None

    @field_validator("plan")
    @classmethod
    def plan_must_have_summary(cls, v: PlanResponse) -> PlanResponse:
        if not v.requirement_summary or not v.requirement_summary.strip():
            raise ValueError("plan must have a non-empty requirement_summary")
        return v


class _OrmBase(BaseModel):
    """Shared base for models that are read from ORM objects."""
    model_config = ConfigDict(from_attributes=True)


class PlanSummary(_OrmBase):
    id: int
    title: str
    requirement: str
    created_at: datetime


class PlanDetail(_OrmBase):
    id: int
    title: str
    requirement: str
    plan: PlanResponse
    tickets: Optional[List[Ticket]] = None
    created_at: datetime
