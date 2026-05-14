from dataclasses import dataclass
from app.modules.core.domain.factories.todo_factory import TodoFactory
from app.modules.core.domain.repositories.todo_repo import ITodoRepository
from app.modules.core.infrastructure.audit.interfaces import IAuditService
from app.modules.core.infrastructure.audit.audit_log import AuditLog


@dataclass(frozen=True)
class CreateTodoCommand:
    title: str
    description: str
    priority: int
    owner_id: int

class CreateTodoHandler:
    def __init__(self, todo_repo: ITodoRepository, todo_factory: TodoFactory, audit_service: IAuditService):
        self.todo_repo = todo_repo
        self.todo_factory = todo_factory
        self.audit_service = audit_service

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

        return todo.id