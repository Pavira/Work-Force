from app.auth.schema import CreateUserSchema
from fastapi import FastAPI, APIRouter, HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(user: CreateUserSchema):
    result = await register_user(user.username, user.password)
    return result


@router.get("/login")
async def login():
    return {"message": "Login"}
