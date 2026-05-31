import json
import re
import time
from typing import Any

import httpx
from app.core.config import get_settings
from app.core.logging import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)


class SGLangService:
    """OpenAI-compatible client for Qwen via SGLang."""

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def chat_url(self) -> str:
        base = self.settings.sglang_base_url.rstrip("/")
        return f"{base}/v1/chat/completions"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=15),
        reraise=True,
    )
    def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        payload = {
            "model": self.settings.sglang_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        with httpx.Client(timeout=self.settings.sglang_timeout_seconds) as client:
            response = client.post(self.chat_url, json=payload)
            response.raise_for_status()
            body = response.json()

        content = body["choices"][0]["message"]["content"]
        latency_ms = (time.perf_counter() - started) * 1000
        usage = body.get("usage", {})

        logger.info(
            "SGLang completion",
            extra={
                "latency_ms": round(latency_ms, 2),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
            },
        )

        return self._parse_json_content(content)

    def _parse_json_content(self, content: str) -> dict[str, Any]:
        content = content.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise

    def health_check(self) -> dict[str, Any]:
        base = self.settings.sglang_base_url.rstrip("/")
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{base}/health")
                return {
                    "status": "ok" if response.status_code == 200 else "degraded",
                    "status_code": response.status_code,
                    "model": self.settings.sglang_model,
                }
        except Exception as exc:
            return {"status": "unavailable", "error": str(exc), "model": self.settings.sglang_model}
