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


# commands_count = 0
# adm_console = False


# ======================================================================================================DATA

# ======================================================================================================KEYBOARDS


# # Returns keyboard with menu buttons
# def main_keyboard():
#     keyboard = types.ReplyKeyboardMarkup(row_width=2)
#
#     button_1 = types.KeyboardButton(buttons_text[0])
#     button_2 = types.KeyboardButton(buttons_text[1])
#     button_3 = types.KeyboardButton(buttons_text[2])
#     button_4 = types.KeyboardButton(buttons_text[3])
#     button_5 = types.KeyboardButton(buttons_text[4])
#
#     keyboard.add(button_1, button_2, button_3, button_4, button_5)
#     keyboard.resize_keyboard = True
#     return keyboard
#
#
# def settings_keyboard():
#     keyboard = types.ReplyKeyboardMarkup(row_width=3)
#     button_1 = types.KeyboardButton(settings_text[0])
#     button_2 = types.KeyboardButton(settings_text[1])
#
#     button_3 = types.KeyboardButton(settings_text[2])
#     button_4 = types.KeyboardButton(settings_text[3])
#     button_5 = types.KeyboardButton(settings_text[4])
#
#     keyboard.row(button_1, button_2)
#     keyboard.row(button_3)
#     keyboard.row(button_4)
#     keyboard.row(button_5)
#
#     keyboard.resize_keyboard = True
#     return keyboard


def groups_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for group in sorted(timetable.group_list):
        name = group
        button = types.InlineKeyboardButton(name, callback_data=name)
        keyboard.add(button)

    keyboard.resize_keyboard = True

    return keyboard


# def additional_keyboard():
#     keyboard = types.ReplyKeyboardMarkup(row_width=3)
#     button_1 = types.KeyboardButton(additional_text[0])
#     button_2 = types.KeyboardButton(additional_text[1])
#     button_3 = types.KeyboardButton(additional_text[2])
#
#     keyboard.row(button_1, button_2)
#     keyboard.row(button_3)
#
#     keyboard.resize_keyboard = True
#     return keyboard
#

# def admin_keyboard():
#     keyboard = types.ReplyKeyboardMarkup()
#
#     button_1 = types.KeyboardButton("SendMessageToAllUsrs")
#     button_2 = types.KeyboardButton(settings_text[4])
#
#     keyboard.add(button_1)
#     keyboard.add(button_2)
#
#     keyboard.resize_keyboard = True
#     return keyboard


# def change_view_type():
#     keyboard = types.ReplyKeyboardMarkup()
#
#     button_1 = types.KeyboardButton(view_type_text[0])
#     button_2 = types.KeyboardButton(view_type_text[1])
#
#     keyboard.row(button_1, button_2)
#
#     keyboard.resize_keyboard = True
#     return keyboard


# =================================================================================================COMMAND HANDLERS

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


# =================================================================================================KEYBOARD HANDLERS
#
# # Handler for keyboard buttons
# @bot.message_handler(content_types=['text'])
# def keyboard_handlers(message):
#     global adm_console
#     count = check_user_commands(message)
#     change_user_commands(message, count)
#
#     if count + 2 >= 18:
#         if count + 2 == 18:
#             bot.send_message(
#                 message.chat.id,
#                 "Слишком много запросов. Повторите попытку позже"
#             )
#
#         return
#
#     if adm_console:
#         send_message_to_all_users(message.text)
#         adm_console = False
#         bot.send_message(
#             message.chat.id,
#             "done",
#             reply_markup=admin_keyboard()
#         )
#         return
#
#     while Switch(message.text):
#         # main_keyboard buttons
#         if case(buttons_text[0]):
#             timetable_handler(message, 'today')
#             break
#         if case(buttons_text[1]):
#             timetable_handler(message, 'tomorrow')
#             break
#         if case(buttons_text[2]):
#             timetable_handler(message, 'current')
#             break
#         if case(buttons_text[3]):
#             timetable_handler(message, 'next')
#             break
#         # settings button
#         if case(buttons_text[4]):
#             bot.send_message(
#                 message.chat.id,
#                 "Переходим к настройкам .. ",
#                 reply_markup=settings_keyboard()
#             )
#             break
#
#         if case(settings_text[0]):
#             on_help(message)
#             break
#         if case(settings_text[1]):
#             bot.send_message(
#                 message.chat.id,
#                 "Выберите группу:",
#                 reply_markup=groups_keyboard()
#             )
#             break
#         if case(settings_text[2]):
#             bot.send_message(
#                 message.chat.id,
#                 '1️⃣   *Полное:* информация отображается в столбик \n\n2️⃣   *Короткое:* '
#                 'информация отображается в строчку',
#                 parse_mode="Markdown",
#                 reply_markup=change_view_type()
#             )
#             break
#         if case(settings_text[3]):
#             bot.send_message(
#                 message.chat.id,
#                 "Дополнительная информация",
#                 reply_markup=additional_keyboard()
#             )
#             break
#         if case(settings_text[4]):
#             bot.send_message(
#                 message.chat.id,
#                 '📕  Главное меню',
#                 reply_markup=main_keyboard()
#             )
#             break
#
#         if case(view_type_text[0]) or case(view_type_text[1]):
#             change_user_info(message, 'view_type')
#             bot.send_message(
#                 message.chat.id,
#                 'Вид отображения изменен!',
#                 reply_markup=main_keyboard()
#             )
#             break
#
#         # additional keyboard
#         if case(additional_text[0]):
#             bot.send_message(
#                 message.chat.id,
#                 timetable.type_of_week(),
#                 reply_markup=main_keyboard()
#             )
#             break
#
#         if case(additional_text[1]):
#             bot.send_message(
#                 message.chat.id,
#                 abbreviation,
#                 reply_markup=main_keyboard()
#             )
#             break
#
#         # admin
#         if case("admconsole"):
#             bot.send_message(
#                 message.chat.id,
#                 "what you want to do",
#                 reply_markup=admin_keyboard()
#             )
#             break
#
#         if case("SendMessageToAllUsrs"):
#             bot.send_message(
#                 message.chat.id,
#                 "Введите сообщение",
#                 reply_markup=admin_keyboard()
#             )
#             adm_console = True
#
#             break
#
#         # user picked a group
#         if not user.check_user_existence():
#             registration(message)
#         else:
#             change_user_info(message, 'group')
#
#         break


# ================================================================================================================DATA

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


def check_user_commands(message):
    try:
        user_commands_count = database.get_user_data(message.chat.id, "commands_count", database.db_memory)
        return int(user_commands_count)
    except IndexError:
        database.insert_data("users", [message.chat.id, 0], database.db_memory)
        return 0


def change_user_commands(message, count: int):
    condition = "chat_id=" + str(message.chat.id)
    values = {'commands_count': count + 1}
    database.update_data("users", values, database.db_memory, condition)


# def change_user_info(message, info: str):
#     condition = "chat_id=" + str(message.chat.id)
#     values = []
#
#     if info == 'group':
#         values = {"group_name": message.text}
#         bot.send_message(
#             message.chat.id,
#             "Готово! Группа изменена на " + message.text + "✨",
#             reply_markup=main_keyboard()
#         )
#
#     if info == 'view_type':
#         if message.text == view_type_text[0]:
#             values = {"view_type": 'full'}
#         else:
#             values = {"view_type": 'short'}
#
#     database.update_data("users", values, database.db_file, condition)


# =========================================================================================================OTHER


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
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_1 = types.InlineKeyboardButton(strings.buttons_text[0], callback_data=strings.query_timetable[0])
    button_2 = types.InlineKeyboardButton(strings.buttons_text[1], callback_data=strings.query_timetable[1])
    button_3 = types.InlineKeyboardButton(strings.buttons_text[2], callback_data=strings.query_timetable[2])
    button_4 = types.InlineKeyboardButton(strings.buttons_text[3], callback_data=strings.query_timetable[3])
    button_5 = types.InlineKeyboardButton(strings.buttons_text[4], callback_data=strings.query_timetable[4])

    markup.add(button_1, button_2)
    markup.add(button_3, button_4)
    markup.add(button_5)
    return markup


# Setting up user group
@bot.callback_query_handler(lambda query: query.data in timetable.group_list)
def process_callback_groups(query):
    if not user.check_user_existence():
        registration(query)


# Displaying a schedule
@bot.callback_query_handler(lambda query: query.data in strings.query_timetable)
def process_callback_timetable(query):
    if not user.check_user_existence():
        user_manager.reload_user(query.message.message_id)

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


print("bot has been started successfully")
rt = RepeatedTimer(25, database.reset_commands_count)  # it auto-starts, no need of rt.start()
bot.polling(none_stop=True)
