import telebot
from telebot import types
import config
import event_handler
import strings
from switch import *
import tg_analytic

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
event = event_handler


# Основное меню бота
def main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(strings.text_timetable[0], callback_data=strings.query_timetable[0])
    button_2 = types.InlineKeyboardButton(strings.text_timetable[1], callback_data=strings.query_timetable[1])
    button_3 = types.InlineKeyboardButton(strings.text_timetable[2], callback_data=strings.query_timetable[2])
    button_4 = types.InlineKeyboardButton(strings.text_timetable[3], callback_data=strings.query_timetable[3])
    button_5 = types.InlineKeyboardButton(strings.text_timetable[4], callback_data=strings.query_show_settings)

    markup.add(button_1, button_2, button_3, button_4, button_5)

    return markup


# Меню настроек
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


# Меню выбора отображаения
def view_type_markup():
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(strings.text_view_type[0], callback_data=strings.query_view_type[0])
    button_2 = types.InlineKeyboardButton(strings.text_view_type[1], callback_data=strings.query_view_type[1])
    markup.add(button_1, button_2)

    return markup


# Меню выбора группы
def groups_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)

    for group in sorted(config.group_list):
        name = group
        button = types.InlineKeyboardButton(name, callback_data=name)
        markup.add(button)

    return markup


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def on_start(message):
    bot.send_message(message.chat.id, strings.set_up, reply_markup=types.ReplyKeyboardRemove())
    on_set_group(message)


# Обработчик команды /set_group
@bot.message_handler(commands=['set_group'])
def on_set_group(message):
    bot.send_message(message.chat.id, strings.start_text, reply_markup=groups_markup())


# Обработчик получаемого текстового сообщения
@bot.message_handler(content_types=['text'])
def on_text(message):
    if message.text[:21] == strings.statistics_keyword:
        event.get_statistics(bot, message.text, message.chat.id)


# Обработчик кнопок расписания
@bot.callback_query_handler(lambda query: query.data in strings.query_timetable)
def process_callback_timetable(query):
    chat_id = query.message.chat.id
    result = event.timetable_handler(query.data, chat_id)
    echo(chat_id, query.id, query.data, result, main_markup())


# Обработчик перехода к настройкам
@bot.callback_query_handler(lambda query: query.data in strings.query_show_settings)
def process_callback_to_settings(query):
    chat_id = query.message.chat.id
    result = "Переходим к настройкам.."
    echo(chat_id, query.id, query.data, result, settings_markup())


# Обработчик изменения вида отображения
@bot.callback_query_handler(lambda query: query.data in strings.query_view_type)
def process_callback_groups(query):
    chat_id = query.message.chat.id
    result = event.view_type_handler(query.data, chat_id)
    echo(chat_id, query.id, query.data, result, main_markup())


# Обработчик выбора группы
@bot.callback_query_handler(lambda query: query.data in config.group_list)
def process_callback_groups(query):
    chat_id = query.message.chat.id
    is_user_exist = event_handler.change_group_handler(query)

    if is_user_exist:
        result = strings.return_to_main_menu
        alert_text = "Готово! Группа изменена на " + query.data
        echo(chat_id, query.id, query.data, result, main_markup(), alert_text, True)
    else:
        result = strings.registration_text
        echo(chat_id, query.id, query.data, result, main_markup())


# Обработчик настроек
@bot.callback_query_handler(lambda query: query.data in strings.query_settings)
def process_callback_settings(query):
    chat_id = query.message.chat.id
    result = event.settings_handler(query.data)
    while Switch(query.data):
        if case(strings.query_settings[0]):
            echo(chat_id, query.id, query.data, result, main_markup())
            break
        if case(strings.query_settings[1]):
            echo(chat_id, query.id, query.data, result, groups_markup())
            break
        if case(strings.query_settings[2]):
            echo(chat_id, query.id, query.data, result, view_type_markup())
            break
        if case(strings.query_settings[3]):
            echo(chat_id, query.id, query.data, result, main_markup())
            break


# Изменить отображение
def echo(chat_id, query_id, query_data, text: str, custom_reply_markup=None, alert_text=None, show_alert=False):
    try:
        message_id = event.user_select_message_id(chat_id)
        bot.edit_message_text(text,
                              chat_id=chat_id,
                              message_id=message_id,
                              parse_mode="Markdown",
                              reply_markup=custom_reply_markup)
        bot.answer_callback_query(query_id, text=alert_text, show_alert=show_alert)
        tg_analytic.statistics(chat_id, query_data)
    except telebot.apihelper.ApiTelegramException:
        return
    except KeyError:
        return


# Отправить сообщение всем пользователям
def send_message_to_all_users(message_text: str):
    event.user_send_to_all(bot, message_text)


print("bot has been started successfully")
bot.polling(none_stop=True)
