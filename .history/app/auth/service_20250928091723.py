# app/auth/service.py
from passlib.context import CryptContext
from app.auth.jwt_handler import create_access_token
from app.auth.schema import CreateUserSchema
from app.db.firebase_client import db
from fastapi import HTTPException
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


# ----------------Create User----------------- #
async def register_user(username: str, password: str) -> dict:
    """
    Registers a new user in Firestore.
    - Hashes the password
    - Checks for existing username
    - Stores created_at timestamp (UTC)
    """
    try:
        users_ref = db.collection("users")

        # Check if user already exists
        query = users_ref.where("username", "==", username).limit(1).get()
        if query:
            logger.warning(f"Attempt to register existing username: {username}")
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the password
        hashed_password = get_password_hash(password)

        # UTC timezone-aware timestamp
        created_at = datetime.now(timezone.utc)

        user_data = {
            "username": username,
            "password": hashed_password,
            "created_at": created_at,  # Stored as Firestore Timestamp
        }

        users_ref.add(user_data)
        logger.info(f"User registered successfully: {username}")

        return {
            "success": True,
            "message": "User registered successfully",
            "data": {"username": username},
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user {username}: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while registering user"
        )


# ----------------Login User----------------- #
async def login_user(username: str, password: str) -> dict:
    """
    Authenticates a user.
    - Verifies username and password
    - Returns success message if authenticated
    - Generates and returns a JWT token
    """
    try:
        users_ref = db.collection("users")

        # Fetch user by username
        query = users_ref.where("username", "==", username).limit(1).get()
        if not query:
            logger.warning(f"Login attempt with non-existent username: {username}")
            raise HTTPException(status_code=400, detail="Invalid username or password")

        user_doc = query[0]
        user_data = user_doc.to_dict()

        # Verify password
        if not verify_password(password, user_data["password"]):
            logger.warning(f"Invalid password attempt for username: {username}")
            raise HTTPException(status_code=400, detail="Invalid username or password")

        logger.info(f"User logged in successfully: {username}")

        # Generate and return JWT token
        access_token = create_access_token(subject=username)
        return {"access_token": access_token}
        # return {
        #     "success": True,
        #     "message": "User logged in successfully",
        #     "data": {"username": username},
        #     "token": access_token,
        # }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user {username}: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while logging in user"
        )
