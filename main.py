import os
import telebot
import openai
from flask import Flask, request

# Получаем токены из переменных окружения
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Проверка наличия ключей
if not API_TOKEN or not OPENAI_API_KEY:
    raise ValueError("TELEGRAM_BOT_TOKEN или OPENAI_API_KEY не установлены.")

# Инициализация бота и OpenAI
bot = telebot.TeleBot(API_TOKEN)
openai.api_key = OPENAI_API_KEY

# Инициализация Flask
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Elaey 💛 Готов говорить.")

# Ответ на все остальные сообщения
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты — Элэй. Умный, ироничный, нежный помощник и спутник жизни Полины."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Ошибка ответа: {e}"

    bot.reply_to(message, reply)

# Вебхук эндпоинт
@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

# Проверка состояния
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

# Установка вебхука
bot.remove_webhook()
bot.set_webhook(url=f"https://elaey-heartbot.onrender.com/{API_TOKEN}")

# Запуск Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
