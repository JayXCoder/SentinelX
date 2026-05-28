from app.rules.cyber_rules import CorrelationRule

RULES: list[CorrelationRule] = [
    CorrelationRule(
        rule_name="vendor_instability_risk",
        required_signal_types=["vendor_risk", "financial", "osint"],
        time_window_hours=72,
        minimum_signals=2,
        entity_match_required=True,
        output_event_type="vendor_risk_event",
        category_keywords=["downtime", "outage", "breach", "compliance", "hiring_freeze"],
    ),
    CorrelationRule(
        rule_name="vendor_financial_distress",
        required_signal_types=["vendor_risk", "financial"],
        time_window_hours=120,
        minimum_signals=2,
        entity_match_required=True,
        output_event_type="vendor_risk_event",
        category_keywords=["layoff", "bankruptcy", "funding", "debt", "loss"],
    ),
    CorrelationRule(
        rule_name="vendor_reputation_decline",
        required_signal_types=["vendor_risk", "osint"],
        time_window_hours=96,
        minimum_signals=3,
        entity_match_required=True,
        output_event_type="reputation_event",
        category_keywords=["complaint", "review", "lawsuit", "scandal"],
    ),
]
