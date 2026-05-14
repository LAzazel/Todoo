from dataclasses import dataclass
from app.modules.core.domain.factories.todo_factory import TodoFactory
from app.modules.core.domain.repositories.todo_repo import ITodoRepository
from app.modules.core.infrastructure.audit.interfaces import IAuditService
from app.modules.core.infrastructure.audit.audit_log import AuditLog
from app.modules.core.integration_events import TodoCreatedIntegrationEvent
from app.modules.core.infrastructure.event_bus.interfaces import IEventBus


@dataclass(frozen=True)
class CreateTodoCommand:
    title: str
    description: str
    priority: int
    owner_id: int

class CreateTodoHandler:
    def __init__(self, todo_repo: ITodoRepository, todo_factory: TodoFactory, audit_service: IAuditService, event_bus: IEventBus):
        self.todo_repo = todo_repo
        self.todo_factory = todo_factory
        self.audit_service = audit_service
        self.event_bus = event_bus

    def execute(self, command: CreateTodoCommand) -> int:
        todo = self.todo_factory.create_todo(
            title=command.title,
            description=command.description,
            priority_val=command.priority,
            owner_id=command.owner_id
        )
        self.todo_repo.add(todo)
        
        try:
            self.audit_service.log(AuditLog(
                user_id=command.owner_id,
                action="todo_created",
                entity_id=todo.id,  
                details=command.title
            ))
        except Exception:
            pass

        integration_event = TodoCreatedIntegrationEvent(
            todo_id=todo.id,
            owner_id=todo.owner_id,
            priority=todo.priority
        )
        self.event_bus.publish(integration_event)

        return todo.id