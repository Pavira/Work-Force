from fastapi import FastAPI
from app.auth.controller import router as auth_router

app = FastAPI()

# Api routes
app.include_router(auth_router)
