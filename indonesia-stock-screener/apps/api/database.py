import os
# 1. Added SQLModel to the imports
from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./indonesia_stocks.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

# 2. Added the missing init_db function
def init_db():
    SQLModel.metadata.create_all(engine)