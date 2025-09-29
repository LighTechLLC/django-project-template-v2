import hashlib
import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView as BaseTokenView

from .schemas import TokenUser


class TokenView(BaseTokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            parsed_body = json.loads(body)
            access_token = parsed_body.get("access_token")

            if access_token is not None:
                token_checksum = hashlib.sha256(
                    access_token.encode("utf-8")
                ).hexdigest()
                token = (
                    get_access_token_model()
                    .objects.select_related("user")
                    .get(token_checksum=token_checksum)
                )
                app_authorized.send(sender=self, request=request, token=token)

                # customize response
                parsed_body["user"] = TokenUser.model_validate(
                    token.user
                ).model_dump(by_alias=True)

                body = json.dumps(parsed_body, default=str)

        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response
