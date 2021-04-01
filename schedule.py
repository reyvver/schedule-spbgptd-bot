import config
from schedule_models import *

table = config.gc.open_by_key(config.SHEET_KEY)

values: dict = {}  # Все значения, полученные из таблицы Excel
current_time: str = ""


# Загрузить все строчки из листа
def load_data_from_sheets():
    global values

    for current_sheet in table.worksheets():
        group_name = current_sheet.title
        current_values: List[List] = current_sheet.get_all_values()
        values[group_name] = current_values


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
def initialize_day_schedule(first_row_of_day: int, group_name: str):
    day_couples: List[ClassItemCouple] = []

    counter = first_row_of_day
    end = first_row_of_day + 11

    group_values = values[group_name]

    while counter < end:
        if (counter < len(group_values)) & (counter + 1 < len(group_values)):
            numerator = group_values[counter]
            denominator = group_values[counter + 1]
            day_couples.append(get_items_couple(numerator, denominator))

        counter = counter + 2

    return DaySchedule(class_couples=day_couples)


# Создание расписания недели
def initialize_week_schedule(group_name: str):
    row_number: int = 1  # Начинаем с первой строки
    days_schedule: List[DaySchedule] = []

    for i in range(6):
        days_schedule.append(initialize_day_schedule(row_number, group_name))
        row_number = row_number + 12  # Следующий день начинается через 12 строк

    return WeekSchedule(days_schedule=days_schedule)


load_data_from_sheets()
