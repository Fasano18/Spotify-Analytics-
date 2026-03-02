import asyncio
import base64
from typing import Any, Dict, Optional

import httpx

from app.auth.token_store import TokenData, TokenStore
from app.config import settings
from app.spotify import endpoints
from app.spotify.exceptions import RateLimitError, SpotifyAPIError, TokenExpiredError


class SpotifyClient:
    """Cliente HTTP assíncrono para a API do Spotify.

    Responsável por:
    - anexar o token de acesso automaticamente;
    - fazer refresh do token quando necessário;
    - lidar com rate limiting (HTTP 429) respeitando o cabeçalho Retry-After.
    """

    def __init__(self, token_store: TokenStore, timeout: float | None = None) -> None:
        self._token_store = token_store
        self._timeout = timeout or settings.REQUEST_TIMEOUT_SECONDS
        self._client = httpx.AsyncClient(timeout=self._timeout)

    async def close(self) -> None:
        await self._client.aclose()

    def _get_auth_header(self) -> Dict[str, str]:
        token_data = self._token_store.get()
        if not token_data:
            raise TokenExpiredError("Token não encontrado. Faça login para continuar.")
        return {"Authorization": f"Bearer {token_data.access_token}"}

    async def _refresh_token(self) -> None:
        token_data = self._token_store.get()
        if not token_data or not token_data.refresh_token:
            raise TokenExpiredError()

        basic = base64.b64encode(
            f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()
        ).decode()

        data = {
            "grant_type": "refresh_token",
            "refresh_token": token_data.refresh_token,
        }

        resp = await self._client.post(
            endpoints.AUTH_TOKEN_URL,
            data=data,
            headers={"Authorization": f"Basic {basic}"},
        )

        if resp.status_code != 200:
            raise TokenExpiredError("Não foi possível renovar o token de acesso.")

        payload = resp.json()
        new_token = TokenData(
            access_token=payload["access_token"],
            refresh_token=payload.get("refresh_token", token_data.refresh_token),
            token_type=payload.get("token_type", "Bearer"),
            expires_in=payload.get("expires_in"),
        )
        self._token_store.save(new_token)

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executa uma requisição GET na API do Spotify com tratamento de erros.

        - Reaplica a requisição quando recebe 401 (token expirado) após tentar refresh.
        - Respeita Retry-After em caso de 429.
        """

        retries = 0
        while True:
            headers = self._get_auth_header()
            response = await self._client.get(url, params=params, headers=headers)

            if response.status_code == 200:
                return response.json()

            if response.status_code == 401 and retries < 1:
                # tenta refresh do token e repete a requisição
                try:
                    await self._refresh_token()
                    retries += 1
                    continue
                except TokenExpiredError:
                    # Se o refresh falhar, levanta erro para o usuário fazer login novamente
                    raise TokenExpiredError("Sua sessão expirou. Faça login novamente.")

            if response.status_code == 429:
                retry_after_header = response.headers.get("Retry-After", "1")
                try:
                    retry_after = float(retry_after_header)
                except ValueError:
                    retry_after = 1.0
                await asyncio.sleep(retry_after)
                raise RateLimitError(retry_after=retry_after)

            if response.status_code >= 500:
                raise SpotifyAPIError("Erro interno da API do Spotify.", status_code=502)

            # erros 4xx em geral
            try:
                payload = response.json()
                message = payload.get("error_description") or payload.get("error", {}).get(
                    "message", "Erro ao chamar a API do Spotify."
                )
            except Exception:  # pragma: no cover - fallback de parsing
                message = "Erro ao chamar a API do Spotify."
            raise SpotifyAPIError(message, status_code=response.status_code)

