# Pydantic models for the Task Generator Agent output.
# A TaskResponse contains a list of Ticket objects grouped by phase.

import re
from typing import List, Literal, Optional

from pydantic import BaseModel, field_validator

VALID_LABELS = {
    "backend", "frontend", "database", "auth", "api",
    "testing", "infra", "docs", "devops", "security", "performance",
}

VALID_ESTIMATES = {1, 2, 3, 5, 8}


class Ticket(BaseModel):
    id: str                                          # e.g. "T-1", "T-2"
    title: str                                       # short ticket title
    description: str                                 # what needs to be done and why
    acceptance_criteria: List[str]                   # conditions that define "done"
    priority: Literal["high", "medium", "low"]       # enforced enum
    estimate: Optional[int] = None                   # story points: 1, 2, 3, 5, or 8
    phase: str                                       # milestone this ticket belongs to
    labels: List[str]                                # from VALID_LABELS
    dependencies: List[str]                          # ticket IDs e.g. ["T-1"]

    @field_validator("id")
    @classmethod
    def id_must_match_pattern(cls, v: str) -> str:
        if not re.fullmatch(r"T-\d+", v):
            raise ValueError(f"Ticket id must match 'T-N' format, got '{v}'")
        return v

    @field_validator("acceptance_criteria")
    @classmethod
    def criteria_must_not_be_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("acceptance_criteria must have at least one item")
        return v

    @field_validator("estimate")
    @classmethod
    def estimate_must_be_valid(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v not in VALID_ESTIMATES:
            raise ValueError(f"estimate must be one of {sorted(VALID_ESTIMATES)}, got {v}")
        return v

    @field_validator("labels")
    @classmethod
    def labels_must_be_valid(cls, v: List[str]) -> List[str]:
        invalid = [l for l in v if l not in VALID_LABELS]
        if invalid:
            raise ValueError(f"Invalid labels: {invalid}. Must be from: {sorted(VALID_LABELS)}")
        return v


class TaskResponse(BaseModel):
    tickets: List[Ticket]
