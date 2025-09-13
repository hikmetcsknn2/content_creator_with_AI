# 🚀 Content Assistant V2

**AI-Powered Content Generation System with Admin Panel**

Bu proje, Google Gemini AI kullanarak çok adımlı içerik üretimi yapan bir sistemdir. Admin paneli ile konfigürasyonları yönetebilir, dinamik verilerle özelleştirilmiş içerikler oluşturabilirsiniz.

## ✨ Özellikler

- 🤖 **Google Gemini AI Entegrasyonu** - Gemini 2.5 Flash ve 1.5 Pro modelleri
- 📝 **Çok Adımlı İçerik Üretimi** - Birden fazla prompt ile sıralı içerik oluşturma
- ⚙️ **Esnek Konfigürasyon Sistemi** - Her prompt için ayrı AI ayarları
- 🎛️ **Admin Panel** - Konfigürasyon oluşturma ve test etme
- 🔄 **Dinamik Veri Desteği** - JSON formatında özel veriler
- 📊 **Detaylı Metadata** - Her adımın işlem detayları
- 🌐 **REST API** - Programatik erişim
- 💾 **SQLite Veritabanı** - Hafif ve taşınabilir

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Admin Panel   │    │   FastAPI       │    │   Google        │
│   (Frontend)    │◄──►│   Backend       │◄──►│   Gemini AI     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   SQLite        │
                       │   Database      │
                       │                 │
                       └─────────────────┘
```

## 🚀 Kurulum

### 1. Repository'yi Klonlayın
```bash
git clone <repository-url>
cd content_assistant_clean
```

### 2. Virtual Environment Oluşturun
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Ayarlayın
`.env` dosyası oluşturun:
```bash
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 5. Uygulamayı Başlatın
```bash
python -m uvicorn basefolder.main_v2:app --host 127.0.0.1 --port 8000 --reload
```

### 6. Admin Panelini Açın
Tarayıcınızda `admin_panel_clean.html` dosyasını açın.

## 📖 Kullanım

### Admin Panel

#### 1. Konfigürasyon Oluşturma
- **"➕ Yeni Konfigürasyon"** sekmesine gidin
- Konfigürasyon adını girin (örn: "blog", "makale")
- Prompt sayısını seçin
- Her prompt için:
  - İçeriği yazın
  - AI ayarlarını yapılandırın (model, temperature, top_p, mime type)
- **"Konfigürasyon Oluştur"** butonuna tıklayın

#### 2. Test ve Düzenleme
- **"🧪 Test & Düzenleme"** sekmesine gidin
- Mevcut konfigürasyonu seçin
- Prompt'ları düzenleyin
- Dinamik verileri JSON formatında girin:
  ```json
  {
    "topic": "teknoloji",
    "location": "İstanbul",
    "target_audience": "geliştiriciler"
  }
  ```
- **"Test Çalıştır"** butonuna tıklayın
- Sonuçları inceleyin ve gerekirse kaydedin

### API Kullanımı

#### İçerik Üretimi
```bash
curl -X POST "http://127.0.0.1:8000/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "blog",
    "dynamic_data": {
      "topic": "yapay zeka",
      "audience": "başlangıç seviyesi"
    }
  }'
```

#### Konfigürasyon Listesi
```bash
curl -X GET "http://127.0.0.1:8000/content-types"
```

## 🔧 Konfigürasyon Formatı

### Prompt Yapısı
```json
{
  "step": 1,
  "text": "Blog yazısı için başlık oluştur. Konu: {topic}",
  "ai_settings": {
    "model": "gemini-2.5-flash",
    "temperature": 0.7,
    "top_p": 0.7,
    "response_mime_type": "text/plain",
    "max_tokens": 8192
  }
}
```

### Dinamik Veri Kullanımı
Prompt'larda `{variable_name}` formatında değişkenler kullanabilirsiniz:
- `{topic}` → Dinamik veri: `{"topic": "teknoloji"}`
- `{location}` → Dinamik veri: `{"location": "İstanbul"}`

## 📊 API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `GET` | `/content-types` | Tüm konfigürasyonları listele |
| `GET` | `/prompts/{content_type}` | Belirli konfigürasyonun prompt'larını getir |
| `POST` | `/content-types` | Yeni konfigürasyon oluştur |
| `PUT` | `/content-types/{content_type}` | Konfigürasyon güncelle |
| `DELETE` | `/content-types/{content_type}` | Konfigürasyon sil |
| `POST` | `/generate-content` | İçerik üret |

## 🎯 Örnek Kullanım Senaryoları

### 1. Blog Yazısı
```json
{
  "content_type": "blog",
  "dynamic_data": {
    "topic": "yapay zeka",
    "target_audience": "geliştiriciler",
    "word_count": "1000"
  }
}
```

### 2. Ürün Açıklaması
```json
{
  "content_type": "product_description",
  "dynamic_data": {
    "product_name": "Akıllı Saat",
    "features": "kalp ritmi, GPS, su geçirmez",
    "price_range": "orta segment"
  }
}
```

### 3. Sosyal Medya İçeriği
```json
{
  "content_type": "social_media",
  "dynamic_data": {
    "platform": "Instagram",
    "content_type": "hikaye",
    "hashtags": "#teknoloji #ai"
  }
}
```

## 🔍 Debug ve Loglar

Uygulama çalışırken terminal'de şu bilgileri görebilirsiniz:
- 🔑 API Key yükleme durumu
- 🔍 İçerik türü arama
- 📊 Dinamik veriler
- ⚙️ AI ayarları
- 🤖 AI yanıtları
- ⚠️ Hata mesajları

## 🛠️ Geliştirme

### Proje Yapısı
```
content_assistant_clean/
├── basefolder/
│   ├── main_v2.py          # FastAPI backend
│   └── models_v2.py        # SQLAlchemy modelleri
├── admin_panel_clean.html  # Admin panel frontend
├── requirements.txt        # Python bağımlılıkları
├── .env                   # Environment variables
├── .gitignore            # Git ignore kuralları
└── README.md             # Bu dosya
```

### Yeni Özellik Ekleme
1. Backend'de yeni endpoint ekleyin (`main_v2.py`)
2. Gerekirse yeni model ekleyin (`models_v2.py`)
3. Frontend'de yeni UI bileşeni ekleyin (`admin_panel_clean.html`)
4. Test edin ve dokümantasyonu güncelleyin

## 🐛 Sorun Giderme

### Yaygın Hatalar

#### 1. API Key Hatası
```
ValueError: GEMINI_API_KEY environment variable bulunamadı!
```
**Çözüm:** `.env` dosyasında API key'inizi kontrol edin.

#### 2. Token Limiti Hatası
```
⚠️ Token limiti aşıldı (max_tokens: 1000)
```
**Çözüm:** Konfigürasyonunuzda `max_tokens` değerini artırın (önerilen: 8192).

#### 3. Güvenlik Filtresi
```
⚠️ Güvenlik filtresi: Prompt'u değiştirin
```
**Çözüm:** Prompt'unuzu daha açıklayıcı ve uygun hale getirin.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Sorularınız için issue açabilir veya iletişime geçebilirsiniz.

---

**Not:** Bu proje Google Gemini AI API'sini kullanır. API kullanım limitlerinizi kontrol etmeyi unutmayın.
