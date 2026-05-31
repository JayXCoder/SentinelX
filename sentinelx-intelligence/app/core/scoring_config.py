from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreWeights:
    severity: float = 0.30
    confidence: float = 0.20
    source_reliability: float = 0.15
    recency: float = 0.15
    frequency: float = 0.10
    entity_importance: float = 0.10


@dataclass(frozen=True)
class RiskLevelThresholds:
    low_max: int = 24
    medium_max: int = 49
    high_max: int = 74
    # critical: 75-100


SCORE_WEIGHTS = ScoreWeights()
RISK_THRESHOLDS = RiskLevelThresholds()

# Per-score-type severity multipliers (applied before weighted sum)
SCORE_TYPE_MULTIPLIERS: dict[str, float] = {
    "cyber_exposure": 1.2,
    "vendor_risk": 1.0,
    "gtm_opportunity": 0.9,
    "market_threat": 1.0,
    "financial_risk": 1.1,
    "reputation_risk": 0.95,
}

# Recency decay: signals older than these hours get reduced weight
RECENCY_DECAY_HOURS: dict[str, float] = {
    "fresh": 24.0,    # weight = 1.0
    "recent": 72.0,   # weight = 0.7
    "aged": 168.0,    # weight = 0.4
    # older → weight = 0.2
}

RECENCY_WEIGHTS: dict[str, float] = {
    "fresh": 1.0,
    "recent": 0.7,
    "aged": 0.4,
    "stale": 0.2,
}


def risk_level_from_score(score: float) -> str:
    if score <= RISK_THRESHOLDS.low_max:
        return "low"
    if score <= RISK_THRESHOLDS.medium_max:
        return "medium"
    if score <= RISK_THRESHOLDS.high_max:
        return "high"
    return "critical"
