# app/utils/jwt_handler.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv(
    "JWT_SECRET", "super-secret-key"
)  # use env variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour


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


def verify_access_token(token: str) -> dict | None:
    """
    Decode and validate JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        return None
