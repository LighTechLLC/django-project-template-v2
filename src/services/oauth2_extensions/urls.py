from django.urls import path
from oauth2_provider import views as oauth2_views

from services.oauth2_extensions.token_view import TokenView

urlpatterns = [
    path("token/", TokenView.as_view(), name="token"),
    path(
        "revoke_token/",
        oauth2_views.RevokeTokenView.as_view(),
        name="revoke-token",
    ),
    path(
        "introspect/",
        oauth2_views.IntrospectTokenView.as_view(),
        name="introspect",
    ),
]
