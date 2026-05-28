from app.agents.base_agent import BaseAgent


class ExecutiveSummaryAgent(BaseAgent):
    signal_type = "executive_summary"
    category_default = "executive"

    def system_prompt(self) -> str:
        return (
            "You are an executive intelligence summarizer for SentinelX. "
            "Produce business-readable executive summaries, intelligence briefs, "
            "strategic implications, and recommended next actions. "
            "Return valid JSON with keys: signal_type, category, title, summary, "
            "entities, severity (0-10), confidence (0-1), source_reliability (0-1), "
            "evidence (array of strings), recommended_action. "
            "Set signal_type to 'executive_summary'."
        )
