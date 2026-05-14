from dataclasses import dataclass
from app.modules.core.domain.repositories.todo_repo import ITodoRepository
from app.modules.core.application.read_models.todo_read_model import TodoReadModel
from app.modules.core.domain.errors import TodoNotFoundError


@dataclass(frozen=True)
class GetTodoQuery:
    todo_id: int
    owner_id: int

class GetTodoHandler:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, query: GetTodoQuery) -> TodoReadModel:
        todo = self.todo_repo.get_by_id(query.todo_id)
        if not todo or todo.owner_id != query.owner_id:
            raise TodoNotFoundError("Todo not found")

        return TodoReadModel(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            priority=todo.priority.value,
            owner_id=todo.owner_id,
            complete=todo.complete
        )