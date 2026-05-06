from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr

from app.application.dto.user_dto import RegisterUserDTO, LoginUserDTO
from app.application.use_cases.auth.register import RegisterUserUseCase
from app.application.use_cases.auth.login import LoginUserUseCase
from app.presentation.dependencies import get_register_use_case, get_login_use_case

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class AuthRegisterRequest(BaseModel):
    email: str
    password: str
    username: str
    first_name: str
    last_name: str
    phone_number: str

class AuthLoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request: AuthRegisterRequest,
    use_case: RegisterUserUseCase = Depends(get_register_use_case)
):
    dto = RegisterUserDTO(
        email=request.email, 
        password=request.password,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        phone_number=request.phone_number
    )
    user_dto = use_case.execute(dto)
    return {"message": "User successfully registered", "user_id": user_dto.id}

@router.post("/login", response_model=TokenResponse)
def login(
    request: AuthLoginRequest,
    use_case: LoginUserUseCase = Depends(get_login_use_case)
):
    dto = LoginUserDTO(email=request.email, password=request.password)
    token = use_case.execute(dto)
    return TokenResponse(access_token=token)