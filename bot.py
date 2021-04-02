import telebot
from telebot import types
import tg_analytic

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


@bot.message_handler(content_types=['text'])
def on_text(message):
    if message.text == strings.statistics_keyword:
        get_statistics(message.text, message.chat.id)


# Displaying a schedule
@bot.callback_query_handler(lambda query: query.data in strings.query_timetable)
def process_callback_timetable(query):
    chat_id = query.message.chat.id
    timetable_handler(chat_id, query.data)
    bot.answer_callback_query(query.id)
    tg_analytic.statistics(chat_id, query.data)


# Settings
@bot.callback_query_handler(lambda query: query.data in strings.query_settings)
def process_callback_settings(query):
    chat_id = query.message.chat.id
    settings_handler(chat_id, query.data)
    bot.answer_callback_query(query.id)
    tg_analytic.statistics(chat_id, query.data)


# View_type
@bot.callback_query_handler(lambda query: query.data in strings.query_view_type)
def process_callback_groups(query):
    chat_id = query.message.chat.id
    view_type_handler(chat_id, query.data)
    bot.answer_callback_query(query.id)
    tg_analytic.statistics(chat_id, query.data)


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
    except KeyError:
        bot.send_message(chat_id, "Пожалуйста, выполните команду /start")


def registration(chat_id, query):
    user.initialise_user(query)
    echo(chat_id, strings.registration_text, main_markup())


def changing_group(chat_id, query):
    user.changing_group(query.message.chat.id, query.data, query.message.message_id)
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
    view_type = user.user_data(chat_id, "view_type")
    group_name = user.user_data(chat_id, "group_name")

    if view_type == "None":
        bot.send_message(chat_id, "Пожалуйста, выполните команду /start")
        return 0

    while Switch(string):
        if case(strings.query_timetable[0]):
            echo(chat_id, timetable.get_day_schedule("Сегодня", view_type, group_name), main_markup())
            break
        if case(strings.query_timetable[1]):
            echo(chat_id, timetable.get_day_schedule("Завтра", view_type, group_name), main_markup())
            break
        if case(strings.query_timetable[2]):
            echo(chat_id, timetable.get_week_schedule("Текущая", view_type, group_name), main_markup())
            break
        if case(strings.query_timetable[3]):
            echo(chat_id, timetable.get_week_schedule("Следующая", view_type, group_name), main_markup())
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


def get_statistics(txt, chat_id):
    st = txt.text.split(' ')

    if 'txt' in st or 'тхт' in st:
        tg_analytic.analysis(st, chat_id)
        with open('%s.txt' % chat_id, 'r', encoding='UTF-8') as file:
            bot.send_document(chat_id, file)
            tg_analytic.remove(chat_id)
    else:
        messages = tg_analytic.analysis(st, chat_id)
        bot.send_message(chat_id, messages)


print("bot has been started successfully")
bot.polling(none_stop=True)
