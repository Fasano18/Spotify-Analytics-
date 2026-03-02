from fastapi import APIRouter, Depends, Query

from app.common.schemas import TimeRange
from app.dependencies import get_spotify_client
from app.spotify.client import SpotifyClient
from app.artists.schemas import TopArtistsResponse
from app.artists.service import get_top_artists

router = APIRouter(prefix="/top", tags=["Top Artistas"])


@router.get(
    "/artists",
    summary="Lista os top artistas do usuário autenticado",
    response_model=TopArtistsResponse,
)
async def top_artists(
    time_range: TimeRange = Query(TimeRange.medium_term, description="Intervalo de tempo para análise."),
    limit: int = Query(20, ge=1, le=50, description="Quantidade de artistas a retornar (1-50)."),
    spotify_client: SpotifyClient = Depends(get_spotify_client),
) -> TopArtistsResponse:
    """Retorna os artistas mais ouvidos pelo usuário em um determinado período."""

    return await get_top_artists(spotify_client, time_range=time_range, limit=limit)

