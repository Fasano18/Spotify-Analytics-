from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TimeRange(str, Enum):
    """Intervalo de tempo para análises de top artistas e músicas."""

    short_term = "short_term"
    medium_term = "medium_term"
    long_term = "long_term"


class Pagination(BaseModel):
    """Informações de paginação retornadas pela API."""

    model_config = ConfigDict(from_attributes=True)

    limite: int = Field(..., description="Quantidade de itens retornados.")
    offset: int = Field(..., description="Offset atual.")
    total: Optional[int] = Field(None, description="Total de itens disponíveis.")


class ErrorResponse(BaseModel):
    """Estrutura padrão de respostas de erro."""

    model_config = ConfigDict(from_attributes=True)

    codigo: str = Field(..., description="Código de erro interno ou do Spotify.")
    mensagem: str = Field(..., description="Descrição em português do erro.")

