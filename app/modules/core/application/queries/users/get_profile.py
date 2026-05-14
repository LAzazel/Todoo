from dataclasses import dataclass
from app.modules.core.domain.repositories.user_repo import IUserRepository
from app.modules.core.application.read_models.user_read_model import UserReadModel
from app.modules.core.domain.errors import UserNotFoundError


@dataclass(frozen=True)
class GetProfileQuery:
    user_id: int

class GetProfileHandler:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, query: GetProfileQuery) -> UserReadModel:
        user = self.user_repo.get_by_id(query.user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        return UserReadModel(
            id=user.id,
            email=user.email.value,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            role=user.role
        )