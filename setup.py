import telebot
from decouple import config

API_KEY = config("API_KEY")
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["HI"])
def greet(message):
    bot.reply_to(message, "HI, how can I help you?")


def ipo_request(message):
    req = message.text.split()
    if len(req) < 2 or req[0].lower() not in "ipo":
        return False
    else:
        return True


@bot.message_handler(func=ipo_request)
def ipo(message):
    request = message.text.split()[1]
    bot.send_message(message.chat.id, "HI, welcome in world of IPOs..")


bot.polling()
