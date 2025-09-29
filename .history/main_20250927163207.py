from fastapi import FastAPI
from app.auth.route import router as auth_router
import uvicorn

app = FastAPI()

# Api routes
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
