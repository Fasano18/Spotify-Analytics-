from typing import Protocol

from pydantic import BaseModel, ConfigDict


class TokenData(BaseModel):
    """Representa os dados de token armazenados."""

    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None


class TokenStore(Protocol):
    """Contrato para armazenamento de tokens."""

    def save(self, token_data: TokenData) -> None:  # pragma: no cover - interface
        ...

    def get(self) -> TokenData | None:  # pragma: no cover - interface
        ...

    def clear(self) -> None:  # pragma: no cover - interface
        ...


class InMemoryTokenStore:
    """Implementação simples em memória do TokenStore.

    Em produção, pode ser facilmente substituída por Redis ou outro storage.
    """

    def __init__(self) -> None:
        self._token_data: TokenData | None = None

    def save(self, token_data: TokenData) -> None:
        self._token_data = token_data

    def get(self) -> TokenData | None:
        return self._token_data

    def clear(self) -> None:
        self._token_data = None

