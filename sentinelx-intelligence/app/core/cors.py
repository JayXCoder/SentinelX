from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app: FastAPI, cors_origins: str) -> None:
    """Apply CORS. Wildcard env is expanded — credentials + '*' is invalid in browsers."""
    raw = [o.strip() for o in cors_origins.split(",") if o.strip()]
    if not raw or "*" in raw:
        origins = [
            "http://localhost:4002",
            "http://127.0.0.1:4002",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    else:
        origins = raw

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
