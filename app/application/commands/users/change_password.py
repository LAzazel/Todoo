from dataclasses import dataclass
from app.domain.errors import UserNotFoundError
from app.domain.repositories.user_repo import IUserRepository
from app.application.interfaces.auth_services import IPasswordHasher


@dataclass(frozen=True)
class ChangePasswordCommand:
    user_id: int
    new_password: str

class ChangePasswordHandler:
    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def execute(self, command: ChangePasswordCommand) -> None:
        user = self.user_repo.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError("User not found")

        new_hashed = self.password_hasher.hash(command.new_password)
        user.change_password(new_hashed)
        
        self.user_repo.update(user)