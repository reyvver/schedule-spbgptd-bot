from typing import List

abbreviation = "БМ» — ул. Большая Морская, д.18\n" \
               "«Д» — пер. Джамбула, д.13\n" \
               "«В» — Вознесенский пр., д.46\n" \
               "«М» — Моховая ул., д.26\n" \
               "'ДО' – дистанционное обучение"

help_text = "Данный бот предназначен для использования студентами вуза СПБГУПТД.\n\n" \
            "Для отображение расписания воспользуйтесь соответсвующими кнопками, отображающимися под сообщением." \
            "При необходимости *перезапустить бота* можно с помощью команды */start* \n\n" \
            "Если при старте была неправильно выбрана *группа*, то изменить ее можно в настройках или с помощью " \
            "команды */set_group* \n\n" \
            "Если возникли какие-то вопросы, обращайтесь на почту\n➡   tvdragunvova@mail.ru"

set_up = "Приятного пользования! ✨\n\n" \
         "Если нашли ошибку или есть вопросы, обращайтесь на почту\n ➡   tvdragunvova@mail.ru"
return_to_main_menu = "Какое расписание нужно вывести?"

start_text = "Крутим шестеренками.. ⚙ Done!\n\nВыберите свою группу ⬇\n"
registration_text = "Готов к работе! Для отображения расписания воспользуйтесь кнопками снизу"
view_type_text = "Выберите тип ⬇\n\n1️⃣   *Полное:* информация отображается в столбик \n\n2️⃣   *Короткое:* " \
                 "информация отображается в строчку"

text_timetable = ['📌 Сегодня', '📋 Завтра', '📍 Эта неделя', '📅 Следующая', '🔧 Настройки']
query_timetable = ["main_today", "main_tomorrow", "main_current", "main_next"]
query_show_settings = "main_settings"

text_settings = ['❓ Помощь', '👥  Сменить группу', '🧾 Изменить отображение расписания', '⬅  Назад']
query_settings = ["help", "change_group", "change_view_type", "go_back"]

text_view_type = ['1️⃣   Полное', '2️⃣   Короткое']
query_view_type = ["full", "short"]

days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
emoji = ["\U0001F4D5", "\U0001F4D7", "\U0001F4D8", "\U0001F4D9", "\U0001F4D2", "\U0001F4D4"]

statistics_keyword = "statistic_hello_kitty"
# =================================================================================================================

space = "      "


def edit_date_number(number: int):
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)


def get_full_timetable(data: dict):
    data["name"] = edit_string(data["name"])

    result = space + "⏰ _" + data["time"] + "_\n" + \
             space + "🖍 " + data["name"] + "\n" + \
             space + "🏫 " + data["location"] + "\n" +\
             space + data["group"] + "\n"

    return "\n" + result


def get_short_timetable(data: dict):
    result = "⏰ *" + data["time"] + "* - " + data["name"] + "\n" + \
             space + data["location"] + " " + data["group"]

    return "\n" + result


def edit_string(text: str):
    result: str = ""
    lines: List = [""]
    line_index = 0
    count = len(text)

    if count <= 31:
        return text

    words = text.split(' ')

    for el in words:
        if el == ' ':
            return
        if len(lines[line_index]) + len(el) <= 31:
            lines[line_index] += el + " "
        else:
            line_index += 1
            lines.append(el + " ")

    result += lines[0]

    for index in range(len(lines)):
        if index != 0:
            result += "\n" + space + lines[index]

    return result

