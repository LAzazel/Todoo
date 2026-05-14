from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.modules.core.application.interfaces.auth_services import IPasswordHasher, ITokenService
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.modules.core.domain.errors import InvalidCredentialsError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasslibPasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

class JoseTokenService(ITokenService):
    def generate_token(self, user_id: int, role: str) -> str:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": str(user_id), "role": role, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise InvalidCredentialsError("Invalid or expired token")