import re
from datetime import UTC, datetime
from typing import Any

from app.core.logging import get_logger
from bs4 import BeautifulSoup
from langdetect import LangDetectException, detect

logger = get_logger(__name__)

ENTITY_PATTERNS = [
    (r"\bCVE-\d{4}-\d+\b", "cve"),
    (r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "email"),
    (r"\b(?:sk|pk)_(?:live|test)_[A-Za-z0-9]+\b", "api_key"),
    (r"\b(?:AWS|AKIA)[A-Z0-9]{16,}\b", "aws_key"),
]

REDACT_PATTERNS = [
    (r"\b(?:sk|pk)_(?:live|test)_[A-Za-z0-9]+\b", "[REDACTED_API_KEY]"),
    (r"\b(?:AWS|AKIA)[A-Z0-9]{16,}\b", "[REDACTED_AWS_KEY]"),
]


class ParserService:
    def parse(self, *, html: str | None, text: str | None, url: str) -> dict[str, Any]:
        soup = BeautifulSoup(html or text or "", "lxml")
        title = self._extract_title(soup)
        clean_text = self.redact_sensitive_text(self._clean_text(soup, fallback=text or ""))
        entities = self._extract_entities(clean_text)
        language = self._detect_language(clean_text)
        published_at = self._extract_published_at(soup)

        return {
            "title": title,
            "clean_text": clean_text[:50000],
            "detected_entities": entities,
            "detected_language": language,
            "published_at": published_at,
            "parsed_metadata": {
                "url": url,
                "word_count": len(clean_text.split()),
            },
        }

    @staticmethod
    def redact_sensitive_text(text: str) -> str:
        redacted = text
        for pattern, replacement in REDACT_PATTERNS:
            redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)
        return redacted

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            return og["content"].strip()
        h1 = soup.find("h1")
        return h1.get_text(strip=True) if h1 else None

    def _clean_text(self, soup: BeautifulSoup, fallback: str) -> str:
        for tag in soup(["script", "style", "noscript", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        if not text:
            text = fallback
        text = re.sub(r"\n{3,}", "\n\n", text)
        return re.sub(r"[ \t]+", " ", text).strip()

    def _extract_entities(self, text: str) -> list[dict[str, str]]:
        entities: list[dict[str, str]] = []
        seen: set[str] = set()
        for pattern, kind in ENTITY_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(0)
                if value in seen:
                    continue
                seen.add(value)
                entities.append({"type": kind, "value": value})
        return entities[:100]

    def _detect_language(self, text: str) -> str | None:
        sample = text[:2000]
        if len(sample) < 40:
            return None
        try:
            return detect(sample)
        except LangDetectException:
            return None

    def _extract_published_at(self, soup: BeautifulSoup) -> datetime | None:
        meta = soup.find("meta", property="article:published_time")
        if meta and meta.get("content"):
            try:
                return datetime.fromisoformat(meta["content"].replace("Z", "+00:00"))
            except ValueError:
                pass
        time_tag = soup.find("time")
        if time_tag and time_tag.get("datetime"):
            try:
                return datetime.fromisoformat(
                    time_tag["datetime"].replace("Z", "+00:00")
                )
            except ValueError:
                pass
        return datetime.now(UTC)
