from typing import List
from app.application.dto.todo_dto import TodoResponseDTO
from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.errors import TodoNotFoundError


class GetTodoUseCase:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, todo_id: int, user_id: int) -> TodoResponseDTO:
        todo = self.todo_repo.get_by_id(todo_id)
        
        if not todo or todo.user_id != user_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it")
            
        return TodoResponseDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            priority=todo.priority.value,
            user_id=todo.user_id
        )

class GetAllUserTodosUseCase:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, user_id: int) -> List[TodoResponseDTO]:
        todos = self.todo_repo.get_all_by_user_id(user_id)
        
        return [
            TodoResponseDTO(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                priority=todo.priority.value,
                user_id=todo.user_id
            ) for todo in todos
        ]