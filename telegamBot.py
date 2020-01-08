import telebot
from telebot import types
import json
from secrets import token_hex
import spruthub


configFileName = 'configs/configBot.json'


def read_config(config_file_name):
    with open(config_file_name) as json_file:
        config = json.load(json_file)
    return config


config = read_config(configFileName)
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(config['token'])

auth = False


def saveConfig(config, filename):
    with open(filename, 'w') as outfile:
        json.dump(config, outfile)


@bot.message_handler(commands=['start'])
def start(msg):
    user = msg.chat.id
    bot.send_message(
        user, "Этот бот нужен для контроля умного дома DublDom. Для получения доступа нажмите /auth")


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
    print(text)
    print(user)
    print(config)
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
                config['logs'][config["data"][str(user)]['new_file_path'][1]] = text
                config["data"][str(user)]['new_file_path'][0] = False
                saveConfig(config, configFileName)
                bot.send_message(user, "Файл добавлен")
            else:
                keyboard = types.InlineKeyboardMarkup()
                gen_token = types.InlineKeyboardButton(
                    text="Создать новый токен", callback_data="gen_token")
                clear_token = types.InlineKeyboardButton(
                    text="Сбросить все токены.", callback_data="clear_token")
                get_logs = types.InlineKeyboardButton(
                    text="Получить логи", callback_data="get_logs")
                add_log = types.InlineKeyboardButton(text="Добавить файл", callback_data="add_log")
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


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = call.message.chat.id
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
            for d in config['logs']:
                l = types.InlineKeyboardButton(
                    text=d, callback_data=d)
                keyboard.add(l)
            bot.send_message(user, "Выберите файл", reply_markup=keyboard)
        elif call.data in config['logs']:
            bot.send_document(user, open(config['logs'][call.data], 'rb'))
        elif call.data == "add_log":
            config["data"][str(user)]['new_file_name'] = True
            saveConfig(config, configFileName)
            bot.send_message(user, "Отправьте название файла")


if __name__ == '__main__':
    bot.polling(none_stop=True)
