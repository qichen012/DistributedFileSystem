import os
import requests
from controller.scheduler import get_next_node
from common.utils import log_info, log_error

def split_file(filepath, chunk_size= 1024*1024):
    with open(filepath, "rb") as f:
        index = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield index, chunk
            index += 1

def register_file(file_name, filesize):
    url = "http://localhost:8000/file/register_file"
    data = {"file_name":file_name,"filesize":filesize}
    resp = requests.post(url, json=data)
    return resp.json()["file_id"]

def register_chunk(file_id, chunk_index, node_url):
    url = "http://localhost:8000/file/register_chunk"
    params = {
        "file_id": file_id,
        "chunk_index": chunk_index,
        "node_address": node_url
    }
    resp = requests.post(url, params= params)
    resp.raise_for_status()

def upload_chunk(file_id:int, chunk_index:int, chunk_data:bytes, node_url:str):
    files = {
        "chunk":(f"{file_id}_{chunk_index}",chunk_data)
    }
    data = {
        "file_id": file_id,
        "chunk_index": chunk_index
    }
    resp = requests.post(f"{node_url}/store_chunk",data= data,files=files)
    return resp.json()

def upload_file(filepath):
    filesize = os.path.getsize(filepath)
    file_name = os.path.basename(filepath)
    file_id = register_file(file_name, filesize)
    for index, chunk in split_file(filepath):
        node_url = get_next_node()
        result = upload_chunk(file_id, index,chunk,node_url)
        print(f"Uploading chunk {index} of file id {file_id}",result)
        register_chunk(file_id, index, node_url)

def download_file(file_id: int,save_path:str):
    resp = requests.get("http://localhost:8000/file/get_chunks", params={"file_id": file_id})
    chunks_info = resp.json()
    chunks_info.sort(key= lambda x: x["chunk_index"])

    with open(save_path, "wb") as f:
        for chunk in chunks_info:
            resp = requests.get(
                f"{chunk['node_address']}/get_chunk/",
                params = {"file_id": file_id, "chunk_index": chunk["chunk_index"]}
            )
            resp.raise_for_status()
            f.write(resp.content)
    print(f"File {file_id} download and saved as {save_path}")

def upload_chunk_with_retry(file_id, chunk_index, chunk_data, node_url, retries = 1):
    for attempt in range(retries + 1):
        try:
            result = upload_chunk(file_id, chunk_index, chunk_data, node_url)
            log_info(f"Uploaded chunk {chunk_index} to {node_url}")
            return result
        except Exception as e:
            log_error(f"Attempt {attempt +1} failed: {e}")
            if attempt == retries:
                raise