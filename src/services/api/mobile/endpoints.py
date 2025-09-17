from ninja import Router

# Create mobile API router
router = Router()

router.add_router("users", "services.api.mobile.users.endpoints.router")
