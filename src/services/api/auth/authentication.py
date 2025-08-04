from ninja.security import HttpBearer
from django.http import HttpRequest
from oauth2_provider.models import AccessToken
from oauth2_provider.oauth2_backends import get_oauthlib_core
from oauthlib.common import Request
from typing import Optional, Dict, Any
from django.conf import settings


class OAuth2Bearer(HttpBearer):
    """
    OAuth2 Bearer Token Authentication for django-ninja
    """
    
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate using OAuth2 Bearer token
        """
        try:
            # Get the OAuth2 core
            oauthlib_core = get_oauthlib_core()
            
            # Create a mock request for token validation
            mock_request = Request(
                uri=request.build_absolute_uri(),
                http_method=request.method,
                headers=dict(request.headers),
                body=request.body.decode() if request.body else '',
            )
            
            # Validate the token
            valid, r = oauthlib_core.verify_request(mock_request, scopes=[])
            
            if valid:
                # Get the access token object
                access_token = AccessToken.objects.get(token=token)
                return {
                    'user': access_token.user,
                    'application': access_token.application,
                    'scope': access_token.scope,
                    'expires': access_token.expires,
                    'token': access_token,
                }
            return None
        except (AccessToken.DoesNotExist, Exception):
            return None


# OAuth2 authentication instance
oauth2_auth = OAuth2Bearer() 