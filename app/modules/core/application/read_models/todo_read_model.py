from dataclasses import dataclass

@dataclass(frozen=True)
class TodoReadModel:
    id: int
    title: str
    description: str
    priority: int
    owner_id: int
    complete: bool