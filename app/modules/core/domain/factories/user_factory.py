from app.modules.core.domain.models.user import User
from app.modules.core.domain.value_objects.email import Email
from app.modules.core.domain.repositories.user_repo import IUserRepository
from app.modules.core.domain.errors import UserAlreadyExistsError


class UserFactory:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def create_user(
        self, 
        username: str, 
        email: str, 
        first_name: str, 
        last_name: str, 
        hashed_password: str, 
        phone_number: str
    ) -> User:
        email_vo = Email(email)

        existing_user = self.user_repo.get_by_email(email_vo)
        if existing_user is not None:
            raise UserAlreadyExistsError(f"User with email {email} already exists.")


        return User(
            id=None, 
            email=email_vo, 
            username=username,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            phone_number=phone_number
        )