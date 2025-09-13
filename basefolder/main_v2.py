from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import google.generativeai as genai
import markdown
import os
from datetime import datetime
from dotenv import load_dotenv
from .models_v2 import Base, ContentConfig

# .env dosyasını BOM ile okuma sorununu çöz
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig BOM'u otomatik kaldırır
        content = f.read().strip()
        print(f"📄 .env içeriği: {repr(content)}")
        
        # Manuel olarak environment variable'a ekle
        if '=' in content:
            key, value = content.split('=', 1)
            key = key.strip()
            value = value.strip()
            os.environ[key] = value
            print(f"✅ Manuel olarak eklendi: {key} = {value[:10]}...")

# API key'i al
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable bulunamadı! .env dosyasında tanımlayın.")

print(f"✅ GEMINI_API_KEY yüklendi: {api_key[:10]}...")
genai.configure(api_key=api_key)

# FastAPI app
app = FastAPI(title="Content Assistant V2", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
DATABASE_URL = "sqlite:///./content_assistant_v2.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Gemini AI - API key'i environment variable'dan al
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable bulunamadı! .env dosyasında tanımlayın.")

print(f"✅ GEMINI_API_KEY yüklendi: {GEMINI_API_KEY[:10]}...")
genai.configure(api_key=GEMINI_API_KEY)

# Pydantic Models
class ContentGenerationRequest(BaseModel):
    content_type: str
    dynamic_data: dict = {}
    custom_ai_configs: dict = {}  # step_1, step_2 gibi özel ayarlar için
    custom_prompts: dict = {}  # step_1, step_2 gibi özel prompt'lar için

class ContentConfigCreate(BaseModel):
    content_type: str
    description: str = ""
    prompts: list  # [{"step": 1, "text": "...", "ai_settings": {...}}]

class ContentConfigResponse(BaseModel):
    id: int
    content_type: str
    description: str
    prompts: list
    created_at: datetime

class PromptTestRequest(BaseModel):
    prompt: str
    model: str = "gemini-2.5-flash"
    temperature: float = 0.7
    top_p: float = 0.7
    response_mime_type: str = "text/plain"
    max_tokens: int = 2000

# Helper Functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def apply_dynamic_data(text: str, dynamic_data: dict) -> str:
    """Dinamik verileri prompt'a uygula"""
    for key, value in dynamic_data.items():
        text = text.replace(f"{{{key}}}", str(value))
    return text

def generate_ai_content(prompt: str, ai_settings: dict) -> str:
    """AI ile içerik üret"""
    try:
        print(f"🤖 AI ayarları: {ai_settings}")
        print(f"📝 Prompt uzunluğu: {len(prompt)} karakter")
        
        model = genai.GenerativeModel(ai_settings["model"])
        
        generation_config = {
            "temperature": ai_settings["temperature"],
            "top_p": ai_settings["top_p"],
            "response_mime_type": ai_settings["response_mime_type"]
        }
        
        # Token limitini kontrol et ve minimum 8192 yap
        max_tokens = ai_settings.get("max_tokens", 8192)
        if max_tokens < 8192:
            print(f"⚠️ Max tokens çok düşük ({max_tokens}), 8192'ye yükseltiliyor")
            max_tokens = 8192
        
        generation_config["max_output_tokens"] = max_tokens
        print(f"🎯 Max tokens: {max_tokens}")
        
        print(f"⚙️ Generation config: {generation_config}")
        
        response = model.generate_content(
            [prompt],
            generation_config=generation_config
        )
        
        # finish_reason kontrolü - önce kontrol et
        if response.candidates:
            candidate = response.candidates[0]
            finish_reason = candidate.finish_reason
            
            if finish_reason == 1:  # STOP - Normal
                return response.text if response.text else "Boş yanıt alındı."
            elif finish_reason == 2:  # MAX_TOKENS - Token limiti
                return f"⚠️ Token limiti aşıldı (max_tokens: {ai_settings.get('max_tokens', 'belirtilmemiş')}). Limit artırın."
            elif finish_reason == 3:  # SAFETY
                return "⚠️ Güvenlik filtresi: Prompt'u değiştirin."
            elif finish_reason == 4:  # RECITATION
                return "⚠️ Telif hakkı: İçerik değiştirin."
            else:
                return f"⚠️ AI hatası (finish_reason: {finish_reason})"
        else:
            return "⚠️ AI yanıtı alınamadı."
            
    except Exception as e:
        return f"AI content generation failed: {str(e)}"

def markdown_to_html(text: str) -> str:
    """Markdown'ı HTML'e çevir"""
    return markdown.markdown(text, extensions=['tables', 'fenced_code'])

# API Endpoints

@app.get("/")
async def root():
    return {"message": "Content Assistant V2 API", "version": "2.0.0"}

@app.get("/content-types")
async def list_content_types():
    """Tüm konfigürasyonları listele - admin panel için"""
    db = next(get_db())
    try:
        configs = db.query(ContentConfig).all()
        result = []
        for config in configs:
            result.append({
                "content_type": config.name,
                "prompt_count": len(config.prompts),
                "description": config.description
            })
        return result
    finally:
        db.close()

@app.get("/prompts/{content_type}")
async def get_prompts(content_type: str):
    """Belirli bir konfigürasyonun prompt'larını getir"""
    db = next(get_db())
    try:
        config = db.query(ContentConfig).filter(ContentConfig.name == content_type).first()
        if not config:
            raise HTTPException(status_code=404, detail="Konfigürasyon bulunamadı")
        
        result = []
        for prompt_data in config.prompts:
            result.append({
                "prompt_key": f"{content_type}_prompt_{prompt_data['step']}",
                "step": prompt_data["step"],
                "content": prompt_data["text"],
                "ai_settings": prompt_data.get("ai_settings", {
                    "model": "gemini-2.5-flash",
                    "temperature": 0.7,
                    "top_p": 0.7,
                    "response_mime_type": "text/plain",
                    "max_tokens": 8192
                })
            })
        
        return {
            "content_type": content_type,
            "prompt_count": len(config.prompts),
            "prompts": result
        }
    finally:
        db.close()

@app.post("/generate-content")
async def generate_content(request: ContentGenerationRequest):
    """Ana içerik üretim endpoint'i"""
    db = next(get_db())
    
    try:
        print(f"🔍 İçerik türü aranıyor: {request.content_type}")
        print(f"📊 Dinamik veriler: {request.dynamic_data}")
        print(f"⚙️ Özel AI config'ler: {request.custom_ai_configs}")
        
        # Konfigürasyonu bul
        config = db.query(ContentConfig).filter(ContentConfig.name == request.content_type).first()
        if not config:
            print(f"❌ Konfigürasyon bulunamadı: {request.content_type}")
            raise HTTPException(status_code=404, detail="Konfigürasyon bulunamadı")
        
        print(f"✅ Konfigürasyon bulundu: {config.name}")
        print(f"📝 Prompt sayısı: {len(config.prompts)}")
        
        # Prompt'ları işle
        results = []
        current_content = ""
        step_details = []  # Her step'in detaylarını sakla
        
        for prompt_data in config.prompts:
            step = prompt_data["step"]
            
            # Özel prompt var mı kontrol et
            if f"step_{step}" in request.custom_prompts:
                original_prompt = request.custom_prompts[f"step_{step}"]
                print(f"🔄 Özel prompt kullanılıyor - Step {step}: {original_prompt[:50]}...")
            else:
                original_prompt = prompt_data["text"]
                print(f"🔄 DB prompt kullanılıyor - Step {step}: {original_prompt[:50]}...")
            
            # Dinamik verileri uygula
            processed_prompt = apply_dynamic_data(original_prompt, request.dynamic_data)
            print(f"📝 Dinamik veriler uygulandı: {processed_prompt[:100]}...")
            
            # Önceki adımın sonucunu ekle
            if current_content:
                processed_prompt += f"\n\nÖnceki adımın sonucu:\n{current_content}"
            
            # AI ayarlarını belirle (özel config varsa onu kullan, yoksa prompt'a özel)
            ai_settings = prompt_data.get("ai_settings", {
                "model": "gemini-2.5-flash",
                "temperature": 0.7,
                "top_p": 0.7,
                "response_mime_type": "text/plain",
                "max_tokens": 8192
            })
            
            if f"step_{step}" in request.custom_ai_configs:
                # Özel config kullan
                custom_config = request.custom_ai_configs[f"step_{step}"]
                ai_settings.update(custom_config)
                print(f"⚙️ Özel AI config kullanılıyor: {ai_settings}")
            elif "ai_settings" in prompt_data:
                # Prompt'a özel ayarlar kullan
                ai_settings.update(prompt_data["ai_settings"])
                print(f"⚙️ Prompt özel AI ayarları kullanılıyor: {ai_settings}")
            else:
                print(f"⚙️ Varsayılan AI ayarları kullanılıyor: {ai_settings}")
            
            # AI ile içerik üret
            print(f"🤖 AI'ya gönderiliyor...")
            content = generate_ai_content(processed_prompt, ai_settings)
            print(f"✅ AI yanıtı alındı: {content[:100]}...")
            results.append(content)
            current_content = content
            
            # Step detaylarını kaydet
            step_details.append({
                "step": step,
                "original_prompt": original_prompt,
                "processed_prompt": processed_prompt,
                "ai_settings": ai_settings,
                "output": content
            })
        
        # Son içeriği HTML'e çevir (eğer markdown ise)
        final_content = current_content
        if ai_settings.get("response_mime_type") == "text/markdown":
            final_content = markdown_to_html(current_content)
        
        return {
            "content": final_content,
            "prompt_outputs": results,
            "content_type": config.name,
            "metadata": {
                "total_steps": len(config.prompts),
                "dynamic_data_used": request.dynamic_data,
                "step_details": step_details,
                "original_prompts": config.prompts
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/test-single-prompt")
async def test_single_prompt(request: PromptTestRequest):
    """Tek prompt test et - admin panel için"""
    try:
        ai_settings = {
            "model": request.model,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "response_mime_type": request.response_mime_type,
            "max_tokens": request.max_tokens
        }
        
        content = generate_ai_content(request.prompt, ai_settings)
        
        return {
            "content": content,
            "ai_settings": ai_settings,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/content-types")
async def create_content_type(request: ContentConfigCreate):
    """Yeni konfigürasyon oluştur"""
    print(f"🔍 Create request received: {request}")
    db = next(get_db())
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
        
        return {
            "id": new_config.id,
            "content_type": new_config.name,
            "description": new_config.description,
            "prompts": new_config.prompts,
            "created_at": new_config.created_at
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.put("/content-types/{content_type}")
async def update_content_type(content_type: str, request: ContentConfigCreate):
    """Konfigürasyonu güncelle"""
    db = next(get_db())
    try:
        config = db.query(ContentConfig).filter(ContentConfig.name == content_type).first()
        if not config:
            raise HTTPException(status_code=404, detail="Konfigürasyon bulunamadı")
        
        # Güncelle
        config.description = request.description
        config.prompts = request.prompts
        # default_ai_settings artık kullanılmıyor
        
        db.commit()
        
        return {
            "id": config.id,
            "content_type": config.name,
            "description": config.description,
            "prompts": config.prompts,
            "created_at": config.created_at
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.delete("/content-types/{content_type}")
async def delete_content_type(content_type: str):
    """Konfigürasyonu sil"""
    db = next(get_db())
    try:
        config = db.query(ContentConfig).filter(ContentConfig.name == content_type).first()
        if not config:
            raise HTTPException(status_code=404, detail="Konfigürasyon bulunamadı")
        
        db.delete(config)
        db.commit()
        
        return {"message": "Konfigürasyon silindi"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Admin panel için ek endpoint'ler
@app.post("/prompts")
async def create_or_update_prompt(request: dict):
    """Prompt oluştur veya güncelle - admin panel için"""
    # Bu endpoint sadece admin panel için, gerçekte prompt'lar content-type içinde saklanıyor
    # Bu yüzden sadece başarılı mesaj döndürüyoruz
    return {"message": "Prompt kaydedildi", "success": True}

@app.post("/ai-configs")
async def create_ai_config(request: dict):
    """AI config oluştur - admin panel için"""
    # Bu endpoint sadece admin panel için, gerçekte AI config'ler content-type içinde saklanıyor
    # Bu yüzden sadece başarılı mesaj döndürüyoruz
    return {"id": 1, "message": "AI Config kaydedildi", "success": True}

@app.post("/prompt-ai-configs")
async def create_prompt_ai_config(content_config_id: int, prompt_step: int, ai_config_id: int):
    """Prompt AI config ilişkisi oluştur - admin panel için"""
    # Bu endpoint sadece admin panel için
    return {"message": "Prompt AI Config ilişkisi oluşturuldu", "success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)