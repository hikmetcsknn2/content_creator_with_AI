"""
Configuration and environment setup
"""
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# API key'i al
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable bulunamadı! .env dosyasında tanımlayın.")

print(f"✅ GEMINI_API_KEY yüklendi: {api_key[:10]}...")

# Database URL
DATABASE_URL = "sqlite:///./content_assistant_v2.db"
