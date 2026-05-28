from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class BrightDataService:
    """Proxy-based scraping via Bright Data; falls back to direct HTTP."""

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def enabled(self) -> bool:
        return bool(
            self.settings.bright_data_enabled
            and self.settings.bright_data_username
            and self.settings.bright_data_password
        )

    def proxy_url(self) -> str | None:
        if not self.enabled:
            return None
        user = self.settings.bright_data_username
        password = self.settings.bright_data_password
        host = self.settings.bright_data_host
        port = self.settings.bright_data_port
        return f"http://{user}:{password}@{host}:{port}"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self, url: str, *, render_js: bool = False) -> dict[str, Any]:
        proxies = self.proxy_url()
        timeout = self.settings.scrape_timeout_seconds
        headers = {
            "User-Agent": "SentinelX/1.0 (+https://sentinelx.local)",
        }
        if render_js and self.enabled:
            headers["x-unblock-expect"] = "html"

        logger.info(
            "Bright Data fetch",
            extra={"url": url, "proxy": bool(proxies), "render_js": render_js},
        )

        with httpx.Client(
            proxies=proxies,
            timeout=timeout,
            follow_redirects=True,
        ) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return {
                "url": str(response.url),
                "status_code": response.status_code,
                "html": response.text,
                "via_proxy": bool(proxies),
            }

    def health_check(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "host": self.settings.bright_data_host if self.enabled else None,
            "configured": bool(
                self.settings.bright_data_username and self.settings.bright_data_password
            ),
        }
