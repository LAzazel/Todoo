from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.repositories.user_repo import IUserRepository
from app.domain.models.user import User
from app.domain.value_objects.email import Email
from app.infrastructure.orm.models import UserORM
from app.infrastructure.mappers.user_mapper import UserMapper

class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: Email) -> Optional[User]:
        orm_model = self.session.query(UserORM).filter(UserORM.email == email.value).first()
        return UserMapper.to_domain(orm_model)

    def get_by_id(self, user_id: int) -> Optional[User]:
        orm_model = self.session.query(UserORM).filter(UserORM.id == user_id).first()
        return UserMapper.to_domain(orm_model)

    def get_all(self) -> List[User]:
        orm_models = self.session.query(UserORM).all()
        return [UserMapper.to_domain(m) for m in orm_models]

    def add(self, user: User) -> None:
        orm_model = UserMapper.to_orm(user)
        self.session.add(orm_model)
        self.session.commit()
        self.session.refresh(orm_model)
        user.id = orm_model.id

    def update(self, user: User) -> None:
        orm_model = UserMapper.to_orm(user)
        self.session.merge(orm_model)
        self.session.commit()

    def delete(self, user: User) -> None:
        orm_model = self.session.query(UserORM).filter(UserORM.id == user.id).first()
        if orm_model:
            self.session.delete(orm_model)
            self.session.commit()