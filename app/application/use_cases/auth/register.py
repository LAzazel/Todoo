from app.application.dto.user_dto import RegisterUserDTO, UserResponseDTO
from app.domain.factories.user_factory import UserFactory
from app.domain.repositories.user_repo import IUserRepository
from app.application.interfaces.auth_services import IPasswordHasher

class RegisterUserUseCase:
    def __init__(
        self, 
        user_repo: IUserRepository, 
        user_factory: UserFactory, 
        password_hasher: IPasswordHasher
    ):
        self.user_repo = user_repo
        self.user_factory = user_factory
        self.password_hasher = password_hasher

    def execute(self, dto: RegisterUserDTO) -> UserResponseDTO:
        hashed_password = self.password_hasher.hash(dto.password)
        
        user = self.user_factory.create_user(
            username=dto.username,
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            hashed_password=hashed_password,
            phone_number=dto.phone_number
        )
        
        self.user_repo.add(user)
        
        return UserResponseDTO(
            id=user.id,
            email=user.email.value,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            role=user.role
        )