# Мой дом на SprutHub

#### Api SH

В файле spruthub.py класс api:

```python3
sh = spruthub.api('<путь к серверу>')
sh.auth('<логин>', '<пароль>') # Возвращает токен
```

# Бот для простого доступа у файлам

#### Описание

Этот бот нужен для быстрого доступа к файлам на удаленном устройстве (на которых запущен этот бот). Это удобно когда вам нужно посмотреть логи, однако доступа к устройству нет, например сервер умного дома на даче. Бот позволяет прописать пути к нужным файлам и получать их по запросу. Также реализованна система авторизации с помощью токенов и аккаунта админа.

#### Запуск

Для запуска вам нужен python 3. Также необходимо установить библиотеки командой:

```bash
$ pip install telebot json secrets
```

Пропишите свой токен в поле "token" файла configBot.json и положите этот файл в папку configs/. (Если вы клоннировали репозиторий, он уже лежит в папке configs/)

Запустите бота:

```bash
$ python3 telegramBot.py
```

Отправьте /start от имени пользователя, которого вы хотите назначить администратором. Id, который вам придет впишите в configBot.json в "admin", "authedUsers" в "data" изменить ключ  123456 на нужный id. Например:

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
где 123456 ваше имя пользователя.

#### Использование

Отпраьте сообщение с любым текстом, чтобы получить меню бота

Для того, чтобы добавить нового пользователя нажмите "Создать новый токен". От имени аккаунта, который нужно добавить отправьте /auth, а потом токен.

Чтобы изменить название дома в приглашении измените значаение "homename" в конфиге
