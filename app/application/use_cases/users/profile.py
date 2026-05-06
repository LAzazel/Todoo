from app.application.dto.user_dto import UserResponseDTO
from app.domain.repositories.user_repo import IUserRepository
from app.application.interfaces.auth_services import IPasswordHasher
from app.domain.errors import UserNotFoundError

class GetUserProfileUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> UserResponseDTO:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        return UserResponseDTO(
            id=user.id,
            email=user.email.value,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            role=user.role
        )

class ChangePasswordUseCase:
    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def execute(self, user_id: int, new_password: str) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        new_hashed = self.password_hasher.hash(new_password)
        
        user.change_password(new_hashed)
        
        self.user_repo.update(user)

class ChangePhoneNumberUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int, new_phone: str) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        user.update_phone_number(new_phone)
        
        self.user_repo.update(user)