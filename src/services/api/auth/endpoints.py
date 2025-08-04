from django.http import HttpRequest
from ninja import Router

from services.api.auth.services import (
    TokenService,
    RevokeTokenService,
)
from services.api.auth.schemas import (
    TokenResponse,
    TokenErrorResponse,
    RevokeTokenResponse,
)


# Create router for OAuth2 endpoints
router = Router(tags=["auth"])


@router.post("/token", response={200: TokenResponse, 400: TokenErrorResponse, 401: TokenErrorResponse})
def token_endpoint(request: HttpRequest):
    """
    OAuth2 Token Endpoint (RFC 6749 Section 3.2)
    Uses oauth2-toolkit's server class directly
    """

    token_service = TokenService()
    response = token_service.execute(request)
    return response


@router.post("/revoke", response={200: RevokeTokenResponse, 400: TokenErrorResponse})
def revoke_token_endpoint(request: HttpRequest):
    """
    OAuth2 Token Revocation Endpoint (RFC 7009)
    Uses oauth2-toolkit's server class directly
    """
    revoke_token_service = RevokeTokenService()
    response = revoke_token_service.execute(request)
    return response
