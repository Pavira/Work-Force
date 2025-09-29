from pydantic import BaseModel, Field


class CreateUserModel(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
