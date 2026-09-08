from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine ,text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True) 
# echo = true prints
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() # Without Base, SQLAlchemy cannot understand which classes are tables
    
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()