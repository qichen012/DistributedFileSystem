import os
import requests

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

def upload_file(filepath):
    filesize = os.path.getsize(filepath)
    file_name = os.path.basename(filepath)
    file_id = register_file(file_name, filesize)
    for index, chunk in split_file(filepath):
        #TODO:上传chunk到存储节点
        print(f"Uploading chunk {index} of file id{file_id}")