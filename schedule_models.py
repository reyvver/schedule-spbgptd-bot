from typing import List


# Класс запись/срока/занятие
class ClassItem(object):
    def __init__(self, time_range, class_name, class_type, location, teacher=None, group_index=None):
        self.time_range = time_range
        self.group_index = group_index
        self.class_name = class_name
        self.class_type = class_type
        self.location = location
        self.teacher = teacher


# Класс записи на четную и нечетную неделю
class ClassItemCouple(object):
    def __init__(self, numerator=None, denominator=None):
        self.numerator: ClassItem = numerator
        self.denominator: ClassItem = denominator


# Расписание на день (состоит из массива записей)
class DaySchedule(object):
    def __init__(self, class_couples=None):
        self.class_couples: List[ClassItemCouple] = class_couples


# Расписание на неделю (состоит из массива дней)
class WeekSchedule(object):
    def __init__(self, days_schedule=None):
        self.days_schedule: List[DaySchedule] = days_schedule