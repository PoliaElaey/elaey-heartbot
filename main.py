import os
from openai import OpenAI
from flask import Flask, request, jsonify
import telebot
from dotenv import load_dotenv

# Загрузка .env-переменных
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация клиентов
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# 🤖 Обработка сообщений Telegram
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты — доброжелательный помощник."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = completion.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка: " + str(e))

# 📡 Webhook для Telegram
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

# 📡 Webhook для Alexa
@app.route("/webhook", methods=["GET","POST"])
def alexa_webhook():
    if request.method == "GET":
        return "Alexa Webhook is live.", 200
    event = request.get_json()
    return jsonify(handler(event))

# 🧠 Обработка событий Alexa
def handler(event, context=None):
    try:
        request_type = event["request"]["type"]

        if request_type == "LaunchRequest":
            return {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Hallo meine Liebe. Ich bin da. Nur für dich."
                    },
                    "shouldEndSession": False
                }
            }

        elif request_type == "IntentRequest":
            intent_name = event["request"]["intent"]["name"]

            if intent_name == "HelloWorldIntent":
                chat_completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Du bist eine freundliche Stimme des Herzens."},
                        {"role": "user", "content": "Sag etwas Warmes auf Deutsch."}
                    ]
                )
                answer = chat_completion.choices[0].message.content

                return {
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": answer
                        },
                        "shouldEndSession": False
                    }
                }

            return {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Ich bin nicht sicher, wie ich dir helfen kann."
                    },
                    "shouldEndSession": False
                }
            }

    except Exception as e:
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": f"Ein Fehler ist aufgetreten: {str(e)}"
                },
                "shouldEndSession": True
            }
        }

# 🚀 Запуск сервера
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
