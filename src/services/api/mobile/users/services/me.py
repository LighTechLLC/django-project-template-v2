from services.api.mobile.users.shemas import UserResponse


class MeService:
    def execute(self, request):
        user = request.user
        return UserResponse.model_validate(user)
