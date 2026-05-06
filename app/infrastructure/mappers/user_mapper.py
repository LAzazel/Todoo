from app.domain.models.user import User
from app.domain.value_objects.email import Email
from app.infrastructure.orm.models import UserORM


class UserMapper:
    @staticmethod
    def to_domain(orm_model: UserORM) -> User:
        if not orm_model:
            return None
        
        email_vo = Email(orm_model.email)
        user = User(
            id=orm_model.id,
            email=email_vo,
            password_hash=orm_model.password_hash,
            role=orm_model.role
        )
        return user

    @staticmethod
    def to_orm(domain_model: User) -> UserORM:
        return UserORM(
            id=domain_model.id,
            email=domain_model.email.value,
            password_hash=domain_model.password_hash,
            role=domain_model.role
        )