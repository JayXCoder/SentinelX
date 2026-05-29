from app.rules.cyber_rules import CorrelationRule

RULES: list[CorrelationRule] = [
    CorrelationRule(
        rule_name="competitor_weakness_opportunity",
        required_signal_types=["gtm", "osint"],
        time_window_hours=72,
        minimum_signals=2,
        entity_match_required=False,
        output_event_type="market_opportunity",
        category_keywords=["complaint", "churn", "outage", "competitor_weakness"],
    ),
    CorrelationRule(
        rule_name="buying_intent_cluster",
        required_signal_types=["gtm"],
        time_window_hours=48,
        minimum_signals=2,
        entity_match_required=True,
        output_event_type="market_opportunity",
        category_keywords=["hiring", "rfp", "budget", "evaluation", "intent"],
    ),
    CorrelationRule(
        rule_name="competitor_expansion_threat",
        required_signal_types=["gtm", "financial"],
        time_window_hours=96,
        minimum_signals=2,
        entity_match_required=False,
        output_event_type="competitor_movement",
        category_keywords=["expansion", "new_market", "product_launch", "acquisition"],
    ),
]
