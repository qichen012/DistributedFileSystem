from fastapi import FastAPI
from .routes.file import router as file_router
from .routes.node import router as node_router

app = FastAPI()

app.include_router(file_router, prefix="/file")
app.include_router(node_router, prefix="/node")

@app.get("/ping")
def ping():
    return{"message": "tong"}

@app.get("/hello")
def hello():
    return{"hello": "this is fastapi"}