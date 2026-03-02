from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import RedirectResponse

from app.auth.schemas import TokenResponse
from app.auth.service import AuthService
from app.auth.token_store import TokenStore
from app.dependencies import get_token_store

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def get_auth_service(token_store: TokenStore = Depends(get_token_store)) -> AuthService:
    return AuthService(token_store=token_store)


@router.get("/login", summary="Inicia login com Spotify", response_class=RedirectResponse)
async def login(auth_service: AuthService = Depends(get_auth_service)) -> RedirectResponse:
    """Redireciona o usuário para a página de login do Spotify (fluxo OAuth2)."""

    login_url = auth_service.build_login_url()
    return RedirectResponse(url=login_url, status_code=302)


@router.get(
    "/callback",
    summary="Callback do OAuth2 do Spotify",
    response_model=TokenResponse,
)
async def callback(
    code: str = Query(..., description="Código de autorização recebido do Spotify."),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Recebe o código de autorização do Spotify e troca por um token de acesso."""

    return await auth_service.exchange_code_for_token(code=code)


@router.get(
    "/logout",
    summary="Logout da sessão atual",
    status_code=204,
    response_class=Response,
)
async def logout(auth_service: AuthService = Depends(get_auth_service)) -> Response:
    """Limpa o token armazenado, efetivamente realizando o logout."""

    auth_service.logout()
    return Response(status_code=204)

