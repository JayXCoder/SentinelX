import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import get_logger
from app.db.models.correlated_event import CorrelatedEvent
from app.db.models.intelligence_signal import IntelSignal
from app.rules.cyber_rules import CorrelationRule
from app.rules import cyber_rules, vendor_rules, gtm_rules, financial_rules

logger = get_logger(__name__)

ALL_RULES: list[CorrelationRule] = (
    cyber_rules.RULES + vendor_rules.RULES + gtm_rules.RULES + financial_rules.RULES
)


def _entity_names(signals: list[IntelSignal]) -> set[str]:
    names: set[str] = set()
    for sig in signals:
        for ent in (sig.entities or []):
            if isinstance(ent, dict):
                name = ent.get("name") or ent.get("text") or ""
                if name:
                    names.add(name.lower().strip())
            elif isinstance(ent, str):
                names.add(ent.lower().strip())
    return names


def _signals_match_rule(
    rule: CorrelationRule,
    signals: list[IntelSignal],
    time_window_hours: int | None = None,
) -> list[IntelSignal]:
    window = time_window_hours or rule.time_window_hours
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window)

    matched: list[IntelSignal] = []
    for sig in signals:
        if sig.signal_type not in rule.required_signal_types:
            continue
        sig_ts = sig.timestamp or sig.created_at
        if sig_ts.tzinfo is None:
            sig_ts = sig_ts.replace(tzinfo=timezone.utc)
        if sig_ts < cutoff:
            continue
        matched.append(sig)

    if len(matched) < rule.minimum_signals:
        return []

    if rule.entity_match_required:
        entity_sets = [_entity_names([s]) for s in matched]
        common = entity_sets[0]
        for es in entity_sets[1:]:
            common = common & es
        if not common:
            # Try pairwise intersection instead of full intersection
            any_overlap = False
            for i in range(len(entity_sets)):
                for j in range(i + 1, len(entity_sets)):
                    if entity_sets[i] & entity_sets[j]:
                        any_overlap = True
                        break
                if any_overlap:
                    break
            if not any_overlap:
                return []

    return matched


def _build_involved_entities(signals: list[IntelSignal]) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for sig in signals:
        for ent in (sig.entities or []):
            if isinstance(ent, dict):
                name = (ent.get("name") or ent.get("text") or "").strip()
                if name and name not in seen:
                    seen[name] = ent
            elif isinstance(ent, str) and ent.strip():
                name = ent.strip()
                if name not in seen:
                    seen[name] = {"name": name}
    return list(seen.values())


class CorrelationService:
    def __init__(self, settings=None) -> None:
        self._settings = settings or get_settings()

    def run_all(
        self,
        db: Session,
        time_window_hours: int | None = None,
    ) -> list[CorrelatedEvent]:
        signals = db.query(IntelSignal).all()
        return self._apply_rules(db, signals, time_window_hours)

    def run_for_signal(
        self,
        db: Session,
        signal_id: str,
        time_window_hours: int | None = None,
    ) -> list[CorrelatedEvent]:
        anchor = db.query(IntelSignal).filter(IntelSignal.signal_id == signal_id).first()
        if not anchor:
            logger.warning("Signal not found", extra={"signal_id": signal_id})
            return []

        window = time_window_hours or self._settings.correlation_time_window_hours
        cutoff = datetime.now(timezone.utc) - timedelta(hours=window)
        signals = db.query(IntelSignal).filter(IntelSignal.created_at >= cutoff).all()
        if anchor not in signals:
            signals.append(anchor)

        return self._apply_rules(db, signals, time_window_hours)

    def _apply_rules(
        self,
        db: Session,
        signals: list[IntelSignal],
        time_window_hours: int | None,
    ) -> list[CorrelatedEvent]:
        created: list[CorrelatedEvent] = []

        for rule in ALL_RULES:
            matched = _signals_match_rule(rule, signals, time_window_hours)
            if not matched:
                continue

            signal_ids = [str(s.id) for s in matched]
            timestamps = [s.timestamp or s.created_at for s in matched]
            timestamps_tz = []
            for t in timestamps:
                if t.tzinfo is None:
                    t = t.replace(tzinfo=timezone.utc)
                timestamps_tz.append(t)

            event = CorrelatedEvent(
                id=uuid.uuid4(),
                event_type=rule.output_event_type,
                title=f"[{rule.rule_name}] Correlated intelligence event",
                summary=(
                    f"Rule '{rule.rule_name}' matched {len(matched)} signals "
                    f"of types {rule.required_signal_types}. "
                    f"Event type: {rule.output_event_type}."
                ),
                involved_entities=_build_involved_entities(matched),
                signal_ids=signal_ids,
                correlation_reason=f"Rule: {rule.rule_name}. Matched {len(matched)} signals in {rule.time_window_hours}h window.",
                confidence=round(
                    sum(s.confidence for s in matched) / len(matched), 3
                ),
                severity=max(s.severity for s in matched),
                first_seen=min(timestamps_tz),
                last_seen=max(timestamps_tz),
            )
            db.add(event)
            created.append(event)
            logger.info(
                "Correlated event created",
                extra={"rule": rule.rule_name, "signals": len(matched)},
            )

        if created:
            db.commit()
            for e in created:
                db.refresh(e)

        return created
