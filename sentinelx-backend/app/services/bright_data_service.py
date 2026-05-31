from typing import Any, Literal

import httpx
from app.core.config import get_settings
from app.core.logging import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

BrightDataMode = Literal["off", "api", "proxy"]


class BrightDataService:
    """Bright Data Web Unlocker API or native HTTP proxy; falls back to direct HTTP."""

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def mode(self) -> BrightDataMode:
        if not self.settings.bright_data_enabled:
            return "off"
        if self.settings.bright_data_api_key and self.settings.bright_data_zone:
            return "api"
        if self.settings.bright_data_username and self.settings.bright_data_password:
            return "proxy"
        return "off"

    @property
    def enabled(self) -> bool:
        return self.mode != "off"

    def proxy_url(self) -> str | None:
        if self.mode != "proxy":
            return None
        user = self.settings.bright_data_username
        password = self.settings.bright_data_password
        host = self.settings.bright_data_host
        port = self.settings.bright_data_port
        return f"http://{user}:{password}@{host}:{port}"

    def _fetch_via_api(self, url: str, *, render_js: bool) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "zone": self.settings.bright_data_zone,
            "url": url,
            "format": "raw",
            "method": "GET",
        }
        if render_js:
            payload["headers"] = {"x-unblock-expect": "html"}

        headers = {
            "Authorization": f"Bearer {self.settings.bright_data_api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=self.settings.scrape_timeout_seconds) as client:
            response = client.post(
                self.settings.bright_data_api_url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            return {
                "url": url,
                "status_code": response.status_code,
                "html": response.text,
                "via_proxy": True,
                "via_bright_data_api": True,
            }

    def _fetch_via_proxy(self, url: str, *, render_js: bool) -> dict[str, Any]:
        proxies = self.proxy_url()
        headers = {
            "User-Agent": "SentinelX/1.0 (+https://sentinelx.local)",
        }
        if render_js:
            headers["x-unblock-expect"] = "html"

        with httpx.Client(
            proxies=proxies,
            timeout=self.settings.scrape_timeout_seconds,
            follow_redirects=True,
        ) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return {
                "url": str(response.url),
                "status_code": response.status_code,
                "html": response.text,
                "via_proxy": True,
                "via_bright_data_api": False,
            }

    def _fetch_direct(self, url: str) -> dict[str, Any]:
        with httpx.Client(
            timeout=self.settings.scrape_timeout_seconds,
            follow_redirects=True,
        ) as client:
            response = client.get(
                url,
                headers={"User-Agent": "SentinelX/1.0 (+https://sentinelx.local)"},
            )
            response.raise_for_status()
            return {
                "url": str(response.url),
                "status_code": response.status_code,
                "html": response.text,
                "via_proxy": False,
                "via_bright_data_api": False,
            }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self, url: str, *, render_js: bool = False) -> dict[str, Any]:
        logger.info(
            "Bright Data fetch",
            extra={"url": url, "mode": self.mode, "render_js": render_js},
        )

        if self.mode == "api":
            return self._fetch_via_api(url, render_js=render_js)
        if self.mode == "proxy":
            return self._fetch_via_proxy(url, render_js=render_js)
        return self._fetch_direct(url)

    def health_check(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "mode": self.mode,
            "zone": self.settings.bright_data_zone if self.mode == "api" else None,
            "host": self.settings.bright_data_host if self.mode == "proxy" else None,
            "configured": self.enabled,
            "api_key_set": bool(self.settings.bright_data_api_key),
        }
