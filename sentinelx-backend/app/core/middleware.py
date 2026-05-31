from app.core.metrics import HTTP_REQUESTS
from app.core.rate_limit import check_rate_limit
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        check_rate_limit(request)
        response = await call_next(request)
        path = request.url.path
        if path != "/metrics":
            HTTP_REQUESTS.labels(
                method=request.method,
                path=path,
                status=str(response.status_code),
            ).inc()
        return response
