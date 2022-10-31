import config
import telebot
import keyboard_funks as kb
import output_funks as outf
import work_with_db as db


bot = telebot.TeleBot(token=config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    # #user_name and user_id will need to be entered into the database
    config.temporary_storage_of_received_data[message.from_user.id] = {}
    config.temporary_storage_of_received_data[message.from_user.id]['user_id'] = message.from_user.id

    try:
        if config.temporary_storage_of_received_data[message.from_user.id]["user_id"] == db.search_tuple_db(message.from_user.id)["user_id"]:   #Здесь будет проверка наличия анкеты у пользователя
            bot.send_message(message.chat.id, "Хотите перейти к просмотру анкет?", reply_markup=kb.menu_kb())
        else:   #добавляем user_id, user_name в бд
            config.temporary_storage_of_received_data[message.from_user.id]["user_name"] = str("@" + message.from_user.username)
            #    ...
            #     И переходим к регистрации, добавляя вводимые данные в бд
            start = bot.send_message(message.chat.id, "Создадим анкету (отправьте что угодно, чтобы начать)", reply_markup=kb.reg_kb())
            bot.register_next_step_handler(start, reg)
    except TypeError:

        config.temporary_storage_of_received_data[message.from_user.id]["user_name"] = str("@" + message.from_user.username)
            #    ...
            #     И переходим к регистрации, добавляя вводимые данные в бд
        start = bot.send_message(message.chat.id, "Создадим анкету (отправьте что угодно, чтобы начать)", reply_markup=kb.reg_kb())
        bot.register_next_step_handler(start, reg)

def reg(message):
    #Запрос пола
    fem_req = bot.send_message(message.chat.id, "Выберите пол: М/Ж", 
        reply_markup=kb.switch_fem_kb())
    bot.register_next_step_handler(fem_req, femile)


def femile(message):
    #проверка на выход из функции и нан тайп
    try:
        if message.text.lower() == "начать" or message.text.lower() == "перезапуск" or message.text.lower() == "/start":
            restart = bot.send_message(message.chat.id, "Начнем?", reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart, reg)
            # bot.clear_step_handler(message)
            # 
        elif message.text.lower() == 'м' or message.text.lower() == 'ж':
            #save fem db
            config.temporary_storage_of_received_data[message.from_user.id]['user_sex'] = message.text
            
            #запрос фото
            photo_reqest = bot.send_message(message.chat.id, "Отправьте свое фото", 
                reply_markup=kb.restart_kb())
            bot.register_next_step_handler(photo_reqest, photo)
        else:
            restart = bot.send_message(message.chat.id, 
            'Вы ввели неизвестный пол, введите свой пол снова', 
            reply_markup=kb.switch_fem_kb())
            bot.register_next_step_handler(restart, femile)
    except AttributeError:
        restart = bot.send_message(message.chat.id, 
            'Вы ввели неизвестный пол, введите свой пол снова', 
            reply_markup=kb.switch_fem_kb())
        bot.register_next_step_handler(restart, femile)


def photo(message):
    try:
        if message.text.lower() == "перезапуск" or message.text.lower() == "/start":
            restart = bot.send_message(message.chat.id, "Начнем?", reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart, reg)
        else:
            restart_req = bot.send_message(message.chat.id, "Похоже, вы ввели не фото. Введите фото: ", 
            reply_markup=kb.restart_kb())
            bot.register_next_step_handler(restart_req, photo)
    except AttributeError:
        try:
            if message.photo[-1].file_id:
                config.temporary_storage_of_received_data[message.from_user.id]["img_path"] = message.photo[-1].file_id        
                
                #запрос имени для перехода на следующий шаг
                name_reqwest = bot.send_message(message.chat.id, "Введите свое имя: ")
                bot.register_next_step_handler(name_reqwest, name)
            else:
                restart_req = bot.send_message(message.chat.id, "Похоже, вы ввели не фото. Введите фото: ", reply_markup=kb.reg_kb())
                bot.register_next_step_handler(restart_req, photo)
        except TypeError:
            restart_req = bot.send_message(message.chat.id, "Похоже, вы ввели не фото. Введите фото: ", reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart_req, photo)        


def name(message):
    try:
        if message.text.lower() == "начать" or message.text.lower() == "перезапуск" or message.text.lower() == "/start":
            restart = bot.send_message(message.chat.id, "Начнем?", reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart, reg)
        elif len(message.text)<=255:
            config.temporary_storage_of_received_data[message.from_user.id]['name'] = message.text
            
            #Запрос возраста для перехода на следующий шаг
            age_req = bot.send_message(message.chat.id, "Введите возраст:",
                reply_markup=kb.restart_kb())
            bot.register_next_step_handler(age_req, age)
        else:
            restart = bot.send_message(message.chat.id, "Слишком длинное, введите покороче:", reply_markup=kb.restart_kb())
            bot.register_next_step_handler(restart, name)
    except (TypeError, AttributeError):
        restart = bot.send_message(message.chat.id, "Вы ввели неверный тип", reply_markup=kb.restart_kb())
        bot.register_next_step_handler(restart, name)


def age(message):
    try:
        if message.text.lower() == "начать" or message.text.lower() == "перезапуск" or message.text.lower() == "/start":
            restart = bot.send_message(message.chat.id, "Начнем?", reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart, reg)
        elif len(message.text)<=255:
            config.temporary_storage_of_received_data[message.from_user.id]['user_age'] = int(message.text)
            
            #Запрос года для регистрации на следующй шаг
            city_req = bot.send_message(message.chat.id, "Введите город:")
            bot.register_next_step_handler(city_req, city)
        else:
            restart = bot.send_message(message.chat.id, "Ого, да вы долгожитель. Пожалуйста введите возраст покороче")
            bot.register_next_step_handler(restart,  age)
    except (ValueError, AttributeError):
        restart = bot.send_message(message.chat.id, "Пожалуйста введите возраст в виде числа:")
        bot.register_next_step_handler(restart,  age)


def city(message):
    try:
        if message.text.lower() == "начать" or message.text.lower() == "перезапуск" or message.text.lower() == "/start":
            restart = bot.send_message(message.chat.id, "Начнем?", 
                reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart, reg)
        elif len(message.text)<=255:
            config.temporary_storage_of_received_data[message.from_user.id]["user_city"] = message.text

            #запрос инфы рассказа о себе
            info_req = bot.send_message(message.chat.id, "Расскажите о себе(не более 255 символов):")
            bot.register_next_step_handler(info_req, user_info)
        else:
            restart = bot.send_message(message.chat.id, 
                "Пожалуйста введите в виде текста город(не более 255 символов, считая пробелы)",
                reply_markup=kb.restart_kb())
            bot.register_next_step_handler(restart, city)
            pass
    except AttributeError:
        restart = bot.send_message(message.chat.id, 
            "Пожалуйста введите в виде текста город:",
            reply_markup=kb.restart_kb())
        bot.register_next_step_handler(restart, city)

def user_info(message):
    try:
        if message.text.lower() == "начать" or message.text.lower() == "перезапуск" or message.text.lower() == "/start":
            restart = bot.send_message(message.chat.id, "Начнем?", 
                reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart, reg)
        elif len(message.text) <= 255:
            config.temporary_storage_of_received_data[message.from_user.id]["user_info"] = message.text

            #отображение анкеты
            bot.send_photo(message.chat.id, config.temporary_storage_of_received_data[message.from_user.id]["img_path"],
                caption="Вот ваша анкета:\n{0}, {1}, {2}\n{3}".format(config.temporary_storage_of_received_data[message.from_user.id]["name"],
                    config.temporary_storage_of_received_data[message.from_user.id]["user_age"],
                    config.temporary_storage_of_received_data[message.from_user.id]["user_city"],
                    config.temporary_storage_of_received_data[message.from_user.id]["user_info"]),
                reply_markup=kb.after_reg_kb())
            
            #запрос, нравится или нет
            total_req = bot.send_message(message.chat.id, "Нравится?", reply_markup=kb.after_reg_kb()) #Bot send total anket and req. "Do u like it?"
            bot.register_next_step_handler(total_req, total)
        else:
            restart = bot.send_message(message.chat.id, 
            "Введите текс покороче (255 символов)",
            reply_markup=kb.restart_kb())
            bot.register_next_step_handler(restart, user_info)
    except AttributeError:
        restart = bot.send_message(message.chat.id, 
            "Похоже, вы ввели не текст, попробуйте снова",
            reply_markup=kb.restart_kb())
        bot.register_next_step_handler(restart, user_info)



def total(message):
    try:
        if message.text.lower() == "да":
            #загрузка в бд всех введенных данных пользователя
            db.insert_tuple_in_db(
                #добавь table_name 
                user_id=config.temporary_storage_of_received_data[message.from_user.id]['user_id'], 
                user_name=config.temporary_storage_of_received_data[message.from_user.id]['user_name'],
                user_sex=config.temporary_storage_of_received_data[message.from_user.id]['user_sex'], 
                img_path=config.temporary_storage_of_received_data[message.from_user.id]['img_path'], 
                name=config.temporary_storage_of_received_data[message.from_user.id]['name'], 
                user_age=config.temporary_storage_of_received_data[message.from_user.id]['user_age'], 
                user_city=config.temporary_storage_of_received_data[message.from_user.id]['user_city'], 
                user_info=config.temporary_storage_of_received_data[message.from_user.id]['user_info']
                )
            
            
            
            del config.temporary_storage_of_received_data[message.from_user.id]
            
            bot.send_message(message.chat.id, 
                "Хотите перейти к просмотру анкет?", 
                reply_markup=kb.menu_kb())
        elif message.text.lower() == "нет":
            restart = bot.send_message(message.chat.id, 
                "Создадим анкету (отправьте что угодно, чтобы начать)", 
                reply_markup=kb.reg_kb())
            bot.register_next_step_handler(restart, reg)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда", reply_markup=kb.reg_kb())
            bot.send_message(message.chat.id, 
                "Хотите перейти к просмотру анкет?", 
                reply_markup=kb.menu_kb())
            
    except Exception as ex:
        bot.send_message(message.chat.id, "Ошибка: {0}".format(ex), reply_markup=kb.reg_kb())
        print(ex)


@bot.message_handler(content_types=["text"])
def menu(message):
    try:
        if message.text.lower() == "смотреть анкеты":
            start_to_viewing_profiles_req = bot.send_message(message.chat.id, "Нажмите, чтобы начать", reply_markup=kb.reg_kb())
            bot.register_next_step_handler(start_to_viewing_profiles_req, viewing_profiles)
        elif message.text.lower() == "моя анкета":
            vie_my_profile = bot.send_photo(message.chat.id, outf.conclusion_of_the_questionnaire(db.search_tuple_db(message.from_user.id))[0],
                caption="Вот ваша анкета: {0}".format(outf.conclusion_of_the_questionnaire(db.search_tuple_db(message.from_user.id))[1], 
                reply_markup=kb.menu_kb()))
            bot.register_next_step_handler(vie_my_profile, menu)
        elif message.text.lower() == "удали мою анкету":
            are_u_sure_req = bot.send_message(message.chat.id, 
                "Вы уверенны, что хотите удалить свою анкету",
                reply_markup=kb.after_reg_kb())
            bot.register_next_step_handler(are_u_sure_req, del_or_no)
            
        else:
            pass
    except AttributeError:
        restart = bot.send_message(message.chat.id, 
            "Похоже, вы ввели не текст, попробуйте снова",
            reply_markup=kb.restart_kb())
        bot.register_next_step_handler(restart, menu)
def viewing_profiles(message):
    pass

def del_or_no(message):
    try:
        if message.text.lower() == "да":
            db.delete_tuple_db("user_id", message.from_user.id)
            bot.send_message(message.chat.id, 
                "Ваша анкета успешно удалена",
                reply_markup=kb.default())
        elif message.text.lower() == "нет":
            bot.send_message(message.chat.id, 
                "Действие отменено",
                reply_markup=kb.menu_kb())
        else:
            bot.send_message(message.chat.id, 
                "Неизвестный ответ",
                reply_markup=kb.menu_kb())
    except AttributeError:
        restart = bot.send_message(message.chat.id, 
            "Похоже, вы ввели не текст, попробуйте снова, хотите ли вы удалить свою анкету",
            reply_markup=kb.after_reg_kb())
        bot.register_next_step_handler(restart, del_or_no)

bot.polling(none_stop=True, interval=1, timeout=123)

