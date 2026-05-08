from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from typing import List

from app.application.commands.todos.create_todo import CreateTodoCommand, CreateTodoHandler
from app.application.commands.todos.update_todo import UpdateTodoCommand, UpdateTodoHandler
from app.application.commands.todos.delete_todo import DeleteTodoCommand, DeleteTodoHandler
from app.application.commands.todos.change_status import ChangeTodoStatusCommand, ChangeTodoStatusHandler

from app.application.queries.todos.get_todo import GetTodoQuery, GetTodoHandler
from app.application.queries.todos.get_all_todos import GetAllTodosQuery, GetAllTodosHandler

from app.presentation.dependencies import (
    get_create_todo_handler, 
    get_all_todos_handler,
    get_todo_handler,
    get_update_todo_handler,
    get_delete_todo_handler,
    get_change_status_handler,
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

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(
    request: TodoCreateRequest,
    handler: CreateTodoHandler = Depends(get_create_todo_handler),
    owner_id: int = Depends(get_current_user_id)
):
    command = CreateTodoCommand(title=request.title, description=request.description, priority=request.priority, owner_id=owner_id)
    return {"todo_id": handler.execute(command)}

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    handler: GetAllTodosHandler = Depends(get_all_todos_handler),
    owner_id: int = Depends(get_current_user_id)
):
    query = GetAllTodosQuery(owner_id=owner_id)
    return handler.execute(query)

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    handler: GetTodoHandler = Depends(get_todo_handler),
    owner_id: int = Depends(get_current_user_id)
):
    query = GetTodoQuery(todo_id=todo_id, owner_id=owner_id)
    return handler.execute(query)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    request: TodoUpdateRequest,
    handler: UpdateTodoHandler = Depends(get_update_todo_handler),
    owner_id: int = Depends(get_current_user_id)
):
    command = UpdateTodoCommand(todo_id=todo_id, title=request.title, description=request.description, priority=request.priority, owner_id=owner_id)
    handler.execute(command)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    handler: DeleteTodoHandler = Depends(get_delete_todo_handler),
    owner_id: int = Depends(get_current_user_id)
):
    command = DeleteTodoCommand(todo_id=todo_id, owner_id=owner_id)
    handler.execute(command)

@router.patch("/{todo_id}/status", status_code=status.HTTP_204_NO_CONTENT)
def change_todo_status(
    todo_id: int,
    complete: bool,
    handler: ChangeTodoStatusHandler = Depends(get_change_status_handler),
    owner_id: int = Depends(get_current_user_id)
):
    command = ChangeTodoStatusCommand(todo_id=todo_id, owner_id=owner_id, complete=complete)
    handler.execute(command)