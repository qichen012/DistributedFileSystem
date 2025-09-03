import os, requests,sys
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
import atexit

app = FastAPI()
STORAGE_DIR = "./data"
os.makedirs(STORAGE_DIR, exist_ok= True)

@app.get("/health")
def health_check():
    return{"status" : "ok"}

@app.post("/store_chunk")
async def store_chunk(file_id: int = Form(...), chunk_index: int= Form(...), chunk: UploadFile= File(...)):
    contents = await chunk.read()
    file_path = os.path.join(STORAGE_DIR, f"{file_id}_chunk_{chunk_index}")
    with open(file_path, "wb") as f:
        f.write(contents)
    return {"status":"success", "file_id":file_id, "chunk_index":chunk_index}

@app.get("/get_chunk/")
async def get_chunk(file_id: int ,chunk_index: int):
    """
    返回指定 file_id 和 chunk_index 的文件块内容
    """
    file_path = os.path.join(STORAGE_DIR, f"{file_id}_chunk_{chunk_index}")
    return FileResponse(file_path)

def register_node(port):
    node_address = f"http://localhost:{port}"
    try:
        resp = requests.post(
            "http://localhost:8000/node/register_storage_node",
            params = {"address": node_address}
        )
        print(f"Registered node {node_address}: {resp.json()}")
    except Exception as e:
        print(f"Failed to register node : {e}")

def unregister_node(port):
    node_address = f"http://localhost:{port}"
    try:
        resp = requests.post(
            "http://localhost:8000/node/unregister_storage_node",
            params = {"address": node_address}
        )
        print(f"Unregistered node {node_address}: {resp.json()}")
    except Exception as e:
        print(f"Failed to unregister node: {e}")

@app.delete("/delete_chunk")
async def delete_chunk(file_id : int, chunk_index: int):
    file_path = os.path.join(STORAGE_DIR, f"{file_id}_chunk_{chunk_index}")
    if os.path.exists(file_path):
        os.remove(file_path)
    return {"status": "deleted", "file_id": file_id, "chunk_index": chunk_index}

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else "9001"
    register_node(port)
    atexit.register(unregister_node, port)
    import uvicorn
    uvicorn.run("storage_nodes.node:app", host= "0.0.0.0", port=int(port), reload= True)