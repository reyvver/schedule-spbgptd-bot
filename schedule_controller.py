from schedule_models import *
import schedule
import datetime
import strings


# Четная или нечетная неделя, определяется относительно любого дня этой недели. week_type =
# true - четная неделя
# false - нечетная неделя
def define_type_of_current_week(day: datetime):
    number = day.isocalendar()[1]
    if number % 2 == 0:
        return True
    else:
        return False


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
def get_selected_day_schedule(number: int, type_week: bool, view_type, group_name):
    timetable: WeekSchedule = schedule.initialize_week_schedule(group_name)

    current_schedule: DaySchedule = timetable.days_schedule[number]
    result: str = ""

    for couple in current_schedule.class_couples:
        if type_week:
            day = get_item(couple.denominator, view_type)  # Если четная - то знаменатель
        else:
            day = get_item(couple.numerator, view_type)  # Если нечетная - то числитель

        result = result + day

    return result


def get_day_schedule(type_of_day: str, view_type, group_name):
    if type_of_day == "Сегодня":
        selected_day = datetime.datetime.today()
    else:
        selected_day = datetime.datetime.today() + datetime.timedelta(days=1)

    day_to_str = strings.edit_date_number(selected_day.day) + "/" + strings.edit_date_number(
        selected_day.month) + "/" + str(selected_day.year)

    result = "*Расписание на " + type_of_day.lower() + " (" + day_to_str + ")" + ":*\n"

    current_day_number = selected_day.weekday()

    if current_day_number == 6:
        return result + "\nВыходной день 😘"

    current_week_type = define_type_of_current_week(selected_day)
    current_schedule = get_selected_day_schedule(current_day_number, current_week_type, view_type, group_name)

    if current_schedule == "":
        return result + "\nВыходной день 😘"

    return result + current_schedule


# Возвращает расписание на неделю
def get_week_schedule(type_week: str, view_type, group_name):
    current_type = define_type_of_current_week(datetime.datetime.today())
    result: str = ""

    if type_week == "Следующая":
        current_type = not current_type

    for i in range(6):
        day_timetable = get_selected_day_schedule(i, current_type, view_type, group_name)
        if day_timetable != "":
            result = result + strings.emoji[i] + " *" + strings.days_of_week[i] + "* \n" + day_timetable + "\n\n"

    return result


def full_view_type(item: ClassItem, group: str):
    class_full: str

    time_period = "⏰ _" + item.time_range + "_"
    class_name = strings.edit_string("🖍 " + item.class_name)
    class_type = "(" + item.class_type + ")"
    location = "🏫 " + item.location

    count = len(class_name + class_type)

    if count >= 33:
        class_full = strings.space + class_name + "\n" + strings.space + class_type + "\n"
    else:
        class_full = strings.space + class_name + " " + class_type + "\n"

    result = "\n" + strings.space + time_period + "\n" + class_full + strings.space + location + "\n" + strings.space \
             + group + "\n"

    return result


def short_view_type(item: ClassItem, group: str):
    result = "\n⏰ *" + item.time_range + "*  -  " + item.class_name + " (" + item.class_type + ")\n " \
             + strings.space + item.location + " (" + group + ")" + ""
    return result


def type_of_week():
    today = datetime.datetime.today()
    result = define_type_of_current_week(today)

    if result:
        return "Текущая - четная неделя"
    else:
        return "Текущая - нечетная неделя"
