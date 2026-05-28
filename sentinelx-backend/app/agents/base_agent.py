from abc import ABC, abstractmethod

from app.schemas.signal import AgentInput, AgentOutput
from app.services.sglang_service import SGLangService


class BaseAgent(ABC):
    signal_type: str = ""
    category_default: str = "general"

    def __init__(self, sglang: SGLangService | None = None) -> None:
        self.sglang = sglang or SGLangService()

    @abstractmethod
    def system_prompt(self) -> str:
        ...

    def user_prompt(self, data: AgentInput) -> str:
        return (
            f"Analyze the following intelligence record and return JSON only.\n"
            f"Source type: {data.source_type}\n"
            f"Title: {data.title}\n"
            f"Entities: {data.entities}\n"
            f"Metadata: {data.metadata}\n"
            f"Content:\n{data.clean_text[:12000]}"
        )

    def process(self, data: AgentInput) -> AgentOutput:
        raw = self.sglang.complete_json(self.system_prompt(), self.user_prompt(data))
        raw.setdefault("signal_type", self.signal_type)
        raw.setdefault("category", self.category_default)
        return AgentOutput.model_validate(raw)
