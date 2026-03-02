from functools import lru_cache

from fastapi import Depends

from app.auth.token_store import InMemoryTokenStore, TokenStore
from app.spotify.client import SpotifyClient


@lru_cache
def get_token_store() -> TokenStore:
    """Retorna uma instância singleton de TokenStore.

    Em produção, esta função pode ser modificada para utilizar Redis ou banco de dados.
    """

    return InMemoryTokenStore()


async def get_spotify_client(token_store: TokenStore = Depends(get_token_store)) -> SpotifyClient:
    """Factory de SpotifyClient para injeção de dependência.

    O ciclo de vida do client é gerenciado pelo FastAPI.
    """

    client = SpotifyClient(token_store=token_store)
    try:
        yield client
    finally:
        await client.close()

