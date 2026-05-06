class DomainError(Exception):
    pass

class ValidationError(DomainError):
    pass

class UserAlreadyExistsError(DomainError):
    pass

class InvalidEmailError(DomainError):
    pass

class InvalidCredentialsError(DomainError):
    pass

class TodoNotFoundError(DomainError):
    pass

class UserNotFoundError(DomainError):
    pass

class UnauthorizedAdminAccessError(DomainError):
    pass