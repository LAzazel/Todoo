from dataclasses import dataclass
from app.domain.errors import UserNotFoundError, UnauthorizedAdminAccessError
from app.domain.repositories.user_repo import IUserRepository
from app.infrastructure.event_bus.interfaces import IEventBus
from app.application.events.user_events import UserDeleted


@dataclass(frozen=True)
class DeleteUserCommand:
    target_user_id: int
    admin_role: str

class DeleteUserHandler:
    def __init__(self, user_repo: IUserRepository, event_bus: IEventBus):
        self.user_repo = user_repo
        self.event_bus = event_bus

    def execute(self, command: DeleteUserCommand) -> None:
        if command.admin_role != "admin":
            raise UnauthorizedAdminAccessError("Not enough permissions")

        user = self.user_repo.get_by_id(command.target_user_id)
        if not user:
            raise UserNotFoundError("User not found")

        username = user.username
        self.user_repo.delete(user)

        self.event_bus.publish(UserDeleted(
            user_id=command.target_user_id,
            username=username
        ))
