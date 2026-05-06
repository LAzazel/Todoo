from app.application.dto.user_dto import LoginUserDTO
from app.domain.errors import InvalidCredentialsError
from app.domain.repositories.user_repo import IUserRepository
from app.application.interfaces.auth_services import IPasswordHasher, ITokenService
from app.domain.value_objects.email import Email

class LoginUserUseCase:
    def __init__(
        self, 
        user_repo: IUserRepository, 
        password_hasher: IPasswordHasher,
        token_service: ITokenService
    ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, dto: LoginUserDTO) -> str:
        email_vo = Email(dto.email)
        user = self.user_repo.get_by_email(email_vo)
        
        if not user:
            raise InvalidCredentialsError("Invalid email or password")
            
        if not self.password_hasher.verify(dto.password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")

        return self.token_service.generate_token(user_id=user.id, role=user.role)