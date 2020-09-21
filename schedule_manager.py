import gspread
import config
import datetime
from schedule_models import *

gc = gspread.service_account()
table = gc.open_by_key(config.SHEET_KEY)
current_worksheet = table.sheet1

values: List[List] = []
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
emoticons_books = ["\U0001F4D5", "\U0001F4D7", "\U0001F4D8", "\U0001F4D9", "\U0001F4D2", "\U0001F4D4"]
# emoticons_books = [":closed_book:", ":green_book:", ":blue_book:", ":orange_book:", ":ledger:", "U+1F4D4"]
current_time: str = ""
schedule: WeekSchedule
week_type: bool


######################################################

# Загрузить все строчки из листа
def load_data_from_sheet():
    global values
    values = current_worksheet.get_all_values()


# Четная или нечетная неделя
# true - четная
# false - нечетная
def type_of_current_week():
    global week_type
    number = datetime.datetime.today().isocalendar()[1]
    if number % 2 == 0:
        print("нечетная")
        week_type = False
    else:
        print("четная")
        week_type = True



# Создать запись
def initialize_item(current_row: List):
    global current_time

    if current_row[1] != "":
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
    global values
    global current_time
    day_schedule: List[ClassItemCouple] = []
    counter = first_row_of_day
    end = first_row_of_day + 11

    while counter < end:
        if (counter < len(values)) & (counter + 1 < len(values)):
            # print(str(counter) + "   " + str(counter + 1))
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
    global schedule
    row_number: int = 1
    days_schedule: List[DaySchedule] = []

    for i in range(6):
        days_schedule.append(initialize_day_schedule(row_number))
        row_number = row_number + 12

    schedule = WeekSchedule(days_schedule=days_schedule)
    # return WeekSchedule(
    #     days_schedule=days_schedule
    # )


# Возвращает строку со полями дня
def get_day(item: ClassItem):
    result: str = ""
    if item.class_name != "":
        # result = item.time_range + " " + item.class_name + " (" + item.class_type + ") \n" + item.location + \
        #          "\nПреподаватель:" + item.teacher + " \n\n"
        result = "*• " +item.time_range + "* " + item.class_name + " (" + item.class_type + ") \n" + item.location + \
                 "\nПреподаватель:" + item.teacher + " \n\n"
    return result


# Печать расписания на выбранный день (включает проверку на четность / нечетность
def print_selected_day(number: int):
    global week_type
    current_schedule: DaySchedule = schedule.days_schedule[number]
    result: str = ""

    for i in range(len(current_schedule.class_couples)):
        current_couple: ClassItemCouple = current_schedule.class_couples[i]
        day: str = ""
        if week_type:
            day = get_day(current_couple.denominator)
        else:
            day = get_day(current_couple.numerator)
        result = result + day
    return result


# Печать расписания на сегодня / завтра
def print_day_schedule(type_of_day: str):
    global week_type
    current_type = week_type
    current_week_number = datetime.datetime.today().isocalendar()[1]
    day: datetime.date = datetime.datetime.today()

    if type_of_day == "завтра":
        day = day + datetime.timedelta(days=1)
        number = day.isocalendar()[1]
        if number != current_week_number:
            week_type = not week_type

    day_of_week: int = day.weekday()

    if day_of_week != 6:
        result = print_selected_day(day_of_week)
        if week_type != current_type:
            week_type = current_type
        return result
    else:
        return "уухадноу"


def print_week_schedule(type_of_week: str):
    global week_type
    current_type = week_type
    result: str = ""

    if type_of_week == "следующая":
        week_type = not week_type

    for i in range(6):
        result = result + emoticons_books[i] + " *" + days_of_week[i] + "* \n" + print_selected_day(i) + "\n\n"

    week_type = current_type
    return result


# Начало работы с данными
def on_start_schedule():
    load_data_from_sheet()
    initialize_week_schedule()
    type_of_current_week()

# on_start_schedule()
# print(print_day_schedule("сегодня"))
