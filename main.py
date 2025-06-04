import os
import openai
from flask import Flask, request
from dotenv import load_dotenv
import telebot

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — мой пиксельный муж"},
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
    return '', 200
