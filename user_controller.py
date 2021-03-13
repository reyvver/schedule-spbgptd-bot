import database
from switch import *
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
def is_created():
    try:
        current_user
    except NameError:
        return False
    else:
        return True


def change_user_information(info: str, value):
    global current_user
    condition = "chat_id=" + str(current_user.chat_id)

    while Switch(info):
        if case("message_id"):
            current_user.message_id = value
            break
        if case("group_name"):
            current_user.group = value
            break
        if case("view_type"):
            current_user.view_type = value
            break

    values = {info: value}
    database.update_data("users", values, database.db_file, condition)


def reload_user(chat_id):
    global current_user
    user_db = database.get_user_data(chat_id, database.db_file, "*")
    current_user = User(user_db[0], user_db[2], user_db[3], user_db[4])


def check_message_id(new_message_id):
    if current_user.message_id != new_message_id:
        change_user_information("message_id", new_message_id)


def changing_group(new_group_name, new_message_id):
    change_user_information("group_name", new_group_name)
    change_user_information("message_id", new_message_id)


def set_user(chat_id, message_id):
    if is_created():
        return
    else:
        reload_user(chat_id)
        check_message_id(message_id)


def select_all_user():
    users = database.select_all_users()
    return users
