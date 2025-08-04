import json
from django.http import HttpRequest
from oauth2_provider.oauth2_backends import get_oauthlib_core
from ninja.errors import ValidationError

from services.api.auth.schemas import (
    TokenResponse,
    TokenErrorResponse,
)


class TokenService:
    def execute(self, request: HttpRequest) -> TokenResponse | TokenErrorResponse:
        try:
            # Get the OAuth2 core (server + validator)
            oauthlib_core = get_oauthlib_core()

            # Process the token request using oauth2-toolkit's server
            url, headers, body, status = oauthlib_core.create_token_response(request)
            
            if status == 200:
                return TokenResponse.model_validate_json(body)
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