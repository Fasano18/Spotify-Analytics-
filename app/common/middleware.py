import logging
import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("spotify-analytics-api")


def setup_cors(app: FastAPI) -> None:
    """Configura CORS para a aplicação."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )


def request_logging_middleware(app: FastAPI) -> None:
    """Registra middleware de logging e X-Request-ID."""

    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable[[Request], Response]) -> Response:  # type: ignore[override]
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Anexa o request_id ao state para uso em logs internos
        request.state.request_id = request_id

        response: Response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time_ms": round(process_time, 2),
                "request_id": request_id,
            },
        )
        return response

