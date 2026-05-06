from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.errors import TodoNotFoundError

class ChangeTodoStatusUseCase:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, todo_id: int, owner_id: int, complete: bool) -> None:
        todo = self.todo_repo.get_by_id(todo_id)
        if not todo or todo.owner_id != owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it")

        if complete:
            todo.mark_as_completed()
        else:
            todo.mark_as_incomplete()
            
        self.todo_repo.update(todo)