import telebot
from telebot import types
import config
import schedule_manager

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
timetable = schedule_manager


############################################


# handler for command /start
@bot.message_handler(commands=['start'])
def on_start(message):
    get_data()
    bot.send_message(
        message.chat.id,
        "Начнем работу, оки?",
        reply_markup=main_keyboard()
    )


# Show keyboard
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)

    button_1 = types.KeyboardButton('Сегодня')
    button_2 = types.KeyboardButton('Завтра')
    button_3 = types.KeyboardButton('Эта неделя')
    button_4 = types.KeyboardButton('Следующая')

    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard


# Handler for keyboard buttons
@bot.message_handler(content_types=['text'])
def on_text(message):
    if message.text.lower() == "сегодня":
        on_today(message)
    if message.text.lower() == "завтра":
        on_tomorrow(message)
    if message.text.lower() == "эта неделя":
        on_current(message)
    if message.text.lower() == "следующая":
        on_next(message)


# Getting started with sheet's data
def get_data():
    timetable.on_start_schedule()


def on_today(message):
    bot.reply_to(message, timetable.print_day_schedule("сегодня"), parse_mode="Markdown")


# Handler for button 'current week'
def on_current(message):
    bot.send_message(message.chat.id, timetable.print_week_schedule("текущая"), parse_mode="Markdown")


# Handler for button 'today'
def on_next(message):
    bot.send_message(message.chat.id, timetable.print_week_schedule("следующая"), parse_mode="Markdown")


# Handler for button 'tomorrow'
def on_tomorrow(message):
    bot.reply_to(message, timetable.print_day_schedule("завтра"), parse_mode="Markdown")


# # Handler for button 'today'
# def on_today():
#     timetable.print_day_schedule("сегодня")
#
#
# # Handler for button 'tomorrow'
# def on_tomorrow():
#     timetable.print_day_schedule("завтра")
#
#
# # Handler for button 'current week'
# def on_current():
#     timetable.load_data_from_sheet()
#
#
# # Handler for button 'today'
# def on_next():
#     timetable.load_data_from_sheet()


bot.polling(none_stop=True)
