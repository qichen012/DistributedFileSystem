import os
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()
STORAGE_DIR = "./data"
os.makedirs(STORAGE_DIR, exist_ok= True)

@app.post("/store_chunk/")
async def store_chunk(file_id: int = Form(...), chunk_index: int= Form(...), chunk: UploadFile= File(...)):
    contents = await chunk.read()
    file_path = os.path.join(STORAGE_DIR, f"{file_id}_chunk_{chunk_index}")
    with open(file_path, "wb") as f:
        f.write(contents)
    return {"status":"success", "file_id":file_id, "chunk_index":chunk_index}