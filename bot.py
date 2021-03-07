import telebot
import config
import schedule_manager
import database
from telebot import types

from time import sleep
from timer import *

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
timetable = schedule_manager

buttons_text = ['📌 Сегодня', '📋 Завтра', '📍 Эта неделя', '📅 Следующая', '🔧 Настройки']
settings_text = ['❓ Помощь', '👥  Сменить группу', '🧾 Изменить отображение расписания', '⚙   Дополнительно',
                 '⬅  Назад']
additional_text = ['📙 Четность недели', '📗 Обозначения', '⬅  Назад']
view_type_text = ['1️⃣   Полное', '2️⃣   Короткое']

start_text = "setting...up...Done!\n\n" \
             "Выберите свою группу ⬇\n"
help_text = ("Данный бот предназначен для использования студентами вуза СПБГУПТД.\n\n " +
             "*Список команд*:\n" +
             "/help — Справка по боту\n" +
             "/start — Перезапустить бота\n" +
             "/today — Расписание на сегодня\n" +
             "/tomorrow — Расписание на завтра\n" +
             "/week — Расписание на текущую неделю\n" +
             "/next — Расписание на следующую неделю\n\n" +
             "Если нашли ошибку или есть вопросы, обращайтесь на почту\n ➡   tvdragunvova@mail.ru")
abbreviation = "БМ» — ул. Большая Морская, д.18\n" \
               "«Д» — пер. Джамбула, д.13\n" \
               "«В» — Вознесенский пр., д.46\n" \
               "«М» — Моховая ул., д.26\n" \
               "'ДО' – дистанционное обучение" \

commands_count = 0
adm_console = False


# ======================================================================================================KEYBOARDS


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


def settings_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    button_1 = types.KeyboardButton(settings_text[0])
    button_2 = types.KeyboardButton(settings_text[1])

    button_3 = types.KeyboardButton(settings_text[2])
    button_4 = types.KeyboardButton(settings_text[3])
    button_5 = types.KeyboardButton(settings_text[4])

    keyboard.row(button_1, button_2)
    keyboard.row(button_3)
    keyboard.row(button_4)
    keyboard.row(button_5)

    keyboard.resize_keyboard = True
    return keyboard


def groups_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    number = 0

    for group in sorted(timetable.group_list):
        name = group
        # values = [number, name]
        # # database.insert_data("groups_list", values, database.db_file)

        button = types.KeyboardButton(name)
        keyboard.add(button)

        number += 1

    keyboard.resize_keyboard = True
    return keyboard


def additional_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    button_1 = types.KeyboardButton(additional_text[0])
    button_2 = types.KeyboardButton(additional_text[1])
    button_3 = types.KeyboardButton(additional_text[2])

    keyboard.row(button_1, button_2)
    keyboard.row(button_3)

    keyboard.resize_keyboard = True
    return keyboard


def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    button_1 = types.KeyboardButton("SendMessageToAllUsrs")
    button_2 = types.KeyboardButton(settings_text[4])

    keyboard.add(button_1)
    keyboard.add(button_2)

    keyboard.resize_keyboard = True
    return keyboard


def change_view_type():
    keyboard = types.ReplyKeyboardMarkup()

    button_1 = types.KeyboardButton(view_type_text[0])
    button_2 = types.KeyboardButton(view_type_text[1])

    keyboard.row(button_1, button_2)

    keyboard.resize_keyboard = True
    return keyboard


# =================================================================================================COMMAND HANDLERS

# Handler for command /start
@bot.message_handler(commands=['start'])
def on_start(message):
    if not check_user_existence(message):
        bot.send_message(
            message.chat.id,
            start_text,
            reply_markup=groups_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "setting...up...Done! ⬇",
            reply_markup=main_keyboard()
        )


# Handler for command /help
@bot.message_handler(commands=['help'])
def on_help(message):
    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode="Markdown"
    )


# Handler for command /today
@bot.message_handler(commands=['today'])
def on_today(message):
    timetable_handler(message, 'today')


# Handler for command /tomorrow
@bot.message_handler(commands=['tomorrow'])
def on_tomorrow(message):
    timetable_handler(message, 'tomorrow')


# Handler for command /week
@bot.message_handler(commands=['week'])
def on_week(message):
    timetable_handler(message, 'current')


# Handler for command /next
@bot.message_handler(commands=['next'])
def on_next(message):
    timetable_handler(message, 'next')


# =================================================================================================KEYBOARD HANDLERS

# Handler for keyboard buttons
@bot.message_handler(content_types=['text'])
def keyboard_handlers(message):
    global adm_console
    count = check_user_commands(message)
    change_user_commands(message, count)

    if count + 2 >= 18:
        if count + 2 == 18:
            bot.send_message(
                message.chat.id,
                "Слишком много запросов. Повторите попытку позже"
            )

        return

    if adm_console:
        send_message_to_all_users(message.text)
        adm_console = False
        bot.send_message(
            message.chat.id,
            "done",
            reply_markup=admin_keyboard()
        )
        return

    while Switch(message.text):
        # main_keyboard buttons
        if case(buttons_text[0]):
            timetable_handler(message, 'today')
            break
        if case(buttons_text[1]):
            timetable_handler(message, 'tomorrow')
            break
        if case(buttons_text[2]):
            timetable_handler(message, 'current')
            break
        if case(buttons_text[3]):
            timetable_handler(message, 'next')
            break
        # settings button
        if case(buttons_text[4]):
            bot.send_message(
                message.chat.id,
                "Переходим к настройкам .. ",
                reply_markup=settings_keyboard()
            )
            break

        if case(settings_text[0]):
            on_help(message)
            break
        if case(settings_text[1]):
            bot.send_message(
                message.chat.id,
                "Выберите группу:",
                reply_markup=groups_keyboard()
            )
            break
        if case(settings_text[2]):
            bot.send_message(
                message.chat.id,
                '1️⃣   *Полное:* информация отображается в столбик \n\n2️⃣   *Короткое:* '
                'информация отображается в строчку',
                parse_mode="Markdown",
                reply_markup=change_view_type()
            )
            break
        if case(settings_text[3]):
            bot.send_message(
                message.chat.id,
                "Дополнительная информация",
                reply_markup=additional_keyboard()
            )
            break
        if case(settings_text[4]):
            bot.send_message(
                message.chat.id,
                '📕  Главное меню',
                reply_markup=main_keyboard()
            )
            break

        if case(view_type_text[0]) or case(view_type_text[1]):
            change_user_info(message, 'view_type')
            bot.send_message(
                message.chat.id,
                'Вид отображения изменен!',
                reply_markup=main_keyboard()
            )
            break

        # additional keyboard
        if case(additional_text[0]):
            bot.send_message(
                message.chat.id,
                timetable.type_of_week(),
                reply_markup=main_keyboard()
            )
            break

        if case(additional_text[1]):
            bot.send_message(
                message.chat.id,
                abbreviation,
                reply_markup=main_keyboard()
            )
            break

        # admin
        if case("admconsole"):
            bot.send_message(
                message.chat.id,
                "what you want to do",
                reply_markup=admin_keyboard()
            )
            break

        if case("SendMessageToAllUsrs"):
            bot.send_message(
                message.chat.id,
                "Введите сообщение",
                reply_markup=admin_keyboard()
            )
            adm_console = True

            break

        # user picked a group
        if not check_user_existence(message):
            registration(message)
        else:
            change_user_info(message, 'group')

        break


# ================================================================================================================DATA

# Getting started with sheet's data
def get_data(group_name):
    timetable.refresh_data(group_name)


# Check if timetable is empty
def check_timetable(message):
    try:
        user_group = database.get_user_data(message.chat.id, "group_name", database.db_file)
        if len(timetable.values) == 0:
            get_data(user_group)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, сделайте рестарт с помощью команды /start")


def registration(message):
    chat_id = message.chat.id
    user_name = message.chat.username
    first_name = message.from_user.first_name
    group_name = message.text

    database.register_user(chat_id, user_name, first_name, group_name)
    bot.send_message(
        message.chat.id,
        "Приятного пользования! ✨\n\nПри необходимости воспользуйтесь командой /help",
        reply_markup=main_keyboard()
    )


def check_user_commands(message):
    try:
        user_commands_count = database.get_user_data(message.chat.id, "commands_count", database.db_memory)
        return int(user_commands_count)
    except IndexError:
        database.insert_data("users", [message.chat.id, 0], database.db_memory)
        return 0


def check_user_existence(message):
    result: bool = False
    try:
        user_name = database.get_user_data(message.chat.id, "chat_id", database.db_file)
        result = True
    except telebot.apihelper.ApiTelegramException:
        result = False
    finally:
        return result


def change_user_commands(message, count: int):
    condition = "chat_id=" + str(message.chat.id)
    values = {'commands_count': count + 1}
    database.update_data("users", values, database.db_memory, condition)


def change_user_info(message, info: str):
    condition = "chat_id=" + str(message.chat.id)
    values = []

    if info == 'group':
        values = {"group_name": message.text}
        bot.send_message(
            message.chat.id,
            "Готово! Группа изменена на " + message.text + "✨",
            reply_markup=main_keyboard()
        )

    if info == 'view_type':
        if message.text == view_type_text[0]:
            values = {"view_type": 'full'}
        else:
            values = {"view_type": 'short'}

    database.update_data("users", values, database.db_file, condition)


# =========================================================================================================OTHER


class Switch(object):
    value = None

    def __new__(cls, value):
        cls.value = value
        return True


def case(*args):
    return any((arg == Switch.value for arg in args))


# Handler for timetable
def timetable_handler(message, command: str):
    check_timetable(message)

    view_type = database.get_user_data(message.chat.id, "view_type", database.db_file)

    while Switch(command):
        if case('today'):
            bot.reply_to(message, timetable.get_day_schedule("Сегодня", view_type),
                         parse_mode="Markdown")
            break
        if case('tomorrow'):
            bot.reply_to(message, timetable.get_day_schedule("Завтра", view_type),
                         parse_mode="Markdown")
            break
        if case('current'):
            bot.reply_to(message, timetable.get_week_schedule("Текущая", view_type),
                         parse_mode="Markdown")
            break
        if case('next'):
            bot.reply_to(message, timetable.get_week_schedule("Следующая", view_type),
                         parse_mode="Markdown")
            break


def show_main_menu(message):
    bot.send_message(
        message.chat.id,
        "Главное меню ⬇",
        reply_markup=main_keyboard()
    )


def send_message_to_all_users(message_text: str):
    users = database.select_all_users()
    for user in users:
        bot.send_message(
            user[0],
            message_text
        )


print("bot has been started successfully")
rt = RepeatedTimer(25, database.reset_commands_count)  # it auto-starts, no need of rt.start()
bot.polling(none_stop=True)