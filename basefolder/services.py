"""
Business logic services
"""
from typing import List, Dict, Any, Optional
from .models import ContentConfig
from .database import get_db_session

class ContentService:
    """Content configuration service"""
    
    @staticmethod
    def get_all_configs() -> List[ContentConfig]:
        """Tüm konfigürasyonları getir"""
        db = get_db_session()
        try:
            return db.query(ContentConfig).all()
        finally:
            db.close()
    
    @staticmethod
    def get_config_by_name(name: str) -> Optional[ContentConfig]:
        """İsimle konfigürasyon getir"""
        db = get_db_session()
        try:
            return db.query(ContentConfig).filter(ContentConfig.name == name).first()
        finally:
            db.close()
    
    @staticmethod
    def create_config(name: str, description: str, prompts: List[Dict[str, Any]]) -> ContentConfig:
        """Yeni konfigürasyon oluştur"""
        db = get_db_session()
        try:
            new_config = ContentConfig(
                name=name,
                description=description,
                prompts=prompts
            )
            db.add(new_config)
            db.commit()
            db.refresh(new_config)
            return new_config
        finally:
            db.close()
    
    @staticmethod
    def update_config(name: str, description: str, prompts: List[Dict[str, Any]]) -> Optional[ContentConfig]:
        """Konfigürasyon güncelle"""
        db = get_db_session()
        try:
            config = db.query(ContentConfig).filter(ContentConfig.name == name).first()
            if config:
                config.description = description
                config.prompts = prompts
                db.commit()
                db.refresh(config)
            return config
        finally:
            db.close()
    
    @staticmethod
    def delete_config(name: str) -> bool:
        """Konfigürasyon sil"""
        db = get_db_session()
        try:
            config = db.query(ContentConfig).filter(ContentConfig.name == name).first()
            if config:
                db.delete(config)
                db.commit()
                return True
            return False
        finally:
            db.close()
