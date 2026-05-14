from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.modules.core.domain import errors

def domain_error_exception_handler(request: Request, exc: errors.DomainError):
    status_code = status.HTTP_400_BAD_REQUEST

    if isinstance(exc, errors.UserNotFoundError) or isinstance(exc, errors.TodoNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, errors.UserAlreadyExistsError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, errors.InvalidCredentialsError):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, errors.UnauthorizedAdminAccessError):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, errors.InvalidEmailError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )