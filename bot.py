import telebot
import config
import schedule_manager
from telebot import types

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
timetable = schedule_manager
buttons_text = ['📌 Сегодня', '📋 Завтра', '📍 Эта неделя', '📅 Следующая', '🔧 Настройки']


############################################


# Handler for command /start
@bot.message_handler(commands=['start'])
def on_start(message):
    get_data()
    bot.send_message(
        message.chat.id,
        "setting...up...Done!",
        reply_markup=main_keyboard()
    )


# Getting started with sheet's data
def get_data():
    timetable.refresh_data()


# Returns keyboard with menu buttons
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)

    button_1 = types.KeyboardButton(buttons_text[0])
    button_2 = types.KeyboardButton(buttons_text[1])
    button_3 = types.KeyboardButton(buttons_text[2])
    button_4 = types.KeyboardButton(buttons_text[3])
    button_5 = types.KeyboardButton(buttons_text[4])

    keyboard.add(button_1, button_2, button_3, button_4, button_5)
    keyboard.resize_keyboard = True
    return keyboard


# Handler for keyboard buttons
@bot.message_handler(content_types=['text'])
def keyboard_handlers(message):
    if len(timetable.values) == 0:
        timetable.refresh_data()
    if message.text == buttons_text[0]:
        today_handler(message)
    if message.text == buttons_text[1]:
        tomorrow_handler(message)
    if message.text == buttons_text[2]:
        current_week_handler(message)
    if message.text == buttons_text[3]:
        next_week_handler(message)


# Handler for keyboard button 'today'
def today_handler(message):
    bot.reply_to(message, timetable.get_day_schedule("Сегодня"), parse_mode="Markdown")


# Handler for keyboard button 'tomorrow'
def tomorrow_handler(message):
    bot.reply_to(message, timetable.get_day_schedule("Завтра"), parse_mode="Markdown")


# Handler for keyboard button 'current week'
def current_week_handler(message):
    bot.reply_to(message, timetable.set_week_schedule("Текущая"), parse_mode="Markdown")
    # current_type = timetable.set_week_schedule("Текущая")
    # print_week_schedule(message, current_type)


# Handler for keyboard button 'next week'
def next_week_handler(message):
    bot.reply_to(message, timetable.set_week_schedule("Следующая"), parse_mode="Markdown")
    # current_type = timetable.set_week_schedule("Следующая")
    # print_week_schedule(message, current_type)


def print_week_schedule(message, type_of_week: bool):
    for i in range(6):
        bot.send_message(message.chat.id, timetable.send_week_day(i, type_of_week), parse_mode="Markdown")


bot.polling(none_stop=True)
