import config
from schedule_models import *

table = config.gc.open_by_key(config.SHEET_KEY)

values: List[List] = []  # Все значения, полученные из таблицы Excel
current_time: str = ""


# Загрузить все строчки из листа
def load_data_from_sheet(group_name: str):
    global values
    current_worksheet = table.worksheet(group_name)
    values = current_worksheet.get_all_values()


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


# Считываем данные из таблицы Excel и присваиваем переменным значения
def refresh_data(group_name: str):
    load_data_from_sheet(group_name)
