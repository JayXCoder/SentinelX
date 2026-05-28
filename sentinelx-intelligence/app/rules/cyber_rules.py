from dataclasses import dataclass, field


@dataclass(frozen=True)
class CorrelationRule:
    rule_name: str
    required_signal_types: list[str]
    time_window_hours: int
    minimum_signals: int
    entity_match_required: bool
    output_event_type: str
    category_keywords: list[str] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.rule_name)


RULES: list[CorrelationRule] = [
    CorrelationRule(
        rule_name="cyber_multi_signal_incident",
        required_signal_types=["cyber"],
        time_window_hours=24,
        minimum_signals=2,
        entity_match_required=True,
        output_event_type="cyber_incident",
        category_keywords=["vulnerability", "breach", "malware", "threat", "exploit"],
    ),
    CorrelationRule(
        rule_name="cyber_osint_threat_combo",
        required_signal_types=["cyber", "osint"],
        time_window_hours=48,
        minimum_signals=2,
        entity_match_required=False,
        output_event_type="cyber_incident",
        category_keywords=["threat_actor", "attack", "campaign"],
    ),
    CorrelationRule(
        rule_name="critical_vulnerability_cluster",
        required_signal_types=["cyber"],
        time_window_hours=72,
        minimum_signals=3,
        entity_match_required=False,
        output_event_type="cyber_incident",
        category_keywords=["cve", "vulnerability", "patch"],
    ),
]
