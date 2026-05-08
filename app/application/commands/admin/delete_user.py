from dataclasses import dataclass
from app.domain.errors import UserNotFoundError, UnauthorizedAdminAccessError
from app.domain.repositories.user_repo import IUserRepository


@dataclass(frozen=True)
class DeleteUserCommand:
    target_user_id: int
    admin_role: str

class DeleteUserHandler:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, command: DeleteUserCommand) -> None:
        if command.admin_role != "admin":
            raise UnauthorizedAdminAccessError("Not enough permissions")

        user = self.user_repo.get_by_id(command.target_user_id)
        if not user:
            raise UserNotFoundError("User not found")

        self.user_repo.delete(user)