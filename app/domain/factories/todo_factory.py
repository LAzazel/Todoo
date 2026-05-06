from app.domain.models.todo import Todo
from app.domain.value_objects.priority import Priority


class TodoFactory:
    def create_todo(self, title: str, description: str, priority_val: int, user_id: int) -> Todo:
        priority = Priority(priority_val)
        
        return Todo(
            id=None,
            title=title,
            description=description,
            priority=priority,
            user_id=user_id
        )