# Мой дом на SprutHub

#### Библиотека Api SH

В файле spruthub.py класс api:

```python3
sh = spruthub.api('<путь к серверу>')
sh.auth('<логин>', '<пароль>') # Возвращает токен
```
#### Подключение ламп philips и yeelight к spruthub

Склонируйте репозиторий
```bash
git clone https://github.com/TikhonP/SprutHub-myHome.git
cd SprutHub-myHome
```
Отредактируйте файл настройки `vim configs/blubs_config.json`
```json
{
  "sh_server": {
    "url": "ip:55555", < ip address
    "login": "<login>",
    "password": "<pass>"
  },
  "interval": 1, < интервал проверки в секундах
  "yeelight": {
    "discovery": true, < оставьте включенным если у вас одна лампа yeelight
    "sh_aid": [
      [46, 12, 16, 13, 15, 14] < [aid, cid (state), cid(color_temp), cid(value), cid(saturation), cid(hue)]
    ],
    "bulbs": [{
      "ip": "ip",
      "port": "port" < оставить так, если одна лампа  yeelight
    }]
  },
  "philips": {
    "comment": "в sh_aid - [aid, on/off, colorTemp, brightness]",
    "sh_aid": [
      [47, 12, 14, 13], < [aid, on/off, colorTemp, brightness]
      [50, 12, 14, 13]
    ],
    "bulbs": [{
        "ip": "192.168.31.70", < ip лампы philips
        "token": "9A6FEBD4E55F743C01074EA005CD57BD" < токен
      },
      {
        "ip": "192.168.31.23",
        "token": "3d48e0597e7a346489fe08101e02c61f"
      }
    ]
  }
}
```

Запустите

```bash
python3 -m pip install -r req.txt
python3 blubs_sh.py
```


# Бот для простого доступа к файлам

#### Описание

Этот бот нужен для быстрого доступа к файлам на удаленном устройстве (на которых запущен этот бот). Это удобно когда вам нужно посмотреть логи, однако доступа к устройству нет, например сервер умного дома на даче. Бот позволяет прописать пути к нужным файлам и получать их по запросу. Также реализованна система авторизации с помощью токенов и аккаунта админа.

#### Запуск

Для запуска вам нужен python 3. Также необходимо установить библиотеки командой:

```bash
$ pip install telebot json secrets
```

Пропишите свой токен в поле "token" файла "configBot.json" и положите этот файл в папку "configs/". (Если вы клоннировали репозиторий, он уже лежит в папке `configs/`)

Запустите бота:

```bash
$ python3 telegramBot.py
```

Отправьте "/start" от имени пользователя, которого вы хотите назначить администратором. Id, который вам придет впишите в configBot.json в "admin", "authedUsers" в "data" изменить ключ  "123456" на нужный id. Например:

```json
...
"authedUsers": [123456],
"admin": [123456],
...
"data": {
  "123456": {
    "is_auth": false,
    "new_file_name": false,
    "new_file_path": [false, ""],
    "is_edit": [false, ""]
  }
},
...
```
где "123456" ваше имя пользователя.

#### Использование

Отпраьте сообщение с любым текстом, чтобы получить меню бота

Для того, чтобы добавить нового пользователя нажмите "Создать новый токен". От имени аккаунта, который нужно добавить отправьте "/auth", а потом токен.

Чтобы изменить название дома в приглашении измените значаение "homename" в конфиге
