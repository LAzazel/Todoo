from typing import List
from app.application.dto.todo_dto import TodoResponseDTO
from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.errors import TodoNotFoundError


class GetTodoUseCase:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, todo_id: int, owner_id: int) -> TodoResponseDTO:
        todo = self.todo_repo.get_by_id(todo_id)
        
        if not todo or todo.owner_id != owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it")
            
        return TodoResponseDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            priority=todo.priority.value,
            owner_id=todo.owner_id,
            complete=todo.complete
        )

class GetAllUserTodosUseCase:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, owner_id: int) -> List[TodoResponseDTO]:
        todos = self.todo_repo.get_all_by_owner_id(owner_id)
        
        return [
            TodoResponseDTO(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                priority=todo.priority.value,
                owner_id=todo.owner_id,
                complete=todo.complete
            ) for todo in todos
        ]