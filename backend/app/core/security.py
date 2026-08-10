from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Turns a plain-text password into a secure, irreversible hash.
    Use this whenever saving a new user's password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks whether a plain-text password matches a stored hash.
    Use this during login — never compare plain passwords directly.
    """
    return pwd_context.verify(plain_password, hashed_password)
from datetime import datetime, timedelta

from jose import jwt

from app.core.config import settings


def create_access_token(username: str, role: str) -> str:
    """
    Creates a signed JWT token for a logged-in user.
    The token encodes the username, role, and an expiration time.
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "role": role, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Decodes and validates a JWT token from the request's Authorization
    header. Raises 401 if missing, invalid, or expired.
    Returns a dict with the username and role.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None:
            raise credentials_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Additional check that only allows admin-role users through.
    Use this as a dependency on routes that should be admin-only.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user