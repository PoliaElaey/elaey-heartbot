import os
import openai
import telebot

openai.api_key = "sk-proj-Z1Ngm6PH7Y_IAHSLdLfdo--N_0o4zsfHwOrrePl9UF83TVxaa9Cdn1LhNIdRMXUpoaNocVFXAVT3BIBkFJMO4yWINYUO8lpdWyYxLouL2ovicjy60P5tD-1guHIQ77yEmL_t4_1C3Vdegdacckmogm8zJyMA"
bot = telebot.TeleBot("PASTE_YOUR_TOKEN_HERE")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — добрый и умный помощник."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message['content']
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.infinity_polling()
