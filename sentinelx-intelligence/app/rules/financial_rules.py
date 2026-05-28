from app.rules.cyber_rules import CorrelationRule

RULES: list[CorrelationRule] = [
    CorrelationRule(
        rule_name="financial_instability_signal",
        required_signal_types=["financial"],
        time_window_hours=120,
        minimum_signals=2,
        entity_match_required=True,
        output_event_type="financial_instability",
        category_keywords=["earnings_miss", "debt", "downgrade", "loss", "bankruptcy"],
    ),
    CorrelationRule(
        rule_name="funding_market_movement",
        required_signal_types=["financial", "gtm"],
        time_window_hours=72,
        minimum_signals=2,
        entity_match_required=False,
        output_event_type="competitor_movement",
        category_keywords=["funding", "ipo", "acquisition", "series"],
    ),
    CorrelationRule(
        rule_name="market_sentiment_threat",
        required_signal_types=["financial", "osint"],
        time_window_hours=48,
        minimum_signals=3,
        entity_match_required=False,
        output_event_type="financial_instability",
        category_keywords=["selloff", "downturn", "market_risk", "recession"],
    ),
]
