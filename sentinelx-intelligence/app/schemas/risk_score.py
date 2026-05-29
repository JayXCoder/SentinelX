from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class ScoreType(str, Enum):
    cyber_exposure = "cyber_exposure"
    vendor_risk = "vendor_risk"
    gtm_opportunity = "gtm_opportunity"
    market_threat = "market_threat"
    financial_risk = "financial_risk"
    reputation_risk = "reputation_risk"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class RiskScoreOut(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    entity_id: UUID
    entity_name: str
    score_type: str
    score_value: float
    risk_level: str
    explanation: str
    evidence_signal_ids: list
    correlated_event_id: UUID | None
    calculated_at: datetime


class RecalculateRequest(BaseModel):
    score_types: list[str] | None = None
    force: bool = False


class RecalculateResult(BaseModel):
    scores_created: int
    entity_ids: list[str]
