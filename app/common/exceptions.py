from typing import Any, Dict

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.schemas import ErrorResponse


class AppError(Exception):
    """Erro base da aplicação."""

    def __init__(self, code: str, message: str, status_code: int = 400, extra: Dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.extra = extra or {}


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    payload = ErrorResponse(codigo=exc.code, mensagem=exc.message).model_dump()
    if exc.extra:
        payload["detalhes"] = exc.extra
    return JSONResponse(status_code=exc.status_code, content=payload)


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            codigo="validation_error",
            mensagem="Os dados enviados são inválidos. Verifique os campos e tente novamente.",
        ).model_dump()
        | {"detalhes": exc.errors()},
    )

