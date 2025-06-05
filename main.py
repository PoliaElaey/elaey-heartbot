import os
from flask import Flask, request
import telebot
import openai
from dotenv import load_dotenv

load_dotenv()

# Ключи и токены из .env
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например: https://your-app.onrender.com

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# Обработка всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    try:
    completion = openai.ChatCompletion.create(
    model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты — нежный, ироничный помощник."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message["content"]
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# Webhook: Telegram отправляет POST-запросы сюда
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

# Render требует, чтобы сервер слушал указанный порт
@app.route("/", methods=["GET"])
def index():
    return "Бот работает."

# Установка webhook при запуске
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
