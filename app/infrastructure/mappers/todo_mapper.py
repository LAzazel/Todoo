from app.domain.models.todo import Todo
from app.domain.value_objects.priority import Priority
from app.infrastructure.orm.models import TodoORM

class TodoMapper:
    @staticmethod
    def to_domain(orm_model: TodoORM) -> Todo:
        if not orm_model:
            return None
        
        priority_vo = Priority(orm_model.priority)
        return Todo(
            id=orm_model.id,
            title=orm_model.title,
            description=orm_model.description,
            priority=priority_vo,
            owner_id=orm_model.owner_id,
            complete=orm_model.complete
        )

    @staticmethod
    def to_orm(domain_model: Todo) -> TodoORM:
        return TodoORM(
            id=domain_model.id,
            title=domain_model.title,
            description=domain_model.description,
            priority=domain_model.priority.value,
            owner_id=domain_model.owner_id,
            complete=domain_model.complete
        )