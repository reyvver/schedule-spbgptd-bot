import database


# Регистрация в БД и сохранение освновной инфы
def register_user_in_db(chat_id, user_name, group_name, message_id):
    database.register_user(chat_id, user_name, group_name, message_id)


# Внесенние в базу данных нового пользователя
def initialise_user(query):
    chat_id = query.message.chat.id

    user_name = query.message.chat.username
    group_name = query.data
    id_message = query.message.message_id

    register_user_in_db(chat_id, user_name, group_name, id_message)


# Получить определенные данные о пользователе
def user_data(chat_id, data: str):
    try:
        result = database.get_user_data(chat_id, database.db_file, data)[0]
    except TypeError:
        return "None"
    else:
        return result


# Проверить, был ли зарегистрирован пользователь ранее
def is_created(chat_id):
    result = user_data(chat_id, "message_id")

    if result == "None":
        return False
    else:
        return True


# Изменить пользовательскую инф-ию
def change_user_information(chat_id, info: str, value):
    condition = "chat_id=" + str(chat_id)
    values = {info: value}
    database.update_data("users", values, database.db_file, condition)


# Выбрать всех пользователь
def select_all_user():
    users = database.select_all_users()
    return users


# Изменить группу пользователя и идентификатор последнего сообщения
def changing_group(chat_id, new_group_name, new_message_id):
    change_user_information(chat_id, "group_name", new_group_name)
    change_user_information(chat_id, "message_id", new_message_id)


# Изменить тип отображение расписания
def changing_view_type(chat_id, value):
    change_user_information(chat_id, "view_type", value)
