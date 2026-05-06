from app.domain.models.user import User
from app.domain.value_objects.email import Email
from app.domain.repositories.user_repo import IUserRepository
from app.domain.errors import UserAlreadyExistsError


class UserFactory:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def create_user(self, email_str: str, password_hash: str) -> User:
        email_vo = Email(email_str)

        existing_user = self.user_repo.get_by_email(email_vo)
        if existing_user is not None:
            raise UserAlreadyExistsError(f"Користувач з email {email_str} вже існує.")


        return User(
            id=None, 
            email=email_vo, 
            password_hash=password_hash
        )