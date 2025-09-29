from fastapi import FastAPI, APIRouter, HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register():
    return {"message": "Register"}


@router.get("/login")
async def login():
    return {"message": "Login"}
