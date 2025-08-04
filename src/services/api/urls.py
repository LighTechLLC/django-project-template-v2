from django.urls import path

from services.api.api import api

urlpatterns = [
    path("", api.urls),
]
