from typing import Annotated
from app.auth.schema import CreateUserSchema
from app.auth.service import register_user, login_user
from fastapi import APIRouter, Depends
from app.auth.model import Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/register")
async def register(user: CreateUserSchema):
    result = await register_user(user.username, user.password)
    return result


# @router.post("/token")
# async def login(data: CreateUserSchema):
#     result = await login_user(data.username, data.password)
#     return result


@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    result = await login_user(form_data.username, form_data.password)
    return {"access_token": result["access_token"], "token_type": "bearer"}
