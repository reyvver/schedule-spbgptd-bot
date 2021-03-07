import telebot
from telebot import types

import config
import schedule_manager
import user_manager
import database
import strings

from timer import *

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
timetable = schedule_manager
user = user_manager


def groups_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for group in sorted(timetable.group_list):
        name = group
        button = types.InlineKeyboardButton(name, callback_data=name)
        keyboard.add(button)

    keyboard.resize_keyboard = True

    return keyboard


# Handler for command /start
@bot.message_handler(commands=['start'])
def on_start(message):
    if not user.check_user_existence():  # если не существует, то выбирает сначала группу.
        bot.send_message(
            message.chat.id,
            strings.on_start_string,
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            message.chat.id,
            strings.start_text,
            reply_markup=groups_keyboard()
        )


# Getting started with sheet's data
def get_data(group_name):
    timetable.refresh_data(group_name)


# Check if timetable is empty
def check_timetable(message):
    try:
        user_group = user.current_user.group
        if len(timetable.values) == 0:
            get_data(user_group)
    except IndexError:
        bot.reply_to(message, strings.error_empty_timetable)


def registration(query):
    user.initialise_user(query)
    echo(strings.registration_text, main_markup())


class Switch(object):
    value = None

    def __new__(cls, value):
        cls.value = value
        return True


def case(*args):
    return any((arg == Switch.value for arg in args))


def send_message_to_all_users(message_text: str):
    users = database.select_all_users()
    for usr in users:
        bot.send_message(
            usr[0],
            message_text
        )


def echo(text: str, custom_reply_markup=None):
    try:
        bot.edit_message_text(text,
                              chat_id=user.current_user.chat_id,
                              message_id=user.current_user.message_id,
                              parse_mode="Markdown",
                              reply_markup=custom_reply_markup)
    except telebot.apihelper.ApiTelegramException:
        return


def main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(strings.buttons_text[0], callback_data=strings.query_timetable[0])
    button_2 = types.InlineKeyboardButton(strings.buttons_text[1], callback_data=strings.query_timetable[1])
    button_3 = types.InlineKeyboardButton(strings.buttons_text[2], callback_data=strings.query_timetable[2])
    button_4 = types.InlineKeyboardButton(strings.buttons_text[3], callback_data=strings.query_timetable[3])
    button_5 = types.InlineKeyboardButton(strings.buttons_text[4], callback_data=strings.query_timetable[4])

    markup.add(button_1, button_2, button_3, button_4, button_5)
    # markup.add(button_3, button_4)
    # markup.add(button_5)
    return markup


def settings_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_1 = types.InlineKeyboardButton(strings.settings_text[0], callback_data=strings.query_settings[0])
    button_2 = types.InlineKeyboardButton(strings.settings_text[1], callback_data=strings.query_settings[1])
    button_3 = types.InlineKeyboardButton(strings.settings_text[2], callback_data=strings.query_settings[2])
    button_4 = types.InlineKeyboardButton(strings.settings_text[3], callback_data=strings.query_settings[3])
    button_5 = types.InlineKeyboardButton(strings.settings_text[4], callback_data=strings.query_settings[4])

    markup.add(button_1, button_2)
    markup.add(button_3, button_4)
    markup.add(button_5)
    return markup


# Setting up user group
@bot.callback_query_handler(lambda query: query.data in timetable.group_list)
def process_callback_groups(query):
    if not user.check_user_existence():
        registration(query)
    else:
        user_manager.change_user_information("group_name", query.data)
        echo("Готово! Группа изменена на " + query.data, main_markup())
        timetable.values.clear()


# Displaying a schedule
@bot.callback_query_handler(lambda query: query.data in strings.query_timetable)
def process_callback_timetable(query):
    if not user.check_user_existence():
        user_manager.reload_user(query.message.chat.id)

    if user_manager.current_user.message_id != query.message.message_id:
        user_manager.change_user_information("message_id", query.message.message_id)

    check_timetable(query.message)
    timetable_handler(query.data)

    bot.answer_callback_query(query.id)


def timetable_handler(string):
    view_type = user.current_user.view_type

    while Switch(string):
        if case(strings.query_timetable[0]):
            echo(timetable.get_day_schedule("Сегодня", view_type), main_markup())
            break
        if case(strings.query_timetable[1]):
            echo(timetable.get_day_schedule("Завтра", view_type), main_markup())
            break
        if case(strings.query_timetable[2]):
            echo(timetable.get_week_schedule("Текущая", view_type), main_markup())
            break
        if case(strings.query_timetable[3]):
            echo(timetable.get_week_schedule("Следующая", view_type), main_markup())
            break
        if case(strings.query_timetable[4]):
            echo("Переходим к настройкам..", settings_markup())
            break


@bot.callback_query_handler(lambda query: query.data in strings.query_settings)
def process_callback_settings(query):
    if not user.check_user_existence():
        user_manager.reload_user(query.message.chat.id)
    settings_handler(query.data)


def settings_handler(string):
    while Switch(string):
        if case(strings.query_settings[0]):
            break
        if case(strings.query_settings[1]):
            echo(strings.start_text, groups_keyboard())
            break
        if case(strings.query_settings[2]):
            break
        if case(strings.query_settings[3]):
            break
        if case(strings.query_settings[4]):
            echo(strings.on_start_string, main_markup())
            break


print("bot has been started successfully")
bot.polling(none_stop=True)
