from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

class ContentConfig(Base):
    """Ana konfigürasyon tablosu - her şeyi tek tabloda tutuyoruz"""
    __tablename__ = "content_configs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)  # "blog", "emlak", "fikra"
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # JSON olarak saklanacak veriler
    prompts = Column(JSON, nullable=False)  # [{"step": 1, "text": "...", "ai_settings": {...}}]

# Database bağlantısı
DATABASE_URL = "sqlite:///./content_assistant_v2.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
