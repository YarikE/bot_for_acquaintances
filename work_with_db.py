import random
import pymysql
from config import db_name, host, password, user

"""
ФУНКЦИИ:

***********************************************************************************************************************************************************************************

1. check_table(table_name) - вывод всей таблицы в консоль 
    Аргументы:
        1. table_name - название таблицы

***********************************************************************************************************************************************************************************

2. random_full_user_info(table_name, self_int_user) - функция возвращает РАНДОМНЫЙ элемент из таблицы
    Аргументы:
        1. table_name - название таблицы
        2. self_int_user - значение ячейки int_user пользователя

***********************************************************************************************************************************************************************************

3. insert_tuple_in_db(table_name, user_id, user_name, img_path, name, user_age, user_city, user_info) - Добавление кортежа (строки) в таблицу
    Аргументы:
        1. table_name - название таблицы
        2. user_id - ID в телеграмме (984453688)
        3. user_name - имя в телеграмме (@SymPy69) 
        4. img_path - путь к картинке в анкете
        5. name - имя в анкете
        6. user_age - возраст в анкете
        7. user_city - город в анкете
        8. user_info - иформация о себе в анкете 

***********************************************************************************************************************************************************************************

4. delete_tuple_db(table_name, delete_value, delete_cur_value) - Удаление кортежа (строки) из таблицы
    Аргументы:
        1. table_name - название таблицы
        2. delete_value - имя столбца по которому нужно удалить
        3. delete_cur_value - конкретное значение столбца

***********************************************************************************************************************************************************************************

"""


####### БЛОК ДЛЯ СОЗДАНИЯ ТАБЛИЦЫ В БД #######
#######         И ЕЕ ПРОВЕРКИ          #######

# try:
#     # connection
#     connection = pymysql.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=db_name,
#     cursorclass=pymysql.cursors.DictCursor
#     )
#     connection.autocommit = True

# # ##### СОЗДАНИЕ ТАБЛИЦЫ (1 РАЗ!!!)

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE acquaintaces_3(
    #             int_user INT PRIMARY KEY AUTO_INCREMENT,
    #             user_id INT,
    #             user_name VARCHAR(20),
    #             user_sex VARCHAR(10),
    #             img_path VARCHAR(250),
    #             name VARCHAR(50),
    #             user_age INT,
    #             user_city VARCHAR(50),
    #             user_info VARCHAR(250));"""
    #     )

# # список столбцов: int_user, user_id, user_name, user_sex, img_path, name, user_age, user_city, user_info, user_flag
# # пример картежа бд: 1, 905593527, '@SymPy', 'C:/user/1.png', 'Ярик', 18, 'Екб', 'Я занимаюсь тем-то и тем-то и мне скучно', 1

# # ПРОВЕРКА ТАБЛИЦЫ
#     # with connection.cursor() as cursor:
#     #     cursor.execute(
#     #         """SELECT * FROM acquaintaces_4"""
#     #     )
#     #     rows = cursor.fetchall()
#     #     for row in rows:
#     #         print(row['user_age'])
#     #     print('#' * 20)

# # exception block
# except Exception as _ex:
#     print('[info] Error', _ex)

# # finally block (closing all)
# finally:
#     if connection:
#         connection.close()


#### PRINT ТАБЛИЦЫ (ВСЕЙ) ####

def check_table(table_name='acquaintaces_3'):
# connection
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )


        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM {0}""".format(table_name)
            )
            rows = cursor.fetchall()
            print('#' * 20)
            for row in rows:
                print(row)
            print('#' * 20)
    except Exception as _ex:
        print('Функция для работы с БД (check_table) выдала ошибку{0}'.format(_ex))
    finally:
        if connection:
            connection.close()

# ФУНКЦИЯ ВЫВОДА РАНДОМНОГО КАРТЕЖА С ИСКУЛЮЧЕНИЕМ(НЕ ВЫВОДИТЬ СВОЙ КАРТЕЖ)

def random_full_user_info(self_int_user, table_name='acquaintaces_3'):
    try:
        # connection
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM {0} WHERE NOT int_user = {1}""".format(table_name, self_int_user))
            rows = cursor.fetchall()
            random_int_user = random.choice([x for x in range(1, len(rows)) if x != self_int_user])
            for row in rows:
                if row['int_user'] == random_int_user:
                    return row
    # exception 
    except Exception as _ex:
        print('Функция для работы с БД (random_full_user_info) выдала ошибку: {0}'.format(_ex))
    # finally (close connection)
    finally:
        if connection:
            connection.close()

######## ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ КОРТЕЖА В БД ########
# # пример кортежа бд: 1, 905593527, '@SymPy', 'C:/user/1.png', 'Ярик', 18, 'Екб', 'Я занимаюсь тем-то и тем-то и мне скучно'

def insert_tuple_in_db(user_id, user_name, user_sex, img_path, name, user_age, user_city, user_info, table_name='acquaintaces_3'):
    try:
        # connection
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        # Запрос на добавление
        str_exe = "INSERT INTO {0}(`user_id`, `user_name`, `user_sex`, `img_path`, `name`, `user_age`, `user_city`, `user_info`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name)
        with connection.cursor() as cursor:
            cursor.execute(str_exe, (user_id, user_name, user_sex, img_path, name, user_age, user_city, user_info))
            connection.commit()
    # except
    except Exception as _ex:
        print('Функция для работы с БД (insert_tuple_in_db) выдала ошибку: {0}'.format(_ex))

    # finally (close connection)
    finally:
        if connection:
            connection.close()


######## ФУНКЦИЯ ДЛЯ УДАЛЕНИЯ КАРТЕЖА / СТРОКИ В ТАБЛИЦУ ########

def delete_tuple_db(delete_value, delete_cur_value, table_name='acquaintaces_3'):
    try:
        # connection
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        # запрос на удаление
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM {0} WHERE {1} = {2};""".format(table_name, delete_value, delete_cur_value))
            connection.commit()

    # exception
    except Exception as _ex:
        print('Функция для работы с БД (delete_tuple_db) выдала ошибку: {0}'.format(_ex))

    # finally (close connection)
    finally:
        if connection:
            connection.close()


######## ФУНКЦИЯ ДЛЯ ВОЗВРАЩЕНИЯ КОРТЕЖА ИЗ ТАБЛИЦЫ ########

def search_tuple_db(search_cur_val, table_name='acquaintaces_3', search_val='user_id'):
    try:
        # connection
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        # запрос на удаление
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM {0} WHERE {1} = {2}""".format(table_name, search_val, search_cur_val))
            row = cursor.fetchone()
            return row
    # exception      
    except Exception as _ex:
        print('Функция для работы с БД (search_tuple_db) выдала ошибку: {0}'.format(_ex))
    # finally (close connection)
    finally:
        if connection:
            connection.close()


