from django.urls import include, path

from services.api.mobile.urls import urlpatterns as mobile_urls

app_name = "api"

urlpatterns = [
    path("mobile/", include((mobile_urls, "mobile"), namespace="mobile")),
]
