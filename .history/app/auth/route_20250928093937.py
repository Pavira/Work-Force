from typing import Annotated
from app.auth.jwt_handler import get_current_user
from app.auth.schema import CreateUserSchema
from app.auth.service import register_user, login_user
from fastapi import APIRouter, Depends
from app.auth.model import Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
user_dependency = Annotated[str, Depends(get_current_user)]


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


@router.get("/")
async def user(current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"username": current_user}
