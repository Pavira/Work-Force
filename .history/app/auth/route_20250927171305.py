from app.auth.schema import CreateUserSchema
from app.auth.service import register_user
from fastapi import FastAPI, APIRouter, HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(user: CreateUserSchema):
    result = await register_user(user.username, user.password)
    return result
