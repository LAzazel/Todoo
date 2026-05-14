from dataclasses import dataclass

@dataclass
class SystemStats:
    total_todos_created: int = 0
    total_todos_completed: int = 0
    high_priority_todos: int = 0
    total_users_registered: int = 0

@dataclass
class TodoActivityRecorded:
    is_high_priority: bool