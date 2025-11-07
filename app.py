
import os
from flask import Flask, request
from telebot import TeleBot, types

TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
bot = TeleBot(TOKEN)
app = Flask(__name__)

ADMIN_PASSWORD = "iadmin"
admin_verified = set()

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL") + '/' + TOKEN)
    return 'Bot is running!', 200

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🖼 Получить обои", "💎 VIP подписка")
    bot.send_message(message.chat.id, "Добро пожаловать в *Мастер Обоев*!", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🖼 Получить обои")
def send_wallpaper(message):
    bot.send_message(message.chat.id, "Вот случайные обои 🌄 (в будущем тут будет выбор)")

@bot.message_handler(func=lambda m: m.text == "💎 VIP подписка")
def vip_info(message):
    bot.send_message(message.chat.id, "💎 VIP доступ: 23₽/мес или 1000₽ навсегда. В разработке.")

@bot.message_handler(commands=['admin'])
def admin_login(message):
    bot.send_message(message.chat.id, "Введите пароль администратора:")
    bot.register_next_step_handler(message, verify_admin)

def verify_admin(message):
    if message.text == ADMIN_PASSWORD:
        admin_verified.add(message.chat.id)
        bot.send_message(message.chat.id, "✅ Пароль подтверждён! Введите /upload для загрузки обоев.")
    else:
        bot.send_message(message.chat.id, "❌ Неверный пароль.")

@bot.message_handler(commands=['upload'])
def upload(message):
    if message.chat.id not in admin_verified:
        bot.send_message(message.chat.id, "❌ Нет доступа. Введите /admin для входа.")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Для всех", "Только VIP")
    bot.send_message(message.chat.id, "Кому выгружать обои?", reply_markup=markup)
    bot.register_next_step_handler(message, choose_access)

def choose_access(message):
    bot.send_message(message.chat.id, f"📤 Загрузка обоев для: {message.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
