import telebot
import requests

# Telegram bot tokenı
TELEGRAM_TOKEN = '7696616406:AAHP8NOUMcPGu22Tzry4K5V3CKFKblfteNg'

# Google Gemini API Bilgileri
AI_API_KEY = "AIzaSyA_KEcWmdl_Xyh0XQ_uGRNTVT51g_hYK9Q"
AI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_API_KEY}"

# Kullanıcı dili
user_language = {}

bot = telebot.TeleBot(TELEGRAM_TOKEN)

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

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": user_message}]}]
    }
    
    response = requests.post(AI_API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return reply
    else:
        return "Üzgünüm, şu an cevap veremiyorum."

# Başlangıç komutu
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Ben eğlenceli bir sohbet botuyum. Bana her şeyi sorabilirsin!")

# Mesajları işle
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text.lower()

    # Eğer kullanıcı dil değiştirmek istiyorsa
    if "benle türkçe konuş" in text:
        change_language(user_id, "tr")
        bot.reply_to(message, "Tamam! Artık sizinle Türkçe konuşacağım. 😊")
        return
    elif "speak english" in text:
        change_language(user_id, "en")
        bot.reply_to(message, "Alright! I will now speak English with you. 😊")
        return

    # AI'den yanıt al
    reply = get_ai_response(user_id, text)

    # Cevabı gönder
    bot.reply_to(message, reply)

print("Bot çalışıyor...")
bot.polling()