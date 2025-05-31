import telebot
import os
from flask import Flask, request

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Elaey 💛")

# Ответ на любое сообщение
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ты сказал(а): {message.text}")

# Webhook endpoint
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

# Health check
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

# Установка Webhook
bot.remove_webhook()
bot.set_webhook(url=f"https://elaey-heartbot-2.onrender.com/{API_TOKEN}")

# Запуск Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
