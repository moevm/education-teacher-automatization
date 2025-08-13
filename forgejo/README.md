
# Forgejo скрипты

## grant_access_to_github_repo.py
Добавляет людей в коллабораторы репозитория. Есть возможность добавить как на чтение, так и на запись  
Примеры использования

Добавление пользователя suiciderabbit в репозиторий github.com/moevm/cs_lectures с правами только на чтение:  
`./grant_access_to_github_repo.py -g=moevm/cs_lectures:suiciderabbit -p True -t /path/to/token/file`  
Добавление пользователей suiciderabbit и pro100kot в репозиторий github.com/moevm/cs_lectures с правами на запись:  
`./grant_access_to_github_repo.py -g=moevm/cs_lectures:suiciderabbit,pro100kot -t /path/to/token/file`  

Добавление пользователей suiciderabbit и pro100kot в репозиторий github.com/moevm/cs_lectures с правами администратора:
`./grant_access_to_github_repo.py -g=moevm/cs_lectures:suiciderabbit,pro100kot -a True -t /path/to/token/file`  

## get_access_to_github_from_csv.py

TODO: перевести на работу с Forgejo

### Как получить токен
#### Токен через curl
Самый простой способ -- послать запос:
```bash
curl -X POST -H "Content-Type: application/json" -u <USER_NAME>:<PASSWORD> https://<HOST>/api/v1/users/<USER_NAME>/tokens -d '{"name":"<TOKEN_NAME>", "scopes": ["read:user", "write:repository"]}'
```
Подставьте:
+ USER_NAME -- имя пользователями [нужен еще и в ссылке -- будьте внимательны]
+ PASSWORD -- пароль пользователя
+ HOST -- домен, на котором равзернут Forgejo
+ TOKEN_NAME -- имя токена (должно быть уникальное)

Пример:

```bash
curl -X POST -H "Content-Type: application/json" -u kke:SOME_PASSWORD https://git.moevm.info/api/v1/users/kke/tokens -d '{"name":"token_name25", "scopes": ["read:user", "write:repository"]}'
```

#### Токен через WEB UI

https://{FORGEJO_HOST}/user/settings/applications -- перейдите по ссылке и выберите с какими провами будет токен.

### Что делать с токеном
Полученный токен положите в файл и укажите путь к нему, при запуске программы

### Доп настройки при смене домена

В util.py:
```py
FORGEJO_HOST = "git.moevm.info"
FORGEJO_API_BASE = f"https://{FORGEJO_HOST}/api/v1"
```

Заменить FORGEJO_HOST на актуальный домен.