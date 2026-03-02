from typing import Any, Dict

from app.spotify import endpoints
from app.spotify.client import SpotifyClient
from app.user.schemas import UserResponse


async def get_user_info(client: SpotifyClient) -> UserResponse:
    """Obtém informações do usuário autenticado."""

    data: Dict[str, Any] = await client.get(endpoints.ME_URL)
    
    images = data.get("images", [])
    imagem_perfil = images[0]["url"] if images else None
    
    external_urls = data.get("external_urls") or {}
    
    return UserResponse(
        id=data["id"],
        nome=data.get("display_name") or data.get("id", "Usuário"),
        email=data.get("email"),
        imagem_perfil=imagem_perfil,
        pais=data.get("country"),
        seguidores=data.get("followers", {}).get("total"),
    )
