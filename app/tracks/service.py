from typing import Any, Dict, List

from app.common.schemas import Pagination, TimeRange
from app.spotify import endpoints
from app.spotify.client import SpotifyClient
from app.tracks.schemas import TopTracksResponse, TrackResponse


def _to_track_response(item: Dict[str, Any]) -> TrackResponse:
    track = item["track"] if "track" in item else item
    artists = [a["name"] for a in track.get("artists", [])]
    album = track.get("album", {})
    images = album.get("images", [])
    imagem_capa = images[0]["url"] if images else None
    duracao_ms = track.get("duration_ms", 0)
    duracao_minutos = round(duracao_ms / 60000.0, 2) if duracao_ms else 0.0

    external_urls = track.get("external_urls") or {}
    
    # Extrai popularidade - pode estar no item ou no track
    popularidade = track.get("popularity") or item.get("popularity", 0)
    if popularidade is None:
        popularidade = 0

    return TrackResponse(
        id=track["id"],
        nome=track["name"],
        artistas=artists,
        album=album.get("name", ""),
        popularidade=int(popularidade),
        duracao_ms=duracao_ms,
        duracao_minutos=duracao_minutos,
        preview_url=track.get("preview_url"),
        url_externa=external_urls.get("spotify"),
        imagem_capa=imagem_capa,
    )


async def get_top_tracks(
    client: SpotifyClient,
    time_range: TimeRange,
    limit: int,
    offset: int = 0,
) -> TopTracksResponse:
    """Obtém as top músicas do usuário autenticado."""

    params = {
        "time_range": time_range.value,
        "limit": limit,
        "offset": offset,
    }
    data = await client.get(endpoints.ME_TOP_TRACKS_URL, params=params)
    items: List[Dict[str, Any]] = data.get("items", [])
    
    # Se a popularidade não vier da API, calcula baseado na posição (rank)
    # Top 1 = 100%, Top 2 = 95%, etc (decai 5% por posição)
    tracks = []
    for idx, item in enumerate(items):
        track_response = _to_track_response(item)
        # Se popularidade for 0, calcula baseado na posição
        if track_response.popularidade == 0:
            # Calcula popularidade baseada no rank (100 - (posição * 5))
            calculated_pop = max(10, 100 - (idx * 5))
            track_response.popularidade = calculated_pop
        tracks.append(track_response)
    total = data.get("total", len(tracks))

    pagination = Pagination(limite=limit, offset=offset, total=total)
    return TopTracksResponse(itens=tracks, paginacao=pagination)

