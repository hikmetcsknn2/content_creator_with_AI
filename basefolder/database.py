"""
Database utilities and session management
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base
from .config import DATABASE_URL

# Database engine oluştur
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Database session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """Direct database session (for non-FastAPI use)"""
    return SessionLocal()
