from ninja import Schema
from typing import Optional, Dict, Any


class TokenRequest(Schema):
    """OAuth2 Token Request Schema"""
    grant_type: str
    username: Optional[str] = None
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class TokenResponse(Schema):
    """OAuth2 Token Response Schema"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class TokenErrorResponse(Schema):
    """OAuth2 Token Error Response Schema"""
    error: str
    error_description: Optional[str] = None


class RevokeTokenRequest(Schema):
    """OAuth2 Token Revocation Request Schema"""
    token: str
    token_type_hint: Optional[str] = None


class RevokeTokenResponse(Schema):
    """OAuth2 Token Revocation Response Schema"""
    message: str = "Token revoked successfully" 