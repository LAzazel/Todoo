from dataclasses import dataclass
from app.domain.errors import TodoNotFoundError
from app.domain.repositories.todo_repo import ITodoRepository
from app.infrastructure.audit.audit_log import AuditLog
from app.infrastructure.audit.interfaces import IAuditService


@dataclass(frozen=True)
class DeleteTodoCommand:
    todo_id: int
    owner_id: int

class DeleteTodoHandler:
    def __init__(self, todo_repo: ITodoRepository, audit_service: IAuditService):
        self.todo_repo = todo_repo
        self.audit_service = audit_service

    def execute(self, command: DeleteTodoCommand) -> None:
        todo = self.todo_repo.get_by_id(command.todo_id)
        if not todo or todo.owner_id != command.owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it.")

        title = todo.title
        self.todo_repo.delete(todo)

        try:
            self.audit_service.log(AuditLog(
                user_id=command.owner_id,
                action="todo_deleted",
                entity_id=command.todo_id,
                details=title
            ))
        except Exception:
            pass