from apps.users.models import User


class MeService:
    def execute(self, user: User):
        return user
