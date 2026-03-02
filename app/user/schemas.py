from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    """Dados do usuário autenticado."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ID do usuário no Spotify.")
    nome: str = Field(..., description="Nome de exibição do usuário.")
    email: Optional[str] = Field(None, description="Email do usuário.")
    imagem_perfil: Optional[str] = Field(None, description="URL da imagem de perfil.")
    pais: Optional[str] = Field(None, description="País do usuário.")
    seguidores: Optional[int] = Field(None, description="Número de seguidores.")
