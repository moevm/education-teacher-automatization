Скрипт для управления доступом к репозиториям в Forgejo

**Создание токенов**

**Для пользователя (через WEB UI):**
1. Залогиньтесь в Forgejo
2. Перейдите: **Настройки** → **Приложения** → **Сгенерировать новый токен**
3. Укажите имя токена
4. Выберите права:
	repo (обязательно)
	admin:org (для работы с организациями)
	write:org (для управления доступом)
5. Сохраните токен в файл

**Для бота:**
1. Аналогично как для пользователя
2. ```bash
	curl -X POST \
	-H "Content-Type: application/json" \
	-u <USERNAME>:<PASSWORD> \
	http://<FORGEJO_HOST>/api/v1/users/<USERNAME>/tokens \
	-d '{"name":"<TOKEN_NAME>", "scopes": ["repo", "write:org"]}'
   ```

Параметры:

USERNAME - имя пользователя (дважды - в аутентификации и URL)

PASSWORD - пароль пользователя

FORGEJO_HOST - актуальный домен

TOKEN_NAME - уникальное имя токена

scopes - права доступа (рекомендуемые: repo, write:org)


**Настройка организаций**

Создание организации через WEB UI:
1. **Профиль** → **Ваши организации** → **Создать организацию**
2. Заполните:
   - Название
   - Описание (опционально)
3. Нажмите **Создать организацию**

Создание организации через API:

```bash
curl -X POST -H "Authorization: token $(cat admintoken.txt)" \
-H "Content-Type: application/json" \
-d '{"username":"testorg", "description":"Test organization"}' 
\http://<FORGEJO_HOST>/api/v1/orgs
```
FORGEJO_HOST - должен быть актуальным доменом

Использование скрипта

Базовый синтаксис:
```bash
python3 grant_access_to_github_repo.py -t <token_file> [OPTIONS]
```

Опции:
`-t TOKEN` Путь к файлу с токеном (обязательно) `-t token.txt`

`-g SPEC` Добавить доступ `-g "org/repo:user1,user2"`

`-r SPEC` Удалить доступ `-r "org/repo:user1"`

`-p` Read-only доступ (pull) `-p -g "org/repo:user1"`

`-a` Admin доступ | `-a -g "org/repo:user1"`


Пример добавление доступа
```bash
#Добавить несколько пользователей
python3 grant_access_to_github_repo.py -t token.txt -g "testorg/myrepo:bot1,bot2,bot3"
```

### Уровни доступа:
Read `-p` просмотр, клонирование
Write (по умолчанию) + запись, создание PR
Admin `-a`+ управление настройками