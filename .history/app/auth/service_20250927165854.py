from app.auth.model import CreateUserModel
from app.db.firebase_client import db


async def register_user(
    username: str, password: str, create_user_model: CreateUserModel
):
    """
    Register a new user in Firestore with hashed password.
    """
    user_ref = db.collection("users")

    # Check if user already exists
    existing_user = user_ref.document().get()
    if existing_user.exists:
        raise ValueError("User already exists")

    user_doc = user_ref.set(
        {CreateUserModel.username: username, CreateUserModel.password: password}
    )
    return user_doc
