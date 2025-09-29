from fastapi import FastAPI, APIRouter, HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.get("/login")
async def login():
    return {"message": "Login"}
