from sqlalchemy import create_engine, text
from .models import Base

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/test0")
Base.metadata.create_all(engine)

with engine.connect() as conn:
    result = conn.execute(text("SELECT VERSION()"))
    for row in result:
        print("MySQL version:", row[0])