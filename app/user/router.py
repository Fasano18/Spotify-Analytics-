from fastapi import APIRouter, Depends

from app.dependencies import get_spotify_client
from app.spotify.client import SpotifyClient
from app.user.schemas import UserResponse
from app.user.service import get_user_info

router = APIRouter(tags=["Usuário"])


@router.get(
    "/me",
    summary="Informações do usuário autenticado",
    response_model=UserResponse,
)
async def me(spotify_client: SpotifyClient = Depends(get_spotify_client)) -> UserResponse:
    """Retorna as informações do usuário autenticado."""

    return await get_user_info(spotify_client)
