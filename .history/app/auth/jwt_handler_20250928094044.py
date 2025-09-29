# app/utils/jwt_handler.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
import logging
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv(
    "JWT_SECRET", "super-secret-key"
)  # use env variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """
    Generate a JWT token with expiration.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": subject, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"JWT generated for user: {subject}")
    return token


def get_current_user(token: str) -> str:
    """
    Decode the JWT token to get the current user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError("Token does not contain subject")
        return username
    except JWTError as e:
        logger.warning(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
