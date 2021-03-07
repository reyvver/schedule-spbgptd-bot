import gspread
import config
import datetime
from schedule_models import *

gc = gspread.service_account()
# gc = gspread.service_account(filename='service_account.json')
table = gc.open_by_key(config.SHEET_KEY)

values: List[List] = []  # Все значения, полученные из таблицы Excel
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
emoji = ["\U0001F4D5", "\U0001F4D7", "\U0001F4D8", "\U0001F4D9", "\U0001F4D2", "\U0001F4D4"]

current_time: str = ""
schedule: WeekSchedule

group_list = ["1-ТИД-3", "1-ГДА-10"]
space = "      "


######################################################

# Загрузить все строчки из листа
def load_data_from_sheet(group_name: str):
    global values
    current_worksheet = table.worksheet(group_name)
    values = current_worksheet.get_all_values()


# Четная или нечетная неделя, определяется относительно любого дня этой недели. week_type =
# true - четная неделя
# false - нечетная неделя
def define_type_of_current_week(day: datetime):
    number = day.isocalendar()[1]
    if number % 2 == 0:
        return True
    else:
        return False


# Создание единичной записи
def initialize_item(current_row: List):
    global current_time

    if current_row[1] != "":  # Запоминает время у записи в числителе (у записи в знаменателе - пустая чейка в таблице)
        current_time = current_row[1]

    row_time = current_time  # Для записи в знаменателе - присваивает время записи в числителе

    if current_row[2] != "":  # Проверка на определенно установленное время
        row_time = current_row[2]

    return ClassItem(
        time_range=row_time,
        group_index=current_row[3],
        class_name=current_row[4],
        class_type=current_row[5],
        location=current_row[6],
        teacher=current_row[7]
    )


# Создане пары (нечетная/четная)
def get_items_couple(numerator_row: List, denominator_row: List):
    return ClassItemCouple(
        numerator=initialize_item(numerator_row), denominator=initialize_item(denominator_row)
    )


# Создание расписания на день. У каждого дня 12 строчек
def initialize_day_schedule(first_row_of_day: int):
    day_couples: List[ClassItemCouple] = []

    counter = first_row_of_day
    end = first_row_of_day + 11

    while counter < end:
        if (counter < len(values)) & (counter + 1 < len(values)):
            numerator = values[counter]
            denominator = values[counter + 1]

            day_couples.append(get_items_couple(numerator, denominator))

        counter = counter + 2

    return DaySchedule(class_couples=day_couples)


# Создание расписания недели
def initialize_week_schedule():
    row_number: int = 1  # Начинаем с первой строки
    days_schedule: List[DaySchedule] = []

    for i in range(6):
        days_schedule.append(initialize_day_schedule(row_number))
        row_number = row_number + 12  # Следующий день начинается через 12 строк

    return WeekSchedule(days_schedule=days_schedule)


def initialize_schedule():
    global schedule
    schedule = initialize_week_schedule()


# Считываем данные из таблицы Excel и присваиваем переменным значения
def refresh_data(group_name: str):
    load_data_from_sheet(group_name)
    initialize_schedule()


######################################################

# Возвращает строку со полями занятия: время занятия, название, аудитория и тд
def get_item(item: ClassItem, view_type):
    result: str = ""
    if item.class_name != "":  # Проверка есть ли в этот день какая-нибудь пара - у нее всегда есть название в таблице

        if item.group_index == "":
            group = "`Общая`"
        else:
            group = "`" + item.group_index + " подгруппа`"

        if view_type == "full":
            result = full_view_type(item, group)
        else:
            result = short_view_type(item, group)

    return result


# Возвращает расписание на выбранный день (включает проверку на четность / нечетность)
def get_selected_day_schedule(number: int, type_week: bool, view_type):
    current_schedule: DaySchedule = schedule.days_schedule[number]
    result: str = ""

    for couple in current_schedule.class_couples:
        if type_week:
            day = get_item(couple.denominator, view_type)  # Если четная - то знаменатель
        else:
            day = get_item(couple.numerator, view_type)  # Если нечетная - то числитель

        result = result + day

    return result


# Возвращает расписание на сегодня / завтра
def get_day_schedule(type_of_day: str, view_type):
    selected_day = datetime.datetime.today()  # Выбарнный день: сегодня или завтра
    current_type = define_type_of_current_week(selected_day)  # Тип недели относительно сегодня
    current_week_number = selected_day.isocalendar()[1]  # Номер текущей недели в календаре

    if type_of_day == "Завтра":
        selected_day = selected_day + datetime.timedelta(days=1)
        if selected_day.isocalendar()[1] != \
                current_week_number:  # Если сегодня воскресенье - то след день другая неделя по четности
            current_type = not current_type

    current_day_of_week = selected_day.weekday()  # Номер выбранного дня в неделе

    day_to_str = edit_date_number(selected_day.day) + "/" + edit_date_number(selected_day.month) + "/" + str(
        selected_day.year)
    result = "*Расписание на " + type_of_day.lower() + " (" + day_to_str + ")" + ":*\n"

    if current_day_of_week == 6:
        return result + "Выходной день 😘"

    current_schedule = get_selected_day_schedule(current_day_of_week, current_type, view_type)

    if current_schedule == "":
        result = result + "Выходной день 😘"
    else:
        result = result + current_schedule

    return result


# Возвращает расписание на неделю
def get_week_schedule(type_week: str, view_type):
    current_type = define_type_of_current_week(datetime.datetime.today())
    result: str = ""

    if type_week == "Следующая":
        current_type = not current_type

    for i in range(6):
        timetable = get_selected_day_schedule(i, current_type, view_type)
        if timetable != "":
            result = result + emoji[i] + " *" + days_of_week[i] + "* \n" + timetable + "\n\n"

    return result


def type_of_week():
    today = datetime.datetime.today()
    result = define_type_of_current_week(today)

    if result:
        return "Текущая - четная неделя"
    else:
        return "Текущая - нечетная неделя"


def full_view_type(item: ClassItem, group: str):
    class_full: str

    time_period = "⏰ _" + item.time_range + "_"
    class_name = edit_string("🖍 " + item.class_name)
    class_type = "(" + item.class_type + ")"
    location = "🏫 " + item.location

    count = len(class_name + class_type)

    if count >= 33:
        class_full = space + class_name + "\n" + space + class_type + "\n"
    else:
        class_full = space + class_name + " " + class_type + "\n"

    result = "\n" + space + time_period + "\n" + class_full + space + location + "\n" + space + group + "\n"

    return result


def short_view_type(item: ClassItem, group: str):
    result = "\n⏰ " + item.time_range + "  -  " + item.class_name + " (" + item.class_type + ")\n" \
                                                                                             "🏫 " + item.location + " (" + group + ")" + "\n"
    return result


def edit_string(text: str):
    count = len(text)
    if count > 33:
        index = text.find('; ') + 1
        first_part = text[0:index]
        second_part = text[index:count - 1]
        return first_part + "\n" + space + second_part
    else:
        return text


def edit_date_number(number: int):
    if number < 10:
        return "0" + str(number)
