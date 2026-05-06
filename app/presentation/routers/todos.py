from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from typing import List

from app.application.dto.todo_dto import CreateTodoDTO, UpdateTodoDTO, TodoResponseDTO
from app.application.use_cases.todos.create import CreateTodoUseCase
from app.application.use_cases.todos.get import GetAllUserTodosUseCase, GetTodoUseCase
from app.application.use_cases.todos.update import UpdateTodoUseCase
from app.application.use_cases.todos.delete import DeleteTodoUseCase
from app.application.use_cases.todos.status import ChangeTodoStatusUseCase

from app.presentation.dependencies import (
    get_create_todo_use_case, 
    get_all_user_todos_use_case,
    get_todo_use_case,
    get_update_todo_use_case,
    get_delete_todo_use_case,
    get_change_todo_status_use_case,
    get_current_user_id
)


router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


class TodoCreateRequest(BaseModel):
    title: str
    description: str
    priority: int

class TodoUpdateRequest(BaseModel):
    title: str
    description: str
    priority: int

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    owner_id: int
    complete: bool

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    request: TodoCreateRequest,
    use_case: CreateTodoUseCase = Depends(get_create_todo_use_case),
    owner_id: int = Depends(get_current_user_id)
):
    dto = CreateTodoDTO(title=request.title, description=request.description, priority=request.priority)
    return use_case.execute(dto, owner_id)

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    use_case: GetAllUserTodosUseCase = Depends(get_all_user_todos_use_case),
    owner_id: int = Depends(get_current_user_id)
):
    return use_case.execute(owner_id)

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    use_case: GetTodoUseCase = Depends(get_todo_use_case),
    owner_id: int = Depends(get_current_user_id)
):
    return use_case.execute(todo_id, owner_id)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    request: TodoUpdateRequest,
    use_case: UpdateTodoUseCase = Depends(get_update_todo_use_case),
    owner_id: int = Depends(get_current_user_id)
):
    dto = UpdateTodoDTO(title=request.title, description=request.description, priority=request.priority)
    return use_case.execute(todo_id, dto, owner_id=owner_id)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    use_case: DeleteTodoUseCase = Depends(get_delete_todo_use_case),
    owner_id: int = Depends(get_current_user_id)
):
    use_case.execute(todo_id, owner_id)

@router.patch("/{todo_id}/status", status_code=status.HTTP_204_NO_CONTENT)
def change_todo_status(
    todo_id: int,
    complete: bool,
    use_case: ChangeTodoStatusUseCase = Depends(get_change_todo_status_use_case),
    owner_id: int = Depends(get_current_user_id)
):
    use_case.execute(todo_id=todo_id, owner_id=owner_id, complete=complete)