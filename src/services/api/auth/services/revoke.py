import json
from django.http import HttpRequest
from oauth2_provider.oauth2_backends import get_oauthlib_core
from ninja.errors import ValidationError

from services.api.auth.schemas import (
    RevokeTokenResponse,
)

class RevokeTokenService:
    def execute(self, request: HttpRequest) -> RevokeTokenResponse:
            
        try:
            # Get the OAuth2 core (server + validator)
            oauthlib_core = get_oauthlib_core()
            
            # Process the token revocation using oauth2-toolkit's server
            url, headers, body, status = oauthlib_core.create_revocation_response(request)
            
            # RevokeTokenView always returns 200 for security reasons (RFC 7009)
            if status == 200:
                return RevokeTokenResponse()

            body_dict = json.loads(body)
            raise ValidationError({
                "error": body_dict.get("error", "server_error"),
                "error_description": body_dict.get("error_description", "Unknown error"),
            })
                    
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError({
                "error": "server_error",
                "error_description": str(e),
            })