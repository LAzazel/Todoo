from dataclasses import dataclass
from typing import List
from app.modules.core.domain.repositories.user_repo import IUserRepository
from app.modules.core.application.read_models.user_read_model import UserReadModel
from app.modules.core.domain.errors import UnauthorizedAdminAccessError


@dataclass(frozen=True)
class GetAllUsersQuery:
    admin_role: str

class GetAllUsersHandler:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, query: GetAllUsersQuery) -> List[UserReadModel]:
        if query.admin_role != "admin":
            raise UnauthorizedAdminAccessError("Not enough permissions")

        users = self.user_repo.get_all()
        
        return [
            UserReadModel(
                id=user.id,
                email=user.email.value,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=user.phone_number,
                role=user.role
            ) for user in users
        ]