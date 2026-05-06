from app.domain.repositories.user_repo import IUserRepository
from app.domain.errors import DomainError, UserNotFoundError


class AdminDeleteUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, target_user_id: int, admin_role: str) -> None:
        if admin_role != "admin":
            raise DomainError("Not enough rights to perform this operation")
            
        user = self.user_repo.get_by_id(target_user_id)
        if not user:
            raise UserNotFoundError("User not found")
            
        self.user_repo.delete(user)