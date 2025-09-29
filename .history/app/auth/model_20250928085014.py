from pydantic import BaseModel, Field


class CreateUserModel(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str = Field(..., alias="token")
    token_type: str = "bearer"
