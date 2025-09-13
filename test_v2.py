#!/usr/bin/env python3
"""
Content Assistant V2 Test Script
"""

import requests
import json

API_BASE = "http://127.0.0.1:8000"

def test_api():
    print("🚀 Content Assistant V2 Test Başlıyor...\n")
    
    # 1. API Status Check
    print("1. API Status Check...")
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"✅ API Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ API Status Error: {e}\n")
        return
    
    # 2. Create Test Configuration
    print("2. Test Konfigürasyonu Oluşturuluyor...")
    test_config = {
        "name": "test_blog",
        "description": "Test blog konfigürasyonu",
        "prompts": [
            {
                "step": 1,
                "text": "Merhaba! {location} hakkında kısa bir araştırma yap.",
                "ai_settings": {
                    "model": "gemini-2.5-flash",
                    "temperature": 0.7,
                    "top_p": 0.7,
                    "response_mime_type": "text/plain",
                    "max_tokens": 500
                }
            },
            {
                "step": 2,
                "text": "Yukarıdaki araştırmaya dayanarak {location} için bir blog yazısı yaz.",
                "ai_settings": {
                    "model": "gemini-2.5-flash",
                    "temperature": 0.8,
                    "top_p": 0.8,
                    "response_mime_type": "text/markdown",
                    "max_tokens": 1000
                }
            }
        ],
        "default_ai_settings": {
            "model": "gemini-2.5-flash",
            "temperature": 0.7,
            "top_p": 0.7,
            "response_mime_type": "text/plain",
            "max_tokens": 1000
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/configs", json=test_config)
        if response.status_code == 200:
            print("✅ Test konfigürasyonu oluşturuldu")
            print(f"   Response: {response.json()}\n")
        else:
            print(f"❌ Konfigürasyon oluşturma hatası: {response.status_code}")
            print(f"   Error: {response.text}\n")
    except Exception as e:
        print(f"❌ Konfigürasyon oluşturma hatası: {e}\n")
    
    # 3. List Configurations
    print("3. Konfigürasyonlar Listeleniyor...")
    try:
        response = requests.get(f"{API_BASE}/configs")
        if response.status_code == 200:
            configs = response.json()
            print(f"✅ {len(configs)} konfigürasyon bulundu")
            for config in configs:
                print(f"   - {config['name']}: {len(config['prompts'])} prompt")
            print()
        else:
            print(f"❌ Konfigürasyon listesi hatası: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Konfigürasyon listesi hatası: {e}\n")
    
    # 4. Test Content Generation
    print("4. İçerik Üretimi Test Ediliyor...")
    test_request = {
        "config_name": "test_blog",
        "dynamic_data": {
            "location": "Antalya"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/generate-content", json=test_request)
        if response.status_code == 200:
            result = response.json()
            print("✅ İçerik başarıyla üretildi")
            print(f"   Konfigürasyon: {result['config_name']}")
            print(f"   Adım sayısı: {result['metadata']['total_steps']}")
            print(f"   Dinamik veri: {result['metadata']['dynamic_data_used']}")
            print(f"   Prompt çıktıları: {len(result['prompt_outputs'])}")
            print(f"   Final içerik uzunluğu: {len(result['content'])} karakter")
            print()
        else:
            print(f"❌ İçerik üretim hatası: {response.status_code}")
            print(f"   Error: {response.text}\n")
    except Exception as e:
        print(f"❌ İçerik üretim hatası: {e}\n")
    
    print("🎉 Test tamamlandı!")

if __name__ == "__main__":
    test_api()
