from metadata_server.routes.file import SessionLocal
from metadata_server.models import StorageNode
import random, itertools
import requests


_round_robin = None


def get_node_address():
    session = SessionLocal()
    try:
        nodes = session.query(StorageNode).all()
        return [node.address_sn for node in nodes]
    finally:
        session.close()

def get_health_nodes():
    nodes = get_node_address()
    healthy_nodes = []
    for node in nodes:
        try:
            health = requests.get(f"{node}/health", timeout=2)
            if health.status_code == 200 and health.json().get("status") == "ok":
                healthy_nodes.append(node)
        except Exception:
            continue
    if len(healthy_nodes) < 2:
        raise Exception("可用节点不足")
    else:
        return healthy_nodes

def select_nodes_for_chunk(replicas = 2, strategy = "round_robin"):
    nodes = get_health_nodes()
    if strategy == "round_robin":
        global _round_robin
        if _round_robin is None:
            _round_robin = itertools.cycle(nodes)
            return [next(_round_robin) for _ in range(replicas)]
    elif strategy == "random":
        return random.sample(nodes, replicas)
    elif strategy == "least_used":
        useage = {n: get_chunk_count(n) for n in nodes}
        return sorted(useage, key=lambda x: useage[x])[:replicas]
    return nodes[:replicas]

STORAGE_NODES = select_nodes_for_chunk()

current_index = 0



def get_next_node():
    global current_index
    node = STORAGE_NODES[current_index % len(STORAGE_NODES)]
    current_index += 1
    return node



def get_chunk_count(node_url):
    try:
        resp = requests.get(f"{node_url}/chunk_count", timeout=2)
        if resp.status_code == 200:
            return resp.json().get("count", 0)
    except Exception:
        return float('inf')
    return float('inf')

def recover_replicas(file_id: int, desired_replicas: int, metadata_url="http://localhost:8000"):
    resp = requests.get(f"{metadata_url}/file/check_replicas/{file_id}")
    chunks_info = resp.json()
    for chunk_info in chunks_info:
        chunk_index = chunk_info["chunk_index"]
        current_replicas = chunk_info["replicas"]
        if current_replicas < desired_replicas:
            chunk_resp = requests.get(f"{metadata_url}/file/get_chunk_nodes", params={"file_id": file_id, "chunk_index": chunk_index})
            nodes = chunk_resp.json()
            data = None
            for node in nodes:
                try:
                    data = requests.get(f"{node}/get_chunk", params={"file_id": file_id, "chunk_index": chunk_index}).content
                    break
                except:
                    continue
            if data is None:
                print(f"无法恢复文件 {file_id} 的块 {chunk_index}，所有副本均不可用")
                continue
            healthy_nodes = get_health_nodes()
            for node in healthy_nodes:
                if node not in nodes:
                    upload_resp = requests.post(f"{node}/store_chunk", data={"file_id": file_id, "chunk_index": chunk_index}, files={"chunk": (f"{file_id}_{chunk_index}", data)})
                    if upload_resp.status_code == 200:
                        requests.post(f"{metadata_url}/file/register_chunk", params={"file_id": file_id, "chunk_index": chunk_index, "node_address": node})
                        current_replicas += 1
                        print(f"已在节点 {node} 上恢复文件 {file_id} 的块 {chunk_index}")
                    if current_replicas >= desired_replicas:
                        break
            if current_replicas < desired_replicas:
                print(f"无法为文件 {file_id} 的块 {chunk_index} 达到所需的副本数 {desired_replicas}")
