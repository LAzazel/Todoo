from dataclasses import dataclass

@dataclass(frozen=True)
class CreateTodoDTO:
    title: str
    description: str
    priority: int

@dataclass(frozen=True)
class UpdateTodoDTO:
    title: str
    description: str
    priority: int

@dataclass(frozen=True)
class TodoResponseDTO:
    id: int
    title: str
    description: str
    priority: int
    user_id: int