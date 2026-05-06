from app.domain.models.todo import Todo
from app.domain.value_objects.priority import Priority


class TodoFactory:
    def create_todo(self, title: str, description: str, priority_val: int, owner_id: int) -> Todo:
        priority = Priority(priority_val)
        

        return Todo(
                title=title,
                description=description,
                priority=priority,
                owner_id=owner_id,
                complete=False
            )