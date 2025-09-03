from fastapi import FastAPI, APIRouter,HTTPException,Response
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from metadata_server.db import engine
from metadata_server.models import File,Chunk
import os
from typing import Generator
from fastapi import Depends
import requests

SessionLocal = sessionmaker(bind= engine)

router = APIRouter()

class FileRegisterRequest(BaseModel):
    file_name: str
    filesize: int

class FileDownloadRequest(BaseModel):
    file_id: int

STORAGE_DIR = "./data"

def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话的依赖项
    使用yield确保会话在使用后正确关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@router.post("/register_chunk")
async def resgister_chunk(file_id: int,chunk_index: int, node_address: str):
    session = SessionLocal()
    chunk = Chunk(file_id= file_id,chunk_index=chunk_index,node_address= node_address)
    session.add(chunk)
    session.commit()
    session.close()
    return {"status": "ok"}

@router.get("/get_chunks")
async def get_chunks(file_id: int):
    session = SessionLocal()
    chunks = session.query(Chunk).filter(Chunk.file_id==file_id).all()
    session.close()
    return[
        {"chunk_index": c.chunk_index, "node_address": c.node_address}
        for c in chunks
    ]

@router.post("/download")
async def download_file(req: FileDownloadRequest):
    session = SessionLocal()
    file_record = session.query(File).filter(File.id == req.file_id).first()
    session.close()

    if not file_record:
        raise HTTPException(status_code= 404, detail= "文件不存在")
    
    file_path = os.path.join(STORAGE_DIR, file_record.file_name)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail= "文件实际内容不存在")
    
    with open(file_path, "rb") as f:
        content = f.read()

    return Response(
        content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{file_record.file_name}"'
        }
    )

@router.delete("/delete_file/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    chunks = db.query(Chunk).filter(Chunk.file_id == file_id).all()
    for chunk in chunks:
        try:
            requests.delete(f"{chunk.node_address}/delete_chunk",
                            params = {"file_id": file_id, "chunk_index": chunk.chunk_index})
        except:
            pass
    db.query(Chunk).filter(Chunk.file_id == file_id).delete()
    db.query(File).filter(File.id == file_id).delete()
    db.commit()
    return {"status": "deleted", "file_id": file_id}