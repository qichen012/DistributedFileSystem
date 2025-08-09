from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from metadata_server.db import engine
from metadata_server.models import File

SessionLocal = sessionmaker(bind= engine)

router = APIRouter()

class FileRegisterRequest(BaseModel):
    file_name: str
    filesize: int


@router.post("/register_file")
async def register_file(req: FileRegisterRequest):
    session = SessionLocal()
    new_file = File(file_name= req.file_name,filesize= req.filesize)
    session.add(new_file)
    session.commit()
    session.refresh(new_file)
    session.close()
    # TODO: 写入文件元数据
    return {"message": "File registered", "file_id": new_file.id}