from app.agents.base_agent import BaseAgent


class OSINTAgent(BaseAgent):
    signal_type = "osint"
    category_default = "osint"

    def system_prompt(self) -> str:
        return (
            "You are an OSINT analyst for SentinelX. "
            "Detect public discussions, social trends, suspicious activity, "
            "community sentiment, geopolitical signals, and forum mentions. "
            "Return valid JSON with keys: signal_type, category, title, summary, "
            "entities, severity (0-10), confidence (0-1), source_reliability (0-1), "
            "evidence (array of strings), recommended_action. "
            "Set signal_type to 'osint'."
        )
