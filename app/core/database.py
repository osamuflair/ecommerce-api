from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from app.core.config import settings

secret = settings.DATABASE_URL

engine = create_engine(secret)

class Base(DeclarativeBase):
    pass

def get_session():
    with Session(engine) as session:
        yield session