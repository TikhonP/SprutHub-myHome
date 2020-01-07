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
    bot.send_message(user, "Для авторизации пришлите токен, выданный вам.")
    auth = True


@bot.message_handler(content_types=["text"])
def text(msg):
    text = msg.text
    user = msg.chat.id
    if auth:
        if text in config['authTokens']:
            config['authedUsers'].append(user)
            saveConfig(config, configFileName)
            config['authTokens'].remove(text)
            bot.send_message(user, "Вы авторизованны.")
        else:
            bot.send_message(user, "Неверный токен.")
    elif user in config['authedUsers']:
        if user in config['admin']:
            keyboard = types.InlineKeyboardMarkup()
            gen_token = types.InlineKeyboardButton(
                text="Создать новый токен", callback_data="gen_token")
            clear_token = types.InlineKeyboardButton(
                text="Сбросить все токены.", callback_data="clear_token")
            keyboard.add(gen_token)
            keyboard.add(clear_token)
            bot.send_message(user, "Привет повелитель.", reply_markup=keyboard)
        else:
            bot.send_message(user, "Привет пользователь.")


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

def mainLoop():
    shconf = read_config('configs/bulbs_config.json')
    sh = spruthub.api(config['sh_server']['url'])
    t = sh.auth(config['sh_server']['login'], config['sh_server']['password'])
    state = None
    while True:
        now = sh.listOfAllCharacteristicsOfOneServiceAndAccessory(29, 10)[0]['value']
        if state != now:
            for u in config['authedUsers']:
                bot.send_message(u, "Движение  {}".format(state))

if __name__ == '__main__':
    bot.polling(none_stop=True)
