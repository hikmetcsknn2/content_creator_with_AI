"""
API routes for content generation and configuration management
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from .database import get_db
from .models import ContentConfig
from .schemas import (
    ContentGenerationRequest, ContentGenerationResponse,
    ContentConfigCreate, ContentConfigResponse, ContentTypeResponse
)
from .ai_service import generate_ai_content
from .services import ContentService

router = APIRouter()

@router.post("/generate-content", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest, db: Session = Depends(get_db)):
    """Ana içerik üretim endpoint'i"""
    print(f"🔍 Generate request: content_type={request.content_type}")
    print(f"📊 Dynamic data: {request.dynamic_data}")
    print(f"⚙️ Custom AI configs: {list(request.custom_ai_configs.keys())}")
    print(f"📝 Custom prompts: {list(request.custom_prompts.keys())}")
    
    try:
        # Konfigürasyonu DB'den al
        config = db.query(ContentConfig).filter(ContentConfig.name == request.content_type).first()
        if not config:
            raise HTTPException(status_code=404, detail="Konfigürasyon bulunamadı")
        
        print(f"📋 Config found: {config.name}, prompts: {len(config.prompts)}")
        
        # Prompt'ları işle
        step_outputs = []
        step_details = []
        
        for i, prompt_data in enumerate(config.prompts):
            step = prompt_data["step"]
            original_prompt = prompt_data["text"]
            
            # Custom prompt varsa onu kullan
            custom_prompt_key = f"step_{step}"
            if custom_prompt_key in request.custom_prompts:
                processed_prompt = request.custom_prompts[custom_prompt_key]
                print(f"📝 Step {step}: Using custom prompt")
            else:
                processed_prompt = original_prompt
                print(f"📝 Step {step}: Using DB prompt")
            
            # Dinamik verileri ekle
            if request.dynamic_data:
                dynamic_str = ", ".join([f"{k}: {v}" for k, v in request.dynamic_data.items()])
                processed_prompt = f"{processed_prompt}\n\nDinamik veriler: {dynamic_str}"
            
            # Önceki adımın sonucunu ekle
            if step_outputs:
                processed_prompt = f"{processed_prompt}\n\nÖnceki adımın sonucu:\n{step_outputs[-1]}"
            
            # AI ayarlarını belirle
            custom_config_key = f"step_{step}"
            if custom_config_key in request.custom_ai_configs:
                ai_settings = request.custom_ai_configs[custom_config_key]
                print(f"⚙️ Step {step}: Using custom AI config")
            else:
                ai_settings = prompt_data.get("ai_settings", {
                    "model": "gemini-2.5-flash",
                    "temperature": 0.7,
                    "top_p": 0.7,
                    "response_mime_type": "text/plain",
                    "max_tokens": 8000
                })
                print(f"⚙️ Step {step}: Using DB AI config")
            
            # Minimum max_tokens kontrolü
            if ai_settings.get("max_tokens", 0) < 8000:
                ai_settings["max_tokens"] = 8000
                print(f"🔧 Step {step}: Adjusted max_tokens to 8000")
            
            print(f"🤖 Step {step} AI settings: {ai_settings}")
            
            # AI ile içerik üret
            output = generate_ai_content(processed_prompt, ai_settings)
            step_outputs.append(output)
            
            # Step detaylarını kaydet
            step_details.append({
                "step": step,
                "original_prompt": original_prompt,
                "processed_prompt": processed_prompt,
                "ai_settings": ai_settings,
                "output": output
            })
            
            print(f"✅ Step {step} completed")
        
        # Final içerik (son adımın çıktısı)
        final_content = step_outputs[-1] if step_outputs else "İçerik üretilemedi"
        
        # Metadata
        metadata = {
            "total_steps": len(config.prompts),
            "dynamic_data_used": request.dynamic_data,
            "step_details": step_details,
            "original_prompts": config.prompts
        }
        
        return ContentGenerationResponse(
            content=final_content,
            prompt_outputs=step_outputs,
            content_type=request.content_type,
            metadata=metadata
        )
        
    except Exception as e:
        print(f"❌ Generate content error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/content-types", response_model=List[ContentTypeResponse])
async def list_content_types(db: Session = Depends(get_db)):
    """Tüm konfigürasyonları listele"""
    configs = db.query(ContentConfig).all()
    return [
        ContentTypeResponse(
            id=config.id,
            name=config.name,
            description=config.description,
            created_at=config.created_at.isoformat()
        )
        for config in configs
    ]

@router.get("/prompts/{content_type}")
async def get_prompts(content_type: str, db: Session = Depends(get_db)):
    """Belirli bir konfigürasyonun prompt'larını getir"""
    config = db.query(ContentConfig).filter(ContentConfig.name == content_type).first()
    if not config:
        raise HTTPException(status_code=404, detail="Konfigürasyon bulunamadı")
    
    processed_prompts = config.prompts.copy()
    
    return {
        "content_type": content_type,
        "prompts": processed_prompts
    }

@router.post("/content-types", response_model=ContentConfigResponse)
async def create_content_type(request: ContentConfigCreate, db: Session = Depends(get_db)):
    """Yeni konfigürasyon oluştur"""
    print(f"🔍 Create request received: {request}")
    
    try:
        # Aynı isimde konfigürasyon var mı kontrol et
        existing = db.query(ContentConfig).filter(ContentConfig.name == request.content_type).first()
        if existing:
            raise HTTPException(status_code=400, detail="Bu isimde konfigürasyon zaten var")
        
        # Yeni konfigürasyon oluştur
        print(f"📝 Creating config: name={request.content_type}, prompts={len(request.prompts)}")
        new_config = ContentConfig(
            name=request.content_type,
            description=request.description,
            prompts=request.prompts
        )
        
        db.add(new_config)
        db.commit()
        db.refresh(new_config)
        
        return ContentConfigResponse(
            id=new_config.id,
            name=new_config.name,
            description=new_config.description,
            prompts=new_config.prompts,
            created_at=new_config.created_at.isoformat()
        )
        
    except Exception as e:
        db.rollback()
        print(f"❌ Create error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/content-types/{content_type}", response_model=ContentConfigResponse)
async def update_content_type(content_type: str, request: ContentConfigCreate, db: Session = Depends(get_db)):
    """Mevcut konfigürasyonu güncelle"""
    try:
        config = db.query(ContentConfig).filter(ContentConfig.name == content_type).first()
        if not config:
            raise HTTPException(status_code=404, detail="Konfigürasyon bulunamadı")
        
        # Güncelle
        config.description = request.description
        config.prompts = request.prompts
        
        db.commit()
        db.refresh(config)
        
        return ContentConfigResponse(
            id=config.id,
            name=config.name,
            description=config.description,
            prompts=config.prompts,
            created_at=config.created_at.isoformat()
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
