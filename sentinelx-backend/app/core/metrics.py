from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

HTTP_REQUESTS = Counter(
    "sentinelx_http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)


def metrics_response() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
