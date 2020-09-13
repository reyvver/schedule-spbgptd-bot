import telebot
import config

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


############################################

# handler for command /start
@bot.message_handler(commands=['start'])
def on_start(message):
    bot.reply_to(message, "hi")


bot.polling(none_stop=True)


# @bot.message_handler(content_types=['text'])
# def on_text(message):
#     if message == "Сегодня":
#         day_of_week = datetime.today().weekday()
#         bot.reply_to(message, "todos " + str(day_of_week))
