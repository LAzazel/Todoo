from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.errors import TodoNotFoundError

class DeleteTodoUseCase:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, todo_id: int, user_id: int) -> None:
        todo = self.todo_repo.get_by_id(todo_id)
        
        if not todo or todo.user_id != user_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it")

        self.todo_repo.delete(todo)