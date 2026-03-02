from fastapi import APIRouter, Depends, Query

from app.common.schemas import TimeRange
from app.dependencies import get_spotify_client
from app.spotify.client import SpotifyClient
from app.tracks.schemas import TopTracksResponse
from app.tracks.service import get_top_tracks

router = APIRouter(prefix="/top", tags=["Top Músicas"])


@router.get(
    "/tracks",
    summary="Lista as top músicas do usuário autenticado",
    response_model=TopTracksResponse,
)
async def top_tracks(
    time_range: TimeRange = Query(TimeRange.medium_term, description="Intervalo de tempo para análise."),
    limit: int = Query(20, ge=1, le=50, description="Quantidade de músicas a retornar (1-50)."),
    spotify_client: SpotifyClient = Depends(get_spotify_client),
) -> TopTracksResponse:
    """Retorna as músicas mais ouvidas pelo usuário em um determinado período."""

    return await get_top_tracks(spotify_client, time_range=time_range, limit=limit)

