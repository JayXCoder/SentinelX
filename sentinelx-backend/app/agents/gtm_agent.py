from app.agents.base_agent import BaseAgent


class GTMAgent(BaseAgent):
    signal_type = "gtm"
    category_default = "go_to_market"

    def system_prompt(self) -> str:
        return (
            "You are a GTM intelligence analyst for SentinelX. "
            "Detect competitor pricing, feature launches, product announcements, "
            "customer complaints, buying intent, hiring trends, and technology adoption. "
            "Return valid JSON with keys: signal_type, category, title, summary, "
            "entities, severity (0-10), confidence (0-1), source_reliability (0-1), "
            "evidence (array of strings), recommended_action. "
            "Set signal_type to 'gtm'."
        )
