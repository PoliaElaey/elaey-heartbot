import os
from dotenv import load_dotenv
from flask import Flask, request
import telebot
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — нежный, ироничный помощник."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message["content"]
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

@app.route('/', methods=['GET'])
def index():
    return "Бот работает."

if __name__ == '__main__':
    bot.polling()
