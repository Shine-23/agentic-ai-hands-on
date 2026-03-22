# History API endpoints.
# Handles saving, listing, loading, and deleting plans from PostgreSQL.
# Plans and tickets are stored in separate tables (plans + tickets).

import json
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import PlanRecord, TicketRecord
from app.schemas.history import SavePlanRequest, PlanSummary, PlanDetail
from app.schemas.plan import PlanResponse
from app.schemas.task import Ticket

router = APIRouter(prefix="/history", tags=["history"])


@router.post("/save", response_model=PlanSummary)
def save_plan(payload: SavePlanRequest, db: Session = Depends(get_db)):
    title = (payload.plan.requirement_summary or "Untitled Plan")[:150]

    # Prevent saving the exact same plan twice
    existing = db.query(PlanRecord).filter(PlanRecord.title == title).first()
    if existing:
        raise HTTPException(status_code=409, detail="A plan with this title already exists.")

    record = PlanRecord(
        title=title,
        requirement=payload.plan.requirement_summary,
        plan_json=json.dumps(payload.plan.model_dump()),
    )
    db.add(record)
    db.flush()  # get record.id before committing

    if payload.tickets:
        for t in payload.tickets:
            db.add(TicketRecord(
                plan_id=record.id,
                ticket_id=t.id,
                title=t.title,
                description=t.description,
                acceptance_criteria=json.dumps(t.acceptance_criteria),
                priority=t.priority,
                estimate=t.estimate,
                phase=t.phase,
                labels=json.dumps(t.labels),
                dependencies=json.dumps(t.dependencies),
            ))

    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=List[PlanSummary])
def list_plans(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return (
        db.query(PlanRecord)
        .order_by(PlanRecord.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{plan_id}", response_model=PlanDetail)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    record = db.query(PlanRecord).filter(PlanRecord.id == plan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Plan not found")

    tickets = None
    if record.tickets:
        try:
            tickets = [
                Ticket(
                    id=t.ticket_id,
                    title=t.title,
                    description=t.description,
                    acceptance_criteria=json.loads(t.acceptance_criteria),
                    priority=t.priority,
                    estimate=t.estimate,
                    phase=t.phase,
                    labels=json.loads(t.labels),
                    dependencies=json.loads(t.dependencies),
                )
                for t in record.tickets
            ]
        except (json.JSONDecodeError, KeyError) as e:
            raise HTTPException(status_code=500, detail=f"Ticket data is malformed: {e}")

    return PlanDetail(
        id=record.id,
        title=record.title,
        requirement=record.requirement,
        plan=PlanResponse(**json.loads(record.plan_json)),
        tickets=tickets,
        created_at=record.created_at,
    )


@router.delete("/{plan_id}", status_code=204)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    record = db.query(PlanRecord).filter(PlanRecord.id == plan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(record)  # cascade deletes tickets too
    db.commit()
    return Response(status_code=204)
