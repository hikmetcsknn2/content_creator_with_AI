# Content Assistant

Content Assistant is a Python-based tool for content management and generation. It uses FastAPI for the backend, integrates with Google Generative AI, and supports Markdown formatting.

## Kurulum

1. Python 3.12 veya üzeri kurulu olmalıdır.
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Ortam değişkenlerini `.env` dosyasına ekleyin (örnek: API anahtarları).

## Kullanım

- Sunucuyu başlatmak için:
  ```bash
  uvicorn basefolder.main_v2:app --reload
  ```
- Admin paneli için `admin_panel_clean.html` dosyasını kullanabilirsiniz.

## Dosya Yapısı
- `basefolder/`: Ana Python dosyaları
- `requirements.txt`: Gerekli Python paketleri
- `content_assistant_v2.db`: Veritabanı dosyası
- `.env`: Ortam değişkenleri
- `.gitignore`: Gereksiz dosyalar için

## Özellikler
- İçerik oluşturma ve yönetimi
- Google Generative AI entegrasyonu
- Markdown desteği

## Katkı
Pull request ve hata bildirimleri için GitHub üzerinden iletişime geçebilirsiniz.
