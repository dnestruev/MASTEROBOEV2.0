import telebot
from flask import Flask, request

# 🔹 ВСТАВЬ СВОЙ ТОКЕН СЮДА:
TOKEN = "8057107808:AAH4hRcpWp2IKI_MSl1zEmDUsfeFWdk4QT8"

# 🔹 ССЫЛКА НА ТВОЙ САЙТ НА RENDER:
WEBHOOK_URL = f"https://masteroboev2-0.onrender.com/{TOKEN}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ====== ОБРАБОТКА СООБЩЕНИЙ ======
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(
        message,
        "Привет 👋 Я бот *Мастер Обоев!* 🎨\n"
        "Здесь ты можешь получать красивые обои 📱.\n\n"
        "👉 Напиши /vip чтобы узнать о VIP доступе.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['vip'])
def vip_info(message):
    bot.reply_to(
        message,
        "💎 *VIP доступ* позволяет получать эксклюзивные обои!\n\n"
        "💰 Стоимость:\n"
        "• 23 руб/мес\n"
        "• 1000 руб — навсегда 🔥",
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, "Я тебя понял 😊 Используй команды: /start, /vip")

# ====== FLASK ЧАСТЬ ======
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    """Получение апдейтов от Telegram"""
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/', methods=['GET'])
def index():
    """Render проверяет доступность сайта — просто ответим."""
    return '✅ Бот "Мастер Обоев" работает через Render!', 200

# ====== ЗАПУСК ЛОКАЛЬНО (для тестов) ======
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")
    app.run(host='0.0.0.0', port=8080)
