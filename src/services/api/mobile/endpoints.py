from ninja import Router

from services.api.auth import AuthBearer

# Create mobile API router
router = Router()

router.add_router("users", "services.api.mobile.users.endpoints.router")
