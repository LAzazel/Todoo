from dataclasses import dataclass
from app.domain.errors import TodoNotFoundError
from app.domain.repositories.todo_repo import ITodoRepository


@dataclass(frozen=True)
class DeleteTodoCommand:
    todo_id: int
    owner_id: int

class DeleteTodoHandler:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, command: DeleteTodoCommand) -> None:
        todo = self.todo_repo.get_by_id(command.todo_id)
        if not todo or todo.owner_id != command.owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it.")

        self.todo_repo.delete(todo)