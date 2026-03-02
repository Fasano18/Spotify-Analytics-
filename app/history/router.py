from fastapi import APIRouter, Depends, Query

from app.dependencies import get_spotify_client
from app.history.schemas import HistoryResponse
from app.history.service import get_recently_played
from app.spotify.client import SpotifyClient

router = APIRouter(prefix="/history", tags=["Histórico"])


@router.get(
    "",
    summary="Histórico recente de músicas",
    response_model=HistoryResponse,
)
async def history(
    limit: int = Query(50, ge=1, le=50, description="Quantidade de itens recentes a retornar (1-50)."),
    spotify_client: SpotifyClient = Depends(get_spotify_client),
) -> HistoryResponse:
    """Retorna o histórico recente de músicas reproduzidas pelo usuário."""

    return await get_recently_played(spotify_client, limit=limit)

