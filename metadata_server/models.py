from sqlalchemy import Column, Integer,String,BigInteger,DateTime,ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class File(Base):
    __tablename__="files"
    id = Column(Integer,primary_key=True,autoincrement=True)
    file_name= Column(String(255),nullable=False)
    filesize = Column(BigInteger, nullable=False)
    upload_time = Column(DateTime,default= datetime.utcnow)

class Chunk(Base):
    __tablename__= "chunks"
    id = Column(Integer,primary_key=True,autoincrement=True)
    file_id= Column(Integer,ForeignKey("files.id"),nullable= False)
    chunk_index= Column(Integer, nullable=False)
    check_sum = Column(String(64))
    node_address = Column(String(255))

class StorageNode(Base):
    __tablename__ = "storage_nodes"
    id = Column(Integer,primary_key=True,autoincrement=True)
    address_sn = Column(String(255), nullable= False)
    last_heartbeat = Column(DateTime)