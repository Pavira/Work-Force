from app.auth.schema import CreateUserSchema
from app.auth.service import register_user, login_user
from fastapi import FastAPI, APIRouter, HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(user: CreateUserSchema):
    result = await register_user(user.username, user.password)
    return result


@router.post("/login")
async def login(data: CreateUserSchema):
    result = await login_user(data.username, data.password)
    return result
