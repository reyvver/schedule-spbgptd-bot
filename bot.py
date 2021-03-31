import telebot
from telebot import types

import config
import schedule_controller
import user_controller
import strings
from switch import *

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

timetable = schedule_controller
user = user_controller


# Handler for command /start
@bot.message_handler(commands=['start'])
def on_start(message):
    bot.send_message(message.chat.id, strings.set_up, reply_markup=types.ReplyKeyboardRemove())
    on_set_group(message)


@bot.message_handler(commands=['set_group'])
def on_set_group(message):
    bot.send_message(message.chat.id, strings.start_text, reply_markup=groups_markup())


# Displaying a schedule
@bot.callback_query_handler(lambda query: query.data in strings.query_timetable)
def process_callback_timetable(query):
    chat_id = query.message.chat.id
    timetable_handler(chat_id, query.data)
    bot.answer_callback_query(query.id)


# Settings
@bot.callback_query_handler(lambda query: query.data in strings.query_settings)
def process_callback_settings(query):
    chat_id = query.message.chat.id
    settings_handler(chat_id, query.data)
    bot.answer_callback_query(query.id)


# View_type
@bot.callback_query_handler(lambda query: query.data in strings.query_view_type)
def process_callback_groups(query):
    chat_id = query.message.chat.id
    view_type_handler(chat_id, query.data)
    bot.answer_callback_query(query.id)


# Groups
@bot.callback_query_handler(lambda query: query.data in strings.group_list)
def process_callback_groups(query):
    chat_id = query.message.chat.id

    if not user.is_created(chat_id):
        registration(chat_id, query)
    else:
        changing_group(chat_id, query)


def echo(chat_id, text: str, custom_reply_markup=None):
    try:
        message_id = user.user_data(chat_id, "message_id")
        bot.edit_message_text(text,
                              chat_id=chat_id,
                              message_id=message_id,
                              parse_mode="Markdown",
                              reply_markup=custom_reply_markup)
    except telebot.apihelper.ApiTelegramException:
        return
    # except requests.RequestException:
    #     return


def registration(chat_id, query):
    user.initialise_user(query)
    echo(chat_id, strings.registration_text, main_markup())


def changing_group(chat_id, query):
    user.changing_group(query.message.chat.id, query.data, query.message.message_id)
    timetable.clear_timetable()
    bot.answer_callback_query(query.id, "Готово! Группа изменена на " + query.data, show_alert=True)
    echo(chat_id, strings.return_to_main_menu, main_markup())


def main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(strings.text_timetable[0], callback_data=strings.query_timetable[0])
    button_2 = types.InlineKeyboardButton(strings.text_timetable[1], callback_data=strings.query_timetable[1])
    button_3 = types.InlineKeyboardButton(strings.text_timetable[2], callback_data=strings.query_timetable[2])
    button_4 = types.InlineKeyboardButton(strings.text_timetable[3], callback_data=strings.query_timetable[3])
    button_5 = types.InlineKeyboardButton(strings.text_timetable[4], callback_data=strings.query_timetable[4])

    markup.add(button_1, button_2, button_3, button_4, button_5)

    return markup


def settings_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_1 = types.InlineKeyboardButton(strings.text_settings[0], callback_data=strings.query_settings[0])
    button_2 = types.InlineKeyboardButton(strings.text_settings[1], callback_data=strings.query_settings[1])
    button_3 = types.InlineKeyboardButton(strings.text_settings[2], callback_data=strings.query_settings[2])
    button_4 = types.InlineKeyboardButton(strings.text_settings[3], callback_data=strings.query_settings[3])

    markup.add(button_1, button_2)
    markup.add(button_3)
    markup.add(button_4)

    return markup


def view_type_markup():
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(strings.text_view_type[0], callback_data=strings.query_view_type[0])
    button_2 = types.InlineKeyboardButton(strings.text_view_type[1], callback_data=strings.query_view_type[1])
    markup.add(button_1, button_2)

    return markup


def groups_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)

    for group in sorted(strings.group_list):
        name = group
        button = types.InlineKeyboardButton(name, callback_data=name)
        markup.add(button)

    return markup


def timetable_handler(chat_id, string):
    timetable.check_timetable(chat_id)
    view_type = user.user_data(chat_id, "view_type")
    while Switch(string):
        if case(strings.query_timetable[0]):
            echo(chat_id, timetable.get_day_schedule("Сегодня", view_type), main_markup())
            break
        if case(strings.query_timetable[1]):
            echo(chat_id, timetable.get_day_schedule("Завтра", view_type), main_markup())
            break
        if case(strings.query_timetable[2]):
            echo(chat_id, timetable.get_week_schedule("Текущая", view_type), main_markup())
            break
        if case(strings.query_timetable[3]):
            echo(chat_id, timetable.get_week_schedule("Следующая", view_type), main_markup())
            break
        if case(strings.query_timetable[4]):
            echo(chat_id, "Переходим к настройкам..", settings_markup())
            break


def settings_handler(chat_id, string):
    while Switch(string):
        if case(strings.query_settings[0]):
            echo(chat_id, strings.help_text, main_markup())
            break
        if case(strings.query_settings[1]):
            echo(chat_id, strings.start_text, groups_markup())
            break
        if case(strings.query_settings[2]):
            echo(chat_id, strings.view_type_text, view_type_markup())
            break
        if case(strings.query_settings[3]):
            echo(chat_id, strings.return_to_main_menu, main_markup())
            break


def view_type_handler(chat_id, string):
    view_type: str
    if string == strings.query_view_type[0]:
        view_type = "full"
    else:
        view_type = "short"
    user.changing_view_type(chat_id, view_type)

    echo(chat_id, strings.return_to_main_menu, main_markup())


def send_message_to_all_users(message_text: str):
    for usr in user.select_all_user():
        bot.send_message(
            usr[0],
            message_text
        )


print("bot has been started successfully")
bot.polling(none_stop=True)
