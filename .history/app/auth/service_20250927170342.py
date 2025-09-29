from app.auth.schema import CreateUserSchema
from app.db.firebase_client import db


async def register_user(
    username: str, password: str, create_user_schema: CreateUserSchema
):
    """
    Register a new user in Firestore with hashed password.
    """
