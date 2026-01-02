from sqlmodel import SQLModel
from ..database.database import engine
from ..models.user import User

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)