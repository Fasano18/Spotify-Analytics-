from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.common.schemas import Pagination


class ArtistResponse(BaseModel):
    """Representa um artista do Spotify."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ID do artista no Spotify.")
    nome: str = Field(..., description="Nome do artista.")
    generos: List[str] = Field(default_factory=list, description="Gêneros associados ao artista.")
    popularidade: int = Field(..., ge=0, le=100, description="Popularidade do artista (0-100).")
    seguidores: int = Field(..., ge=0, description="Quantidade de seguidores no Spotify.")
    imagem_perfil: Optional[str] = Field(None, description="URL da imagem principal do artista.")
    url_externa: Optional[str] = Field(None, description="URL pública do artista no Spotify.")


class TopArtistsResponse(BaseModel):
    """Resposta para listagem de top artistas do usuário."""

    model_config = ConfigDict(from_attributes=True)

    itens: List[ArtistResponse] = Field(..., description="Lista de artistas do usuário.")
    paginacao: Pagination = Field(..., description="Informações de paginação.")

