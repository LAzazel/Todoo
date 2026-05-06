from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.models.todo import Todo
from app.infrastructure.orm.models import TodoORM
from app.infrastructure.mappers.todo_mapper import TodoMapper

class SQLAlchemyTodoRepository(ITodoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        orm_model = self.session.query(TodoORM).filter(TodoORM.id == todo_id).first()
        return TodoMapper.to_domain(orm_model)

    def get_all_by_owner_id(self, owner_id: int) -> List[Todo]:
        orm_models = self.session.query(TodoORM).filter(TodoORM.owner_id == owner_id).all()
        return [TodoMapper.to_domain(m) for m in orm_models]

    def get_all(self) -> List[Todo]:
        orm_models = self.session.query(TodoORM).all()
        return [TodoMapper.to_domain(m) for m in orm_models]

    def add(self, todo: Todo) -> None:
        orm_model = TodoMapper.to_orm(todo)
        self.session.add(orm_model)
        self.session.commit()
        self.session.refresh(orm_model)
        todo.id = orm_model.id

    def update(self, todo: Todo) -> None:
        orm_model = TodoMapper.to_orm(todo)
        self.session.merge(orm_model)
        self.session.commit()

    def delete(self, todo: Todo) -> None:
        orm_model = self.session.query(TodoORM).filter(TodoORM.id == todo.id).first()
        if orm_model:
            self.session.delete(orm_model)
            self.session.commit()