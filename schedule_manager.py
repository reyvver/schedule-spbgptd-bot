import gspread
import config
import datetime
from schedule_models import *

gc = gspread.service_account()
table = gc.open_by_key(config.SHEET_KEY)
current_worksheet = table.sheet1

values: List[List] = []  # Все значения, полученные из таблицы Excel
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
emoji = ["\U0001F4D5", "\U0001F4D7", "\U0001F4D8", "\U0001F4D9", "\U0001F4D2", "\U0001F4D4"]

current_time: str = ""
schedule: WeekSchedule


######################################################

# Загрузить все строчки из листа
def load_data_from_sheet():
    global values
    values = current_worksheet.get_all_values()


# Четная или нечетная неделя, определяется относительно любого дня этой недели. week_type =
# true - четная неделя
# false - нечетная неделя
def define_type_of_current_week(day: datetime):
    number = day.isocalendar()[1]
    if number % 2 == 0:
        return False
    else:
        return True


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
    # global current_time

    day_couples: List[ClassItemCouple] = []

    counter = first_row_of_day
    end = first_row_of_day + 11

    while counter < end:
        if (counter < len(values)) & (counter + 1 < len(values)):
            # print(str(counter) + "   " + str(counter + 1))
            # current_time = ""
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
def refresh_data():
    load_data_from_sheet()
    initialize_schedule()


######################################################

# Возвращает строку со полями занятия: время занятия, название, аудитория и тд
def get_item(item: ClassItem):
    result: str = ""
    if item.class_name != "":  # Проверка есть ли в этот день какая-нибудь пара - у нее всегда есть название в таблице
        if item.group_index == "":
            result = "*• " + item.time_range + "* " + item.class_name + " (" + item.class_type + ") \n" + item.location + \
                      "\n*Общая*" + " \n\n"
        else:
            result = "*• " + item.time_range + "* " + item.class_name + " (" + item.class_type + ") \n" + item.location + \
                     "\n*" + item.group_index + " подгруппа * " + " \n\n"
    return result


# Возвращает расписание на выбранный день (включает проверку на четность / нечетность)
def get_selected_day_schedule(number: int, type_of_week: bool):
    current_schedule: DaySchedule = schedule.days_schedule[number]
    result: str = ""

    for couple in current_schedule.class_couples:
        if type_of_week:
            day = get_item(couple.denominator)  # Если четная - то знаменатель
        else:
            day = get_item(couple.numerator)  # Если нечетная - то числитель
        result = result + day

    return result


# Возвращает расписание на сегодня / завтра
def get_day_schedule(type_of_day: str):
    selected_day = datetime.datetime.today()  # Выбарнный день: сегодня или завтра
    current_type = define_type_of_current_week(selected_day)  # Тип недели относительно сегодня
    current_day_of_week = selected_day.weekday()  # Номер выбранного дня в неделе
    current_week_number = selected_day.isocalendar()[1]  # Номер текущей недели в календаре

    if type_of_day == "Завтра":
        selected_day = selected_day + datetime.timedelta(days=1)
        if selected_day.isocalendar()[1] != \
                current_week_number:  # Если сегодня воскресенье - то след день другая неделя по четности
            current_type = not current_type

    if current_day_of_week != 6:  # Если не воскресенье то
        result = get_selected_day_schedule(current_day_of_week, current_type)
        return result
    else:
        return "уихадноу"


# Возвращает расписание на неделю
def set_week_schedule(type_of_week: str):
    current_type = define_type_of_current_week(datetime.datetime.today())

    # if type_of_week == "Следующая":
    #     current_type = not current_type
    #
    # return current_type

    current_type = define_type_of_current_week(datetime.datetime.today())
    result: str = ""

    if type_of_week == "Следующая":
        current_type = not current_type

    for i in range(6):
        result = result + emoji[i] + " *" + days_of_week[i] + "* \n" + \
                 get_selected_day_schedule(i, current_type) + "\n\n"

    return result


def send_week_day(number: int, type_of_week):
    return emoji[number] + " *" + days_of_week[number] + "* \n" + \
                 get_selected_day_schedule(number, type_of_week) + "\n\n"

