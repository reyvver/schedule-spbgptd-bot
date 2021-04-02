abbreviation = "БМ» — ул. Большая Морская, д.18\n" \
               "«Д» — пер. Джамбула, д.13\n" \
               "«В» — Вознесенский пр., д.46\n" \
               "«М» — Моховая ул., д.26\n" \
               "'ДО' – дистанционное обучение"

help_text = "Данный бот предназначен для использования студентами вуза СПБГУПТД.\n\n" \
            "Для отображение расписания воспользуйтесь соответсвующими кнопками, отображающимися под сообщением." \
            "При необходимости *перезапустить бота* можно с помощью команды */start* \n\n"\
            "Если при старте была неправильно выбрана *группа*, то изменить ее можно в настройках или с помощью " \
            "команды */set_group* \n\n"\
            "Если возникли какие-то вопросы, обращайтесь на почту\n➡   tvdragunvova@mail.ru"

set_up = "Приятного пользования! ✨\n\n" \
                  "Если нашли ошибку или есть вопросы, обращайтесь на почту\n ➡   tvdragunvova@mail.ru"
return_to_main_menu = "Какое расписание нужно вывести?"

start_text = "Крутим шестеренками.. ⚙ Done!\n\nВыберите свою группу ⬇\n"
registration_text = "Готов к работе! Для отображения расписания воспользуйтесь кнопками снизу"
view_type_text = "Выберите тип ⬇\n\n1️⃣   *Полное:* информация отображается в столбик \n\n2️⃣   *Короткое:* " \
                "информация отображается в строчку"

text_timetable = ['📌 Сегодня', '📋 Завтра', '📍 Эта неделя', '📅 Следующая', '🔧 Настройки']
query_timetable = ["main_today", "main_tomorrow", "main_current", "main_next", "main_settings"]

text_settings = ['❓ Помощь', '👥  Сменить группу', '🧾 Изменить отображение расписания', '⬅  Назад']
query_settings = ["help", "change_group", "change_view_type", "go_back"]

text_view_type = ['1️⃣   Полное', '2️⃣   Короткое']
query_view_type = ["full", "short"]

days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
emoji = ["\U0001F4D5", "\U0001F4D7", "\U0001F4D8", "\U0001F4D9", "\U0001F4D2", "\U0001F4D4"]

statistics_keyword = "statistic_hello_kitty"

group_list = ["1-ТИД-3", "1-ГДА-10", "1-АДА-9"]
# =================================================================================================================

space = "      "


def edit_date_number(number: int):
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)


def edit_string(text: str):
    count = len(text)
    if count > 33:
        index = text.find('; ') + 1
        first_part = text[0:index]
        second_part = text[index:count - 1]
        return first_part + "\n" + space + second_part
    else:
        return text
