from app.db.firebase_client import db


async def register_user(username: str, password: str):
    """
    Register a new user in Firestore with hashed password.
    """
