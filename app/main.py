import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.artists.router import router as artists_router
from app.auth.router import router as auth_router
from app.common.exceptions import AppError, app_error_handler, validation_error_handler
from app.common.middleware import request_logging_middleware, setup_cors
from app.config import settings
from app.history.router import router as history_router
from app.tracks.router import router as tracks_router
from app.user.router import router as user_router

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def create_app() -> FastAPI:
    """Cria e configura a instância principal da aplicação FastAPI."""

    app = FastAPI(
        title="Spotify Analytics API",
        description="API REST para análise de dados do Spotify.",
        version="0.1.0",
    )

    # Middlewares
    setup_cors(app)
    request_logging_middleware(app)

    # Exception handlers globais
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]

    # Routers
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(tracks_router)
    app.include_router(artists_router)
    app.include_router(history_router)

    # Servir arquivos estáticos (frontend)
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
    except Exception:
        # Se o diretório não existir, ignora (para desenvolvimento)
        pass

    @app.get("/", tags=["Frontend"])
    async def root() -> FileResponse:
        """Serve a página principal do dashboard."""
        static_path = Path("static/index.html")
        return FileResponse(static_path)

    @app.get("/health", tags=["Infra"])
    async def healthcheck() -> dict[str, Any]:
        """Endpoint simples de healthcheck da API."""

        return {"status": "ok"}

    return app


app = create_app()

