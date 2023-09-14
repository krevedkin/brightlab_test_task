import uvicorn
from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.task.router import router as task_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
