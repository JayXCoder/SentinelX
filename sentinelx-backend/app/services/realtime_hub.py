import asyncio
import json
from typing import Any

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.core.logging import get_logger

logger = get_logger(__name__)


class RealtimeHub:
    """Broadcasts realtime JSON events to connected dashboard clients."""

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.add(websocket)
        await self.broadcast(
            {
                "type": "system_status_update",
                "data": {"status": "connected", "clients": len(self._connections)},
            },
            exclude=None,
        )
        logger.info("WebSocket client connected", extra={"clients": len(self._connections)})

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(websocket)
        logger.info("WebSocket client disconnected", extra={"clients": len(self._connections)})

    async def broadcast(self, payload: dict[str, Any], exclude: WebSocket | None = None) -> None:
        message = json.dumps(payload, default=str)
        async with self._lock:
            targets = list(self._connections)

        stale: list[WebSocket] = []
        for connection in targets:
            if connection is exclude:
                continue
            try:
                await connection.send_text(message)
            except (WebSocketDisconnect, RuntimeError):
                stale.append(connection)

        if stale:
            async with self._lock:
                for connection in stale:
                    self._connections.discard(connection)

    @property
    def client_count(self) -> int:
        return len(self._connections)


_hub: RealtimeHub | None = None


def get_realtime_hub() -> RealtimeHub:
    global _hub
    if _hub is None:
        _hub = RealtimeHub()
    return _hub
