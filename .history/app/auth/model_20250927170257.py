from pydantic import BaseModel, Field


class CreateUserModel(BaseModel):
    username: str
    password: str
