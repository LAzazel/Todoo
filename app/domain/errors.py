class DomainError(Exception):
    pass

class ValidationError(DomainError):
    pass

class UserAlreadyExistsError(DomainError):
    pass

class InvalidEmailError(DomainError):
    pass