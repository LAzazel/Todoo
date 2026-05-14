from dataclasses import dataclass
from app.modules.core.domain.errors import UserNotFoundError
from app.modules.core.domain.repositories.user_repo import IUserRepository
from app.modules.core.application.events.user_events import UserPhoneChanged
from app.modules.core.infrastructure.event_bus.interfaces import IEventBus


@dataclass(frozen=True)
class ChangePhoneCommand:
    user_id: int
    new_phone: str

class ChangePhoneHandler:
    def __init__(self, user_repo: IUserRepository, event_bus: IEventBus):
        self.user_repo = user_repo
        self.event_bus = event_bus

    def execute(self, command: ChangePhoneCommand) -> None:
        user = self.user_repo.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError("User not found")

        user.update_phone_number(command.new_phone)
        self.user_repo.update(user)

        self.event_bus.publish(UserPhoneChanged(
            user_id=command.user_id,
            new_phone=command.new_phone
        ))