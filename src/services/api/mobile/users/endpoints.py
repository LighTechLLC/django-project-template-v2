from ninja import Router

from services.api.mobile.users.services.me import MeService
from services.api.mobile.users.shemas import UserResponse

router = Router()


@router.get("me", response=UserResponse)
def get_me(request) -> UserResponse:
    user, _ = request.auth

    serice = MeService()
    result = serice.execute(user)
    return result
