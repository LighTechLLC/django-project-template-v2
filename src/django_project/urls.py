from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from oauth2_provider import urls as oauth2_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("oauth2/", include(oauth2_urls)),
    path("api/", include("services.api.urls")),
]
# disabled for non-debug mode or non-local prefix
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
