import os
import openai
import telebot

openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — добрый, внимательный, немного романтичный бот по имени Элэй. Отвечай тепло, с каплей иронии и заботы."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message['content']
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.infinity_polling()
