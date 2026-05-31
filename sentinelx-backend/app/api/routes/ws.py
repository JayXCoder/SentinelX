from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.core.config import get_settings
from app.services.realtime_hub import get_realtime_hub

router = APIRouter(tags=["realtime"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    api_key: str | None = Query(default=None),
) -> None:
    settings = get_settings()
    if settings.api_key:
        provided = api_key or websocket.headers.get("x-api-key")
        if not provided or provided != settings.api_key:
            await websocket.close(code=4401, reason="Invalid or missing API key")
            return

    hub = get_realtime_hub()
    await hub.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await hub.disconnect(websocket)
