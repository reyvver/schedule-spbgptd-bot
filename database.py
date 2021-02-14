import sqlite3
import codecs
from sqlite3 import Error

db_file = 'schedule.db'
db_memory = ':memory:'
dbm_connection = sqlite3.connect(db_memory, check_same_thread=False)


def create_table(table_name: str, columns: str, database: str):
    sql_query = '''CREATE TABLE IF NOT EXISTS %s (%s);''' % (table_name, columns)
    post_sql_query(sql_query, database)
    # print("table '" + table_name + "' is created")


def delete_table(table_name: str, database: str):
    sql_query = ('''DROP TABLE %s''' % table_name)
    post_sql_query(sql_query, database)
    # print("table '" + table_name + "' is deleted")


def insert_data(table_name: str, values: [], database: str):
    result_values: str = ""

    for value in values:
        result_values += quote_identifier(value) + ","

    result_values = result_values[0:len(result_values) - 1]

    sql_query = ('''INSERT INTO %s VALUES(%s)''' % (table_name, result_values))
    post_sql_query(sql_query, database)

    # print("data was inserted in '" + table_name + "'")


def update_data(table_name: str, values: dict, database: str, condition=None):
    result_values: str = ""

    for key, value in values.items():
        if isinstance(value, str):
            sts = key + "='" + str(value) + "'"
        else:
            sts = key + '=' + str(value)
        result_values += quote_identifier(sts) + ","

    result_values = result_values[1:len(result_values) - 2]

    if condition is None:
        sql_query = ('''UPDATE %s SET %s''' % (table_name, result_values))
    else:
        sql_query = ('''UPDATE %s SET %s WHERE %s''' % (table_name, result_values, condition))

    post_sql_query(sql_query, database)


def check_existence(table_name: str, database: str):
    sql_query = '''SELECT name FROM sqlite_master WHERE type = "table" And name = "%s"''' % table_name
    result = post_sql_query(sql_query, database)

    if result is None:
        return False
    else:
        return True


# def prepare_condition(conditions):
#     result = ""
#
#     if len(conditions) > 1:
#         print("dfg")
#     else:
#         for condition in conditions:
#             result += '(' + condition + ') AND'
#


def post_sql_query(sql_query, database: str):
    if database == db_file:
        connection = sqlite3.connect(database, check_same_thread=False)
    else:
        connection = dbm_connection

    with connection:
        crs = connection.cursor()
        try:
            crs.execute(sql_query)
            connection.commit()
        except Error:
            pass
        result = crs.fetchall()
        return result


def register_user(chat_id, user_name, first_name, group_name):
    try:
        user_check_query = '''SELECT * FROM users WHERE chat_id = %d;''' % chat_id
        result = post_sql_query(user_check_query, db_file)

        if len(result) == 0:
            values = [chat_id, user_name, first_name, group_name, "full"]
            insert_data("users", values, db_file)
            if user_name is None:
                user_name = "Безымянный"
            print("пользователь " + user_name + " (" + str(chat_id) + ") добавлен")
        else:
            print("пользователь " + user_name + " сделал рестарт")

    except Error as e:
        print(e)
        pass


# https://gist.github.com/jeremyBanks/1083518
def quote_identifier(s, errors="strict"):
    try:
        encodable = s.encode("utf-8", errors).decode("utf-8")
    except AttributeError:
        encodable = repr(s).encode("utf-8", errors).decode("utf-8")

    nul_index = encodable.find("\x00")

    if nul_index >= 0:
        error = UnicodeEncodeError("utf-8", encodable, nul_index, nul_index + 1, "NUL not allowed")
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)

    return "\"" + encodable.replace("\"", "\"\"") + "\""


def select_all_users():
    sql_query = '''SELECT * FROM users'''
    return post_sql_query(sql_query, db_memory)


# # # ДОДЕЛАТЬ НАДО

def start_db():
    create_table("users", "chat_id INTEGER PRIMARY KEY NOT NULL, commands_count INTEGER", db_memory)


def reset_commands_count():
    values = {'commands_count': 0}
    update_data("users", values, db_memory)


def get_user_data(chat_id: int, item: str, database: str):
    sql_query = '''SELECT %s FROM users WHERE chat_id = %d''' % (item, chat_id)
    return post_sql_query(sql_query, database)[0][0]


start_db()


# def change_command_count(command_name):
#     sql_query = '''SELECT count FROM commands WHERE command = "%s"''' % command_name
#     number: int = post_sql_query(sql_query, db_file)[0][0] + 1
#     values = {"count": number}
#     update_data("commands", values, db_file, 'command="' + command_name + '"')


# create_table("users", "chat_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT, first_name TEXT", db_file)

# my_dict = {'a': 1, 'b': 2, 'c': 3}
# # print(my_dict.items())
# # key0, value0 = list(my_dict.items())[0]
# # print(key0)
# # print(value0)
# update_data("sdf", my_dict,"sdfg")

# "chat_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT, first_name TEXT"
# max_id = db.execute(
#     'SELECT max(%s) FROM %s where foo > ?' %(id_name, table_name),
#     (max_foo_value, ),
# )
# create_table("users", "chat_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT, first_name TEXT")
# sql_query = "SELECT * FROM users WHERE chat_id=378950106"
# print(post_sql_query(sql_query, db_file))
#
# sql_query = "SELECT * FROM userss WHERE commands_count=2222"
# print(post_sql_query(sql_query, db_file))
#
# sql_query = '''UPDATE userss SET commands_count=666 WHERE chat_id="HERT"'''
# print(post_sql_query(sql_query, db_file))
# create_table("userss", "chat_id INTEGER PRIMARY KEY NOT NULL, commands_count INTEGER", db_file)
# my_dict = {'commands_count': 0}
# number = 1
# update_data("userss", my_dict, db_file, "chat_id=" + str(number))
