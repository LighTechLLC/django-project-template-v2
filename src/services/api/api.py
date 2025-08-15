from ninja import NinjaAPI
from ninja.errors import ValidationError

from services.api.auth import AuthBearer
from services.api.mobile.endpoints import router as mobile_api

# Create the main API instance
api = NinjaAPI(
    title="Django Project API",
    description="API with OAuth2 authentication",
    version="1.0",
    csrf=False,
    auth=AuthBearer(),
)


@api.exception_handler(ValidationError)
def validation_error(request, exc):
    return api.create_response(
        request,
        exc.errors,
        status=400,
    )


# Include the mobile API router
api.add_router("/mobile", mobile_api)
