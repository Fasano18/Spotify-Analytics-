from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TokenResponse(BaseModel):
    """Resposta de token do Spotify."""

    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., description="Token de acesso.")
    token_type: str = Field(..., description="Tipo do token (geralmente Bearer).")
    expires_in: int = Field(..., description="Tempo de expiração em segundos.")
    refresh_token: Optional[str] = Field(None, description="Token de refresh.")
    scope: Optional[str] = Field(None, description="Escopos concedidos.")


class AuthState(BaseModel):
    """Estado usado para proteção do fluxo OAuth2."""

    model_config = ConfigDict(from_attributes=True)

    state: str

