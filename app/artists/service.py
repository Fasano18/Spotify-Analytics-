from typing import Any, Dict, List

from app.common.schemas import Pagination, TimeRange
from app.spotify import endpoints
from app.spotify.client import SpotifyClient
from app.artists.schemas import ArtistResponse, TopArtistsResponse


def _to_artist_response(item: Dict[str, Any]) -> ArtistResponse:
    images = item.get("images") or []
    imagem = images[0]["url"] if images else None
    followers = (item.get("followers") or {}).get("total", 0)
    external_urls = item.get("external_urls") or {}
    
    # Extrai popularidade
    popularidade = item.get("popularity")
    if popularidade is None:
        popularidade = 0

    return ArtistResponse(
        id=item["id"],
        nome=item["name"],
        generos=item.get("genres", []),
        popularidade=int(popularidade),
        seguidores=followers,
        imagem_perfil=imagem,
        url_externa=external_urls.get("spotify"),
    )


async def get_top_artists(
    client: SpotifyClient,
    time_range: TimeRange,
    limit: int,
    offset: int = 0,
) -> TopArtistsResponse:
    """Obtém os top artistas do usuário autenticado."""

    params = {
        "time_range": time_range.value,
        "limit": limit,
        "offset": offset,
    }
    data = await client.get(endpoints.ME_TOP_ARTISTS_URL, params=params)
    items: List[Dict[str, Any]] = data.get("items", [])
    
    # Se a popularidade não vier da API, calcula baseado na posição (rank)
    # Top 1 = 100%, Top 2 = 95%, etc (decai 5% por posição)
    artists = []
    for idx, item in enumerate(items):
        artist_response = _to_artist_response(item)
        # Se popularidade for 0, calcula baseado na posição
        if artist_response.popularidade == 0:
            # Calcula popularidade baseada no rank (100 - (posição * 5))
            calculated_pop = max(10, 100 - (idx * 5))
            artist_response.popularidade = calculated_pop
        artists.append(artist_response)
    total = data.get("total", len(artists))

    pagination = Pagination(limite=limit, offset=offset, total=total)
    return TopArtistsResponse(itens=artists, paginacao=pagination)

