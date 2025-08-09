from fastapi import FastAPI
from .routes.file import router as file_router

app = FastAPI()

app.include_router(file_router, prefix="/file")

@app.get("/ping")
def ping():
    return{"message": "tong"}

@app.get("/hello")
def hello():
    return{"hello": "this is fastapi"}