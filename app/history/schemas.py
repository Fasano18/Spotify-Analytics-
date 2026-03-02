from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.common.schemas import Pagination


class RecentlyPlayedItem(BaseModel):
    """Representa um item do histórico recente do usuário."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ID da faixa.")
    nome: str = Field(..., description="Nome da música.")
    artistas: List[str] = Field(..., description="Lista de artistas.")
    album: str = Field(..., description="Nome do álbum.")
    tocada_em: datetime = Field(..., description="Momento em que a faixa foi reproduzida.")
    duracao_ms: int = Field(..., description="Duração da faixa em milissegundos.")
    duracao_minutos: float = Field(..., description="Duração aproximada em minutos.")
    url_externa: Optional[str] = Field(None, description="URL pública da faixa no Spotify.")
    imagem_capa: Optional[str] = Field(None, description="URL da imagem de capa.")


class HistoryResponse(BaseModel):
    """Resposta de histórico de reprodução recente."""

    model_config = ConfigDict(from_attributes=True)

    itens: List[RecentlyPlayedItem] = Field(..., description="Itens de histórico.")
    paginacao: Pagination = Field(..., description="Informações de paginação.")

