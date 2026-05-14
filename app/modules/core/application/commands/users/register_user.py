from dataclasses import dataclass
from app.modules.core.domain.factories.user_factory import UserFactory
from app.modules.core.domain.repositories.user_repo import IUserRepository
from app.modules.core.application.interfaces.auth_services import IPasswordHasher
from app.modules.core.infrastructure.audit.audit_log import AuditLog
from app.modules.core.infrastructure.audit.interfaces import IAuditService
from app.modules.core.integration_events import UserRegisteredIntegrationEvent


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str
    username: str
    first_name: str
    last_name: str
    phone_number: str

class RegisterUserHandler:
    def __init__(self, user_repo: IUserRepository, user_factory: UserFactory, password_hasher: IPasswordHasher, audit_service: IAuditService, event_bus):
        self.user_repo = user_repo
        self.user_factory = user_factory
        self.password_hasher = password_hasher
        self.audit_service = audit_service
        self.event_bus = event_bus

    def execute(self, command: RegisterUserCommand) -> int:
        hashed_password = self.password_hasher.hash(command.password)
        
        user = self.user_factory.create_user(
            username=command.username,
            email=command.email,
            first_name=command.first_name,
            last_name=command.last_name,
            hashed_password=hashed_password,
            phone_number=command.phone_number
        )
        self.user_repo.add(user)

        try:
            self.audit_service.log(AuditLog(
                user_id=user.id,
                action="user_registered",
                entity_id=user.id,
                details=command.username
            ))
        except Exception:
            pass

        integration_event = UserRegisteredIntegrationEvent(
            user_id=user.id,
            email=user.email
        )
        self.event_bus.publish(integration_event)
        
        return user.id