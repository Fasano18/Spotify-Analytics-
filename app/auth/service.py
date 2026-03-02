import secrets
import urllib.parse
from typing import Dict

import httpx

from app.auth.schemas import TokenResponse
from app.auth.token_store import TokenData, TokenStore
from app.config import settings
from app.spotify import endpoints

SCOPES = [
    "user-read-email",
    "user-read-private",
    "user-top-read",
    "user-read-recently-played",
    "playlist-read-private",
    "playlist-read-collaborative",
]


class AuthService:
    """Responsável pelo fluxo OAuth2 com o Spotify."""

    def __init__(self, token_store: TokenStore) -> None:
        self._token_store = token_store

    def build_login_url(self, state: str | None = None) -> str:
        """Constrói a URL de login do Spotify."""

        if state is None:
            state = secrets.token_urlsafe(16)

        query = {
            "response_type": "code",
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "scope": " ".join(SCOPES),
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "state": state,
        }
        return f"{endpoints.AUTH_AUTHORIZE_URL}?{urllib.parse.urlencode(query)}"

    async def exchange_code_for_token(self, code: str) -> TokenResponse:
        """TROCA o código de autorização por um access token/refresh token."""

        async with httpx.AsyncClient() as client:
            data: Dict[str, str] = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": str(settings.SPOTIFY_REDIRECT_URI),
                "client_id": settings.SPOTIFY_CLIENT_ID,
                "client_secret": settings.SPOTIFY_CLIENT_SECRET,
            }
            resp = await client.post(endpoints.AUTH_TOKEN_URL, data=data)
            resp.raise_for_status()
            payload = resp.json()

        token_response = TokenResponse.model_validate(payload)
        self._token_store.save(
            TokenData(
                access_token=token_response.access_token,
                refresh_token=token_response.refresh_token,
                token_type=token_response.token_type,
                expires_in=token_response.expires_in,
            )
        )
        return token_response

    def logout(self) -> None:
        """Remove os tokens armazenados."""

        self._token_store.clear()

