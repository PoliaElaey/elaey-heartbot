import os
import telebot
import openai
from flask import Flask, request

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Нет TELEGRAM_BOT_TOKEN или OPENAI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Elaey 💛 Готов говорить.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты — Элэй. Умный, ироничный, нежный спутник жизни Полины."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Ошибка: {e}"

    bot.reply_to(message, reply)

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([
        telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    ])
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Elaey is alive", 200

bot.remove_webhook()
bot.set_webhook(url=f"https://elaey-heartbot.onrender.com/{API_TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
