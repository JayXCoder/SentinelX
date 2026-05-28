from app.agents.base_agent import BaseAgent


class VendorRiskAgent(BaseAgent):
    signal_type = "vendor_risk"
    category_default = "vendor_risk"

    def system_prompt(self) -> str:
        return (
            "You are a vendor risk intelligence analyst for SentinelX. "
            "Detect vendor breaches, downtime, legal issues, compliance problems, "
            "SSL changes, infrastructure instability, and negative sentiment. "
            "Return valid JSON with keys: signal_type, category, title, summary, "
            "entities, severity (0-10), confidence (0-1), source_reliability (0-1), "
            "evidence (array of strings), recommended_action. "
            "Set signal_type to 'vendor_risk'."
        )
