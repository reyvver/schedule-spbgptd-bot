import database
from user_models import *

current_user: User


# ===========================================================================================================РЕГИСТРАЦИЯ
# Регистрация в БД и сохранение освновной инфы
def register_user_in_db(chat_id, user_name, group_name, message_id):
    database.register_user(chat_id, user_name, group_name, message_id)


# Создаем экземпляр класса User, чтобы не обращаться к БД и не считывать данные тысячу раз
def create_current_user(chat_id, message_id, group, view_type):
    global current_user
    new_user: User = User(chat_id, group, view_type, message_id)
    current_user = new_user


# Создаем и сохраняем инф-ию пользователя в первый раз (аля регистрация)
def initialise_user(query):
    chat_id = query.message.chat.id

    user_name = query.message.chat.username
    group_name = query.data
    id_message = query.message.message_id

    register_user_in_db(chat_id, user_name, group_name, id_message)
    create_current_user(chat_id, id_message, group_name, "full")


# ===========================================================================================================БАЗА ДАННЫХ
def check_user_existence():
    try:
        current_user
    except NameError:
        return False
    else:
        return True


def change_user_information(info: str, value):
    condition = "chat_id=" + str(current_user.chat_id)
    values = []

    while Switch(info):
        if case("message_id"):
            values = {info: value}
            current_user.message_id = value
            break

        if case("group"):
            break
        if case("view_type"):
            break

    database.update_data("users", values, database.db_file, condition)


def reload_user(chat_id):
    global current_user
    user_db = database.get_user_data(chat_id, database.db_file, True)
    current_user = User(user_db[0], user_db[2], user_db[3], user_db[4])


# ================================================================================================================ДРУГОЕ

class Switch(object):
    value = None

    def __new__(cls, value):
        cls.value = value
        return True


def case(*args):
    return any((arg == Switch.value for arg in args))
