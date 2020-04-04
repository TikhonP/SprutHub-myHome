# Библиотека Api SH

В файле `spruthub.py` класс api:

```python3
sh = spruthub.api('<путь к серверу>')
sh.auth('<логин>', '<пароль>') # Возвращает токен
```

# Подключение ламп philips и yeelight к spruthub
#### Установка python и библиотек:

Склонируйте репозиторий
```bash
git clone https://github.com/TikhonP/SprutHub-myHome.git
cd SprutHub-myHome
```

Проверено на python3.7 и выше.
[Установка python3.8 на raspberry pi](https://installvirtual.com/how-to-install-python-3-8-on-raspberry-pi-raspbian/)
[Установка на другие устройства](https://python.org)

Проверьте стоит ли `pip`
Установка `pip3` на raspberry
```bash
$ sudo apt-get install python3-pip
$ sudo apt-get install libffi-dev libssl-dev # Для python-miio
```
Установка библиотек
```bash
$ python3 -m pip install -r req.txt # Вместо python3 ваш python (например python3.7)
```

#### Настройка
Отредактируйте файл настройки `vim configs/blubs_config.json`
Введите данные сервера sh

```json
  "sh_server": {
    "url": "ip:55555",
    "login": "<login>",
    "password": "<pass>"
  },
```

Уменьшите это значение если хотите меньшей задержки

```json
  "interval": 1,
```
###### Yeelight
Discovery оставьте включенным если у вас одна лампа yeelight
Для каждого устройства нобходимя виртуальные лампы. Их параметры задаются здесь. Для цветного устройства yeelight надо включить `яркость` `тон` `насыщенность` `цветовая температура`
Sh_aid - Параметры устройства в sh `[accessoryid, characteristicid (state), cid(color_temp), cid(value), cid(saturation), cid(hue)]`
Bulbs (ip, port) оставить так, если только одна лампа  yeelight

```json
  "yeelight": {
    "discovery": true,
    "sh_aid": [
      [46, 12, 16, 13, 15, 14]
    ],
    "bulbs": [{
      "ip": "ip",
      "port": "port"
    }]
  },
```
###### Philips
Также виртуальные устройства в sh для ламп philips. Опциональные характеристики `яркость` `цветовая температура`
Sh_aid - `[aid, on/off, colorTemp, brightness]`
Перечислите все лампы таким образом
bulbs ip, token для каждой лампы в той же последовательности
```json
  "philips": {
    "comment": "в sh_aid - [aid, on/off, colorTemp, brightness]",
    "sh_aid": [
      [47, 12, 14, 13]
      [50, 12, 14, 13]
    ],
    "bulbs": [{
        "ip": "192.168.31.70",
        "token": "9A6FEBD4E55F743C01074EA005CD57BD"
      },
      {
        "ip": "192.168.31.23",
        "token": "3d48e0597e7a346489fe08101e02c61f"
      }
    ]
  }
```

#### Запуск
Протестируйте скрипт
```bash
python3 blubs_sh.py
```

Для запуска я использую
```bash
nohup python3 blubs_sh.py &> bulbs.log&
```



# Бот для простого доступа к файлам

#### Описание

Этот бот нужен для быстрого доступа к файлам на удаленном устройстве (на которых запущен этот бот). Это удобно когда вам нужно посмотреть логи, однако доступа к устройству нет, например сервер умного дома на даче. Бот позволяет прописать пути к нужным файлам и получать их по запросу. Также реализованна система авторизации с помощью токенов и аккаунта админа.

#### Запуск

Для запуска вам нужен python 3. Также необходимо установить библиотеки командой:

```bash
$ pip install telebot json secrets
```

Пропишите свой токен в поле `token` файла `configBot.json` и положите этот файл в папку `configs/`. (Если вы клоннировали репозиторий, он уже лежит в папке `configs/`)

Запустите бота:

```bash
$ python3 telegramBot.py
```

Отправьте `/start` от имени пользователя, которого вы хотите назначить администратором. Id, который вам придет впишите в `configBot.json` в `admin`, `authedUsers` в `data` изменить ключ  `123456` на нужный id. Например:

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

где `123456` ваше имя пользователя.

#### Использование

Отпраьте сообщение с любым текстом, чтобы получить меню бота

Для того, чтобы добавить нового пользователя нажмите `Создать новый токен`. От имени аккаунта, который нужно добавить отправьте `/auth`, а потом токен.

Чтобы изменить название дома в приглашении измените значаение `homename` в конфиге
