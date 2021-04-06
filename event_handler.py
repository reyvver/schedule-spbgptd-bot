from switch import *
import user_controller
import strings
import schedule_controller
import tg_analytic

timetable = schedule_controller
user = user_controller


def timetable_handler(option, chat_id):
    result: str = ""

    view_type = user.user_data(chat_id, "view_type")
    group_name = user.user_data(chat_id, "group_name")

    while Switch(option):
        if case(strings.query_timetable[0]):
            result = timetable.get_day_schedule("Сегодня", view_type, group_name)
            break
        if case(strings.query_timetable[1]):
            result = timetable.get_day_schedule("Завтра", view_type, group_name)
            break
        if case(strings.query_timetable[2]):
            result = timetable.get_week_schedule("Текущая", view_type, group_name)
            break
        if case(strings.query_timetable[3]):
            result = timetable.get_week_schedule("Следующая", view_type, group_name)
            break

    return result


def change_group_handler(query):
    chat_id = query.message.chat.id

    if not user.is_created(chat_id):
        user_registration(query)
        return False
    else:
        user_change_group(query)
        return True


def view_type_handler(string, chat_id):
    result: str = strings.return_to_main_menu
    view_type: str

    if string == strings.query_view_type[0]:
        view_type = "full"
    else:
        view_type = "short"
    user.changing_view_type(chat_id, view_type)

    return result


def get_statistics(bot, txt, chat_id):
    st = txt.split(' ')
    if 'txt' in st or 'тхт' in st:
        tg_analytic.analysis(st, chat_id)
        with open('%s.txt' % chat_id, 'r', encoding='UTF-8') as file:
            bot.send_document(chat_id, file)
            tg_analytic.remove(chat_id)
    else:
        messages = tg_analytic.analysis(st, chat_id)
        bot.send_message(chat_id, messages)


def settings_handler(option):
    result: str = ""
    while Switch(option):
        if case(strings.query_settings[0]):
            result = strings.help_text
            break
        if case(strings.query_settings[1]):
            result = strings.start_text
            break
        if case(strings.query_settings[2]):
            result = strings.view_type_text
            break
        if case(strings.query_settings[3]):
            result = strings.return_to_main_menu
            break
    return result


def user_registration(query):
    user.initialise_user(query)


def user_change_group(query):
    user.changing_group(query.message.chat.id, query.data, query.message.message_id)


def user_select_message_id(chat_id):
    return user.user_data(chat_id, "message_id")


def user_send_to_all(bot, message_text):
    for usr in user.select_all_user():
        bot.send_message(
            usr[0],
            message_text
        )
