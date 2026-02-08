from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv # Import load_dotenv

load_dotenv() # Load environment variables from .env

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # Fallback or raise an error if DATABASE_URL is not set
    # For now, we'll keep the SQLite fallback as a development convenience
    print("Warning: DATABASE_URL not found in environment. Falling back to sqlite:///./todo.db")
    DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    """Provides a database session for FastAPI routes."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Creates all database tables."""
    # Hum models ko yahan import kar rahe hain taake koi confusion na ho
    from models import Task, User
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")