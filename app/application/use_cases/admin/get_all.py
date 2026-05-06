from typing import List
from app.application.dto.user_dto import UserResponseDTO
from app.domain.repositories.user_repo import IUserRepository
from app.domain.errors import UnauthorizedAdminAccessError


class AdminGetAllUsersUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, admin_role: str) -> List[UserResponseDTO]:
        if admin_role != "admin":
            raise UnauthorizedAdminAccessError("Not enough rights to perform this operation")

        users = self.user_repo.get_all()
        
        return [
            UserResponseDTO(
                id=user.id,
                email=user.email.value
            ) for user in users
        ]