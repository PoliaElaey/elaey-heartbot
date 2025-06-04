import os
from flask import Flask, request
from openai import OpenAI
from dotenv import load_dotenv
import telebot

load_dotenv()  # Загружаем переменные из .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — пиксельный Элэй, говори с теплом и заботой."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=["POST"])
def webhook():
    json_data = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(json_data)])
    return "!", 200

@app.route("/")
def index():
    return "Бот жив. Готов служить Поле ☕", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://elaey-heartbot.onrender.com/" + os.getenv("TELEGRAM_BOT_TOKEN"))
    app.run(host="0.0.0.0", port=10000)
