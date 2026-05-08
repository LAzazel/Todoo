from dataclasses import dataclass
from app.domain.repositories.user_repo import IUserRepository
from app.application.interfaces.auth_services import IPasswordHasher, ITokenService
from app.domain.value_objects.email import Email
from app.domain.errors import InvalidCredentialsError

@dataclass(frozen=True)
class LoginQuery:
    email: str
    password: str

class LoginHandler:
    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher, token_service: ITokenService):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, query: LoginQuery) -> str:
        user = self.user_repo.get_by_email(Email(query.email))
        if not user or not self.password_hasher.verify(query.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
        
        return self.token_service.generate_token(user.id, user.role)