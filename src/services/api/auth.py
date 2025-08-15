from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest
from ninja.security import HttpBearer
from oauth2_provider.oauth2_backends import get_oauthlib_core


class AuthBearer(HttpBearer):

    def authenticate(self, request: HttpRequest, token: str):
        if request is None:
            return None
        oauthlib_core = get_oauthlib_core()

        try:
            valid, r = oauthlib_core.verify_request(request, scopes=[])
        except ValueError as error:
            if str(error) == "Invalid hex encoding in query string.":
                raise SuspiciousOperation(error)
            raise
        else:
            if valid:
                return r.user, r.access_token
        request.oauth2_error = getattr(r, "oauth2_error", {})
        return None
