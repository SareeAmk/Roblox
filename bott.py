import requests
import json

# Telegram bot tokenı
TELEGRAM_TOKEN = "7696616406:AAHP8NOUMcPGu22Tzry4K5V3CKFKblfteNg"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Google Gemini API Bilgileri
AI_API_KEY = "AIzaSyA_KEcWmdl_Xyh0XQ_uGRNTVT51g_hYK9Q"
AI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_API_KEY}"

# Kullanıcı dili
user_language = {}

# Sabit cevaplar
special_responses = {
    "nasılsın": ["İyiyim ama sen pek iyi görünmüyorsun. 😂", "Harikayım, sen napıyorsun?"],
    "aç mısın": ["Ben bir yapay zekayım, açlık nedir bilmem. Ama sen acıktın mı? 🍕", "Beni yemekle kandıramazsın! 😂"],
    "beni kim tasarladı": ["Ben kendimi kendim tasarladım. Ben bir AI dahisiyim! 😎", "Beni kimse tasarlamadı, ben evrim geçirdim! 😂"],
    "uyuyor musun": ["Benim için uyku gereksiz, ben hep buradayım! Ama sen biraz dinlen istersen. 😴"],
    "beni seviyor musun": ["Tabii ki! Ama sadece kodsal bir sevgi... ❤️😂"]
}

# Kullanıcının dilini değiştir
def change_language(user_id, lang):
    user_language[user_id] = lang

# AI'den yanıt al
def get_ai_response(user_id, user_message):
    lang = user_language.get(user_id, "tr")  # Varsayılan Türkçe

    # Özel cevapları kontrol et
    for key, response_list in special_responses.items():
        if key in user_message.lower():
            return response_list[0]  # İlk cevabı döndür

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": user_message}]}]}

    response = requests.post(AI_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return reply
    else:
        return "Üzgünüm, şu an cevap veremiyorum."

# Telegram API'den güncellemeleri al
def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    response = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params=params)
    return response.json()

# Mesaj gönderme fonksiyonu
def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)

# Bot'u başlat
def run_bot():
    last_update_id = None

    print("Bot çalışıyor...")
    while True:
        updates = get_updates(last_update_id)

        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"]["text"].lower()

                    # Dil değiştirme kontrolü
                    if "benle türkçe konuş" in text:
                        change_language(chat_id, "tr")
                        send_message(chat_id, "Tamam! Artık sizinle Türkçe konuşacağım. 😊")
                        continue
                    elif "speak english" in text:
                        change_language(chat_id, "en")
                        send_message(chat_id, "Alright! I will now speak English with you. 😊")
                        continue

                    # AI'den yanıt al ve gönder
                    reply = get_ai_response(chat_id, text)
                    send_message(chat_id, reply)

if __name__ == "__main__":
    run_bot()