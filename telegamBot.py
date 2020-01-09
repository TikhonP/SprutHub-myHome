from telebot import types, TeleBot, apihelper
import json
from secrets import token_hex

# Укажите путь к файлу конфигурации тут
configFileName = 'configs/configBot.json'


def read_config(config_file_name):
    with open(config_file_name) as json_file:
        config = json.load(json_file)
    return config


config = read_config(configFileName)
apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = TeleBot(config['token'])


def saveConfig(config, filename):
    with open(filename, 'w') as outfile:
        json.dump(config, outfile)


def exception(exception):
    for a in config['admin']:
        bot.send_message(a, "Ошибка!!!!")
        bot.send_message(a, exception)


@bot.message_handler(commands=['start'])
def start(msg):
    user = msg.chat.id
    if config['admin'] == []:
        bot.send_message(
            user, "Нет записи администратора для этого бота. Добавьте в 'admin' запись. Ваш пользователь:\n{}".format(user))
    else:
        if user in config['authedUsers']:
            if user in config['admin']:
                m = 'Вы зарегестрированны как Администратор.'
            else:
                m = 'Вы уже вощли в систему как пользователь.'
        else:
            m = 'Для получения доступа нажмите /auth'
        bot.send_message(
            user, "Этот бот нужен для контроля умного дома {}. {}".format(config['homename'], m))


@bot.message_handler(commands=['auth'])
def authantificate(msg):
    user = msg.chat.id
    config["data"][str(user)] = {"is_auth": True}
    saveConfig(config, configFileName)
    bot.send_message(user, "Для авторизации пришлите токен, выданный вам.")


@bot.message_handler(content_types=["text"])
def text(msg):
    text = msg.text
    user = msg.chat.id
    # print(text)
    # print(user)
    # print(config)
    try:
        if str(user) in config["data"]:
            if config["data"][str(user)]["is_auth"]:
                if text in config['authTokens']:
                    config['authedUsers'].append(user)
                    config['authTokens'].remove(text)
                    config["data"][str(user)]["is_auth"] = False
                    saveConfig(config, configFileName)
                    bot.send_message(user, "Вы авторизованны.")
                else:
                    bot.send_message(user, "Неверный токен.")
        if user in config['authedUsers']:
            if user in config['admin']:
                if config["data"][str(user)]['new_file_name']:
                    config['logs'][text] = None
                    config["data"][str(user)]['new_file_name'] = False
                    config["data"][str(user)]['new_file_path'][0] = True
                    config["data"][str(user)]['new_file_path'][1] = text
                    saveConfig(config, configFileName)
                    bot.send_message(user, "Введите путь к файлу")
                elif config["data"][str(user)]['new_file_path'][0]:
                    config['logs'][config["data"]
                                   [str(user)]['new_file_path'][1]] = text
                    config["data"][str(user)]['new_file_path'][0] = False
                    saveConfig(config, configFileName)
                    bot.send_message(user, "Файл добавлен")
                elif config["data"][str(user)]['is_edit'][0]:
                    config["data"][str(user)]['is_edit'][1] = text
                    config["data"][str(user)]['is_edit'][0] = False
                    saveConfig(config, configFileName)
                    keyboard = types.InlineKeyboardMarkup()
                    delet_log = types.InlineKeyboardButton(
                        text="Удалить файл", callback_data="delet_log")
                    editpath = types.InlineKeyboardButton(
                        text="Редактировать путь к файлу", callback_data="editpath")
                    keyboard.add(delet_log)
                    keyboard.add(editpath)
                    try:
                        bot.send_message(
                            user, config['logs'][text], reply_markup=keyboard)
                    except KeyError:
                        bot.send_message(user, 'Нет файла с таким именем (')
                else:
                    keyboard = types.InlineKeyboardMarkup()
                    gen_token = types.InlineKeyboardButton(
                        text="Создать новый токен", callback_data="gen_token")
                    clear_token = types.InlineKeyboardButton(
                        text="Сбросить все токены.", callback_data="clear_token")
                    get_logs = types.InlineKeyboardButton(
                        text="Получить логи", callback_data="get_logs")
                    add_log = types.InlineKeyboardButton(
                        text="Добавить файл", callback_data="add_log")
                    keyboard.add(add_log)
                    keyboard.add(get_logs)
                    keyboard.add(gen_token)
                    keyboard.add(clear_token)
                    bot.send_message(user, "Привет повелитель.",
                                     reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup()
                get_logs = types.InlineKeyboardButton(
                    text="Получить логи", callback_data="get_logs")
                keyboard.add(get_logs)
                bot.send_message(user, "Привет пользователь.",
                                 reply_markup=keyboard)
        else:
            bot.send_message(user, "Вы не авторизованны")
    except Exception as e:
        exception(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = call.message.chat.id
    try:
        if call.message:
            if call.data == "gen_token":
                new_token = token_hex(16)
                config['authTokens'].append(new_token)
                saveConfig(config, configFileName)
                bot.send_message(user,
                                 "Токен: \n {}".format(new_token))
            elif call.data == "clear_token":
                config['authTokens'] = []
                saveConfig(config, configFileName)
                bot.send_message(user, "Токены сброшенны")
            elif call.data == "get_logs":
                keyboard = types.InlineKeyboardMarkup()
                if config['logs'] != {}:
                    if user in config['admin']:
                        editLogs = types.InlineKeyboardButton(
                            text="Редактировать логи", callback_data="editLogs")
                        keyboard.add(editLogs)
                    for d in config['logs']:
                        l = types.InlineKeyboardButton(
                            text=d, callback_data=d)
                        keyboard.add(l)
                    bot.send_message(user, "Выберите файл",
                                     reply_markup=keyboard)
                else:
                    bot.send_message(user, "Нет добаленных файлов")
            elif call.data in config['logs']:
                try:
                    with open(config['logs'][call.data], 'rb') as f:
                        bot.send_document(user, f)
                except FileNotFoundError:
                    bot.send_message(user, "Нет такого файла на диске.")
            elif call.data == "add_log":
                config["data"][str(user)]['new_file_name'] = True
                saveConfig(config, configFileName)
                bot.send_message(user, "Отправьте название файла")
            elif call.data == "editLogs":
                config["data"][str(user)]['is_edit'][0] = True
                saveConfig(config, configFileName)
                bot.send_message(user, "Отправьте имя редактируемого файла: ")
            elif call.data == "delet_log":
                del config['logs'][config["data"][str(user)]['is_edit'][1]]
                saveConfig(config, configFileName)
                bot.send_message(user, "Файл {} удален".format(
                    config["data"][str(user)]['is_edit'][1]))
    except Exception as e:
        exception(e)


if __name__ == '__main__':
    bot.polling(none_stop=True)
