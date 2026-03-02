from app.common.exceptions import AppError


class SpotifyAPIError(AppError):
    """Erro genérico ao chamar a API do Spotify."""

    def __init__(self, message: str = "Erro ao comunicar com a API do Spotify.", status_code: int = 502):
        super().__init__(code="spotify_api_error", message=message, status_code=status_code)


class TokenExpiredError(AppError):
    """Token de acesso expirado."""

    def __init__(self, message: str = "Seu token expirou. Faça login novamente."):
        super().__init__(code="token_expired", message=message, status_code=401)


class RateLimitError(AppError):
    """Limite de requisições da API do Spotify excedido."""

    def __init__(self, retry_after: int | float | None = None):
        message = "Limite de requisições excedido na API do Spotify."
        extra = {"retry_after": retry_after} if retry_after is not None else {}
        super().__init__(code="rate_limited", message=message, status_code=429, extra=extra)

