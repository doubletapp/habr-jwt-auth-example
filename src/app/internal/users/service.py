from app.internal.users.dto import UserProfileDTO
from app.internal.users.models import APIUser


class MeService:
    def get_me(self, user: APIUser) -> UserProfileDTO:
        return UserProfileDTO.from_orm(user)
