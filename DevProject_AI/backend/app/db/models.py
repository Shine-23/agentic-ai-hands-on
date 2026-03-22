# SQLAlchemy ORM models.
# PlanRecord stores a generated plan. TicketRecord stores each ticket linked to a plan.

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.db.database import Base


class PlanRecord(Base):
    __tablename__ = "plans"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(150), nullable=False)       # first 150 chars of requirement_summary
    requirement = Column(Text, nullable=False)              # requirement_summary from the generated plan
    plan_json   = Column(Text, nullable=False)              # full PlanResponse as JSON string
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    tickets     = relationship("TicketRecord", back_populates="plan", cascade="all, delete-orphan")


class TicketRecord(Base):
    __tablename__ = "tickets"

    id                  = Column(Integer, primary_key=True, index=True)
    plan_id             = Column(Integer, ForeignKey("plans.id"), nullable=False, index=True)
    ticket_id           = Column(String(20), nullable=False)   # e.g. "T-1"
    title               = Column(String(300), nullable=False)
    description         = Column(Text, nullable=False)
    acceptance_criteria = Column(Text, nullable=False)         # JSON array string
    priority            = Column(String(20), nullable=False)
    estimate            = Column(SmallInteger, nullable=True)  # story points: 1,2,3,5,8
    phase               = Column(String(100), nullable=False)
    labels              = Column(Text, nullable=False)         # JSON array string
    dependencies        = Column(Text, nullable=False)         # JSON array string

    plan = relationship("PlanRecord", back_populates="tickets")
