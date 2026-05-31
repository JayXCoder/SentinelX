from datetime import UTC, datetime
from typing import Any

from app.core.scoring_config import (
    RECENCY_DECAY_HOURS,
    RECENCY_WEIGHTS,
    SCORE_TYPE_MULTIPLIERS,
    SCORE_WEIGHTS,
    risk_level_from_score,
)


def _recency_weight(signal_timestamp: datetime | None) -> float:
    if signal_timestamp is None:
        return RECENCY_WEIGHTS["stale"]
    now = datetime.now(UTC)
    if signal_timestamp.tzinfo is None:
        signal_timestamp = signal_timestamp.replace(tzinfo=UTC)
    age_hours = (now - signal_timestamp).total_seconds() / 3600
    if age_hours <= RECENCY_DECAY_HOURS["fresh"]:
        return RECENCY_WEIGHTS["fresh"]
    if age_hours <= RECENCY_DECAY_HOURS["recent"]:
        return RECENCY_WEIGHTS["recent"]
    if age_hours <= RECENCY_DECAY_HOURS["aged"]:
        return RECENCY_WEIGHTS["aged"]
    return RECENCY_WEIGHTS["stale"]


def calculate_raw_score(signals: list[dict[str, Any]], score_type: str) -> float:
    """Compute a 0-100 weighted score from a list of signal dicts."""
    if not signals:
        return 0.0

    total = 0.0
    for sig in signals:
        severity = min(float(sig.get("severity", 0)), 10.0) / 10.0
        confidence = min(float(sig.get("confidence", 0.0)), 1.0)
        reliability = min(float(sig.get("source_reliability", 0.0)), 1.0)
        recency = _recency_weight(sig.get("timestamp"))
        frequency_bonus = min(len(signals) / 10.0, 1.0)
        entity_importance = float(sig.get("entity_importance", 0.5))

        weighted = (
            severity * SCORE_WEIGHTS.severity
            + confidence * SCORE_WEIGHTS.confidence
            + reliability * SCORE_WEIGHTS.source_reliability
            + recency * SCORE_WEIGHTS.recency
            + frequency_bonus * SCORE_WEIGHTS.frequency
            + entity_importance * SCORE_WEIGHTS.entity_importance
        )
        total += weighted

    avg = total / len(signals)
    multiplier = SCORE_TYPE_MULTIPLIERS.get(score_type, 1.0)
    score = min(avg * 100.0 * multiplier, 100.0)
    return round(score, 2)


def score_and_level(signals: list[dict[str, Any]], score_type: str) -> tuple[float, str]:
    score = calculate_raw_score(signals, score_type)
    return score, risk_level_from_score(score)


EXPLANATION_TEMPLATES: dict[str, str] = {
    "cyber_exposure": (
        "Cyber exposure score of {score:.0f} ({level}) based on {count} signals. "
        "Key factors: severity={avg_severity:.1f}/10, confidence={avg_confidence:.0%}, "
        "source reliability={avg_reliability:.0%}."
    ),
    "vendor_risk": (
        "Vendor risk score of {score:.0f} ({level}) from {count} signals covering "
        "operational, financial, and compliance indicators."
    ),
    "gtm_opportunity": (
        "GTM opportunity score of {score:.0f} ({level}) from {count} signals. "
        "Buying intent, hiring signals, and competitor weaknesses detected."
    ),
    "market_threat": (
        "Market threat score of {score:.0f} ({level}) from {count} signals. "
        "Competitor expansion and market sentiment analyzed."
    ),
    "financial_risk": (
        "Financial risk score of {score:.0f} ({level}) from {count} signals. "
        "Earnings, debt, and market indicators assessed."
    ),
    "reputation_risk": (
        "Reputation risk score of {score:.0f} ({level}) from {count} signals. "
        "Social sentiment, news frequency, and complaints analyzed."
    ),
}


def build_explanation(
    score: float,
    level: str,
    score_type: str,
    signals: list[dict[str, Any]],
) -> str:
    default_template = "Score: {score:.0f} ({level}), {count} signals."
    template = EXPLANATION_TEMPLATES.get(score_type, default_template)
    count = len(signals)
    avg_severity = sum(float(s.get("severity", 0)) for s in signals) / max(count, 1)
    avg_confidence = sum(float(s.get("confidence", 0)) for s in signals) / max(count, 1)
    avg_reliability = sum(float(s.get("source_reliability", 0)) for s in signals) / max(count, 1)
    return template.format(
        score=score,
        level=level,
        count=count,
        avg_severity=avg_severity,
        avg_confidence=avg_confidence,
        avg_reliability=avg_reliability,
    )
