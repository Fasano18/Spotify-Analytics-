from datetime import datetime
from typing import Any, Dict, List

from app.common.schemas import Pagination
from app.spotify import endpoints
from app.spotify.client import SpotifyClient
from app.history.schemas import HistoryResponse, RecentlyPlayedItem


def _to_recently_played_item(item: Dict[str, Any]) -> RecentlyPlayedItem:
    track = item["track"]
    artists = [a["name"] for a in track.get("artists", [])]
    album = track.get("album", {})
    images = album.get("images", [])
    imagem_capa = images[0]["url"] if images else None
    duracao_ms = track.get("duration_ms", 0)
    duracao_minutos = round(duracao_ms / 60000.0, 2) if duracao_ms else 0.0
    external_urls = track.get("external_urls") or {}

    return RecentlyPlayedItem(
        id=track["id"],
        nome=track["name"],
        artistas=artists,
        album=album.get("name", ""),
        tocada_em=datetime.fromisoformat(item["played_at"].replace("Z", "+00:00")),
        duracao_ms=duracao_ms,
        duracao_minutos=duracao_minutos,
        url_externa=external_urls.get("spotify"),
        imagem_capa=imagem_capa,
    )


async def get_recently_played(
    client: SpotifyClient,
    limit: int,
) -> HistoryResponse:
    """Obtém o histórico recente de faixas tocadas pelo usuário."""

    params = {"limit": limit}
    data = await client.get(endpoints.ME_PLAYER_RECENTLY_PLAYED_URL, params=params)
    items: List[Dict[str, Any]] = data.get("items", [])
    history_items = [_to_recently_played_item(item) for item in items]

    pagination = Pagination(limite=limit, offset=0, total=len(history_items))
    return HistoryResponse(itens=history_items, paginacao=pagination)

