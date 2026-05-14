from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.modules.core.application.commands.users.register_user import RegisterUserCommand, RegisterUserHandler
from app.modules.core.application.queries.auth.login import LoginQuery, LoginHandler
from app.modules.core.presentation.dependencies import get_register_handler, get_login_handler

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
    handler: RegisterUserHandler = Depends(get_register_handler)
):
    command = RegisterUserCommand(
        email=request.email,
        password=request.password,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        phone_number=request.phone_number
    )
    user_id = handler.execute(command)
    return {"message": "User successfully registered", "user_id": user_id}

@router.post("/login", response_model=TokenResponse)
def login(
    request: AuthLoginRequest,
    handler: LoginHandler = Depends(get_login_handler)
):
    query = LoginQuery(email=request.email, password=request.password)
    token = handler.execute(query)
    return TokenResponse(access_token=token)