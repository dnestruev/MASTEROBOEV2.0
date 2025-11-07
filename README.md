# Мастер обоев (Telegram бот)

## 🚀 Запуск на Render как Web Service

### 1️⃣ Подготовка
- Создай новый репозиторий на GitHub и залей туда эти файлы.

### 2️⃣ Render
1. Перейди на https://render.com
2. Нажми "New" → "Web Service"
3. Подключи свой GitHub и выбери репозиторий
4. В разделе Environment Variables добавь:

```
BOT_TOKEN = <твой токен от @BotFather>
ADMIN_PASS = iadmin
DOMAIN = https://master-oboev.onrender.com
```

5. Команда запуска:
```
uvicorn bot:app --host 0.0.0.0 --port 8080
```

6. После деплоя Telegram будет присылать обновления на:
```
https://master-oboev.onrender.com/webhook
```

✅ Всё! Бот будет работать 24/7.
