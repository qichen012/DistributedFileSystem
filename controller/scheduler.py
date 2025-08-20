from metadata_server.routes.file import SessionLocal
from metadata_server.models import StorageNode
import requests

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
    return healthy_nodes

STORAGE_NODES = get_health_nodes()

current_index = 0

def get_next_node():
    global current_index
    node = STORAGE_NODES[current_index % len(STORAGE_NODES)]
    current_index += 1
    return node