import os
import sqlite3
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASS = os.getenv("ADMIN_PASS", "iadmin")
DOMAIN = os.getenv("DOMAIN", "https://master-oboev.onrender.com")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
app = FastAPI()

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"

# --- Database ---
conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS vip_users (user_id INTEGER PRIMARY KEY)")
cur.execute("CREATE TABLE IF NOT EXISTS wallpapers (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id TEXT, vip_only INTEGER)")
conn.commit()

# --- Handlers ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🖼 Обои", "💎 VIP", "ℹ️ Инфо")
    await message.answer("👋 Привет! Я Мастер Обоев. Выбирай обои!", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "ℹ️ Инфо")
async def info_cmd(message: types.Message):
    await message.answer("📸 Мастер обоев.\nVIP за 23₽/мес или 1000₽ навсегда.\nЗагружай красивые фоны!")

@dp.message_handler(lambda m: m.text == "💎 VIP")
async def vip_cmd(message: types.Message):
    await message.answer("💎 VIP-доступ — 23₽/мес или 1000₽ навсегда.\n(оплата пока не подключена)")

@dp.message_handler(lambda m: m.text == "🖼 Обои")
async def get_wallpapers(message: types.Message):
    cur.execute("SELECT file_id, vip_only FROM wallpapers")
    rows = cur.fetchall()
    if not rows:
        await message.answer("Пока нет обоев 😔")
        return
    for file_id, vip_only in rows:
        if vip_only:
            cur.execute("SELECT * FROM vip_users WHERE user_id=?", (message.from_user.id,))
            if not cur.fetchone():
                continue
        await bot.send_photo(message.chat.id, file_id)

@dp.message_handler(commands=["upload"])
async def upload_cmd(message: types.Message):
    await message.answer("Отправь фото для загрузки (в чат).")

@dp.message_handler(content_types=["photo"])
async def photo_upload(message: types.Message):
    file_id = message.photo[-1].file_id
    cur.execute("INSERT INTO wallpapers (file_id, vip_only) VALUES (?, 0)", (file_id,))
    conn.commit()
    await message.answer("✅ Обои добавлены!")

# --- FastAPI integration ---
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return {"ok": True}
