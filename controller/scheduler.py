from metadata_server.routes.file import SessionLocal
from metadata_server.models import StorageNode

def get_node_address():
    session = SessionLocal()
    try:
        nodes = session.query(StorageNode).all()
        return [node.address_sn for node in nodes]
    finally:
        session.close()
STORAGE_NODES = get_node_address()

current_index = 0

def get_next_node():
    global current_index
    node = STORAGE_NODES[current_index % len(STORAGE_NODES)]
    current_index += 1
    return node