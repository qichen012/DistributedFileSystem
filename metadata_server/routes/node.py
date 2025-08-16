from fastapi import APIRouter
from metadata_server.routes.file import SessionLocal
from metadata_server.models import StorageNode
from datetime import datetime

router = APIRouter()

@router.post("/register_storage_node")
async def register_node(address: str):
    session = SessionLocal()
    try:
        node = session.query(StorageNode).filter(StorageNode.address_sn == address).first()
        if node:
            node.last_heartbeat = datetime.utcnow()
        else:
            node = StorageNode(address_sn = address, last_heartbeat = datetime.utcnow())
            session.add(node)
        session.commit()
        return {"status": "ok","node_id":node.id}
    finally:
        session.close()