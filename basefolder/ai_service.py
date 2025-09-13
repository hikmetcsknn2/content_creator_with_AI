"""
AI service for content generation using Google Gemini
"""
import google.generativeai as genai
from .config import api_key


# Gemini API'yi yapılandır
genai.configure(api_key=api_key)

def generate_ai_content(prompt: str, ai_settings: dict) -> str:
    """
    AI ile içerik üret
    
    Args:
        prompt: AI'ya gönderilecek prompt
        ai_settings: AI ayarları (model, temperature, vb.)
    
    Returns:
        str: AI'dan dönen içerik
    """
    try:
        # Model seç
        model_name = ai_settings.get("model", "gemini-2.5-flash")
        model = genai.GenerativeModel(model_name)
        
        # Generation config
        generation_config = genai.types.GenerationConfig(
            temperature=ai_settings.get("temperature", 0.7),
            top_p=ai_settings.get("top_p", 0.7),
            max_output_tokens=ai_settings.get("max_tokens", 8000),
            response_mime_type=ai_settings.get("response_mime_type", "text/plain")
        )
        
        # İçerik üret
        response = model.generate_content(prompt, generation_config=generation_config)
        
        # Finish reason kontrolü
        if response.candidates and response.candidates[0].finish_reason:
            finish_reason = response.candidates[0].finish_reason
            
            if finish_reason == 2:  # SAFETY
                return "⚠️ İçerik güvenlik politikaları nedeniyle engellendi. Prompt'u değiştirmeyi deneyin."
            elif finish_reason == 3:  # RECITATION
                return "⚠️ İçerik telif hakkı ihlali nedeniyle engellendi. Prompt'u değiştirmeyi deneyin."
            elif finish_reason == 4:  # MAX_TOKENS
                return f"⚠️ Token limiti aşıldı (max_tokens: {ai_settings.get('max_tokens', 8000)}). Limit artırın."
            elif finish_reason == 5:  # STOP
                return "⚠️ İçerik erken durduruldu."
        
        # İçeriği al
        if response.text:
            content = response.text
        else:
            return "⚠️ AI'dan boş yanıt alındı."
        
        
        return content
        
    except Exception as e:
        error_msg = str(e)
        if "finish_reason" in error_msg and "is 2" in error_msg:
            return "⚠️ İçerik güvenlik politikaları nedeniyle engellendi. Prompt'u değiştirmeyi deneyin."
        elif "finish_reason" in error_msg and "is 4" in error_msg:
            return f"⚠️ Token limiti aşıldı (max_tokens: {ai_settings.get('max_tokens', 8000)}). Limit artırın."
        else:
            return f"⚠️ AI içerik üretimi hatası: {error_msg}"
