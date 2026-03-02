from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.common.schemas import Pagination


class TrackResponse(BaseModel):
    """Representa uma faixa musical do Spotify."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ID da faixa no Spotify.")
    nome: str = Field(..., description="Nome da música.")
    artistas: List[str] = Field(..., description="Lista de artistas principais.")
    album: str = Field(..., description="Nome do álbum.")
    popularidade: int = Field(..., ge=0, le=100, description="Popularidade da faixa (0-100).")
    duracao_ms: int = Field(..., description="Duração da faixa em milissegundos.")
    duracao_minutos: float = Field(..., description="Duração aproximada em minutos.")
    preview_url: Optional[str] = Field(None, description="URL de preview de 30s, se disponível.")
    url_externa: Optional[str] = Field(None, description="URL pública da faixa no Spotify.")
    imagem_capa: Optional[str] = Field(None, description="URL da imagem de capa do álbum.")


class TopTracksResponse(BaseModel):
    """Resposta para listagem de top músicas do usuário."""

    model_config = ConfigDict(from_attributes=True)

    itens: List[TrackResponse] = Field(..., description="Lista de faixas do usuário.")
    paginacao: Pagination = Field(..., description="Informações de paginação.")

