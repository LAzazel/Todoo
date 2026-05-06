from app.domain.models.user import User
from app.domain.value_objects.email import Email
from app.infrastructure.orm.models import UserORM


class UserMapper:
    @staticmethod
    def to_domain(orm_model: UserORM) -> User:
        if not orm_model:
            return None
        
        email_vo = Email(orm_model.email)
        return User(
            id=orm_model.id,
            username=orm_model.username,
            email=email_vo,
            first_name=orm_model.first_name,
            last_name=orm_model.last_name,
            hashed_password=orm_model.hashed_password,
            phone_number=orm_model.phone_number,
            role=orm_model.role,
            is_active=orm_model.is_active
        )

    @staticmethod
    def to_orm(domain_model: User) -> UserORM:
        return UserORM(
            id=domain_model.id,
            username=domain_model.username,
            email=domain_model.email.value,
            first_name=domain_model.first_name,
            last_name=domain_model.last_name,
            hashed_password=domain_model.hashed_password,
            phone_number=domain_model.phone_number,
            role=domain_model.role,
            is_active=domain_model.is_active
        )