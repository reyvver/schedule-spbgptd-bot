import gspread
import config
from schedule_models import *

gc = gspread.service_account()
table = gc.open_by_key(config.SHEET_KEY)
current_worksheet = table.sheet1

values: List[List] = []
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
current_time: str
schedule: WeekSchedule


######################################################

# Загрузить все строчки из листа
def load_data_from_sheet():
    global values
    values = current_worksheet.get_all_values()


# Создать запись
def initialize_item(current_row: List):
    global current_time

    if current_time == "":
        current_time = current_row[1]

    row_time = current_time
    if current_row[2] != "":
        row_time = current_row[2]

    return ClassItem(
        time_range=row_time,
        group_index=current_row[3],
        class_name=current_row[4],
        class_type=current_row[5],
        location=current_row[6],
        teacher=current_row[7]
    )


# Получение 1 пары (нечетная/четная) и ее создание
def get_items_couple(numerator_row: List, denominator_row: List):
    return ClassItemCouple(
        numerator=initialize_item(numerator_row), denominator=initialize_item(denominator_row)
    )


# Получение расписания на день. У каждого дня 12 строчек
def initialize_day_schedule(first_row_of_day: int):
    global current_time
    day_schedule: List[ClassItemCouple] = []
    counter = first_row_of_day
    while counter < 13:
        current_time = ""
        numerator = values[counter]
        denominator = values[counter + 1]
        day_schedule.append(get_items_couple(numerator, denominator))
        counter = counter + 2
    return DaySchedule(
        class_couples=day_schedule
    )


# Получение расписания недели
def initialize_week_schedule():
    row_number: int = 1
    days_schedule: List[DaySchedule] = []
    for i in range(6):
        days_schedule.append(initialize_day_schedule(row_number))
        row_number = row_number + 12
    return WeekSchedule(
        days_schedule=days_schedule
    )


def print_selected_item(item: ClassItem):
    print(
        item.time_range + "  " + item.group_index + "  " + item.class_name + "  " + item.class_type + "  " + item.location + "   " + item.teacher)


def print_selected_day(number: int):
    current_schedule: DaySchedule = schedule.days_schedule[number]
    print("Выбранный день  " + days_of_week[number])

    for i in range(len(current_schedule.class_couples)):
        current_couple: ClassItemCouple = current_schedule.class_couples[i]
        print_selected_item(current_couple.numerator)
        print_selected_item(current_couple.denominator)


load_data_from_sheet()
schedule = initialize_week_schedule()
print_selected_day(0)
# global current_day_of_week
# current_day_of_week = day_of_week[i]


# load_data_from_sheet()
# for i in range(12):
#     print(i)

# for i in range(len(values[2])):
#     print(i)
#     print(values[2][i])
#
# week_schedule: WeekSchedule
#
#
# # Забрать расписание из облака
# def update_schedule_from_cloud():
#     global week_schedule
#     week_schedule = load_week_schedule()
#
#
# # Возвращает ClassItem
# def load_class_item(cell_number: int):
#     class_data = table.sheet1.range('B{0}:H{0}'.format(cell_number))
#
#     class_item = ClassItem(time_range=class_data[0].value,
#                            group_index=class_data[2].value,
#                            class_name=class_data[3].value,
#                            class_type=class_data[4].value,
#                            location=class_data[5].value,
#                            teacher=class_data[6].value)
#
#     extra_time_range = class_data[1].value
#     if extra_time_range != "":
#         class_item.time_range = extra_time_range
#
#     if class_item.time_range == "":
#         time_index = cell_number - 1
#         class_item.time_range = table.sheet1.get("B" + str(time_index)).first()
#
#     return class_item
#
#
# # Возвращает пару для четной и нечетной недели
# def load_class_couple(cell_number: int):
#     even = load_class_item(cell_number)
#     odd = load_class_item(cell_number + 1)
#
#     return ClassItemCouple(even, odd)
#
#
# # Возвращает расписание на день
# def load_day_schedule(day_number: int):
#     day_schedule: DaySchedule = DaySchedule()
#
#     i = 2 + ((day_number - 1) * 12)
#     print("i: " + str(i))
#     target = i + 12
#     print("target: " + str(target))
#
#     while i < target:
#         day_schedule.class_couples.append(load_class_couple(i))
#         i += 2
#
#     return day_schedule
#
#
# #  Возвращает расписание на неделю
# def load_week_schedule():
#     return WeekSchedule(
#         monday=load_day_schedule(1),
#         tuesday=load_day_schedule(2),
#         wednesday=load_day_schedule(3),
#         thursday=load_day_schedule(4),
#         friday=load_day_schedule(5),
#         saturday=load_day_schedule(6)
#     )

#####################################################
