# Скрипт для управления доступом к репозиториям в Forgejo

## **Создание токенов**

**Важно:** 
- Для **локального Forgejo** используйте `http://<FORGEJO_HOST>`
- Для **развернутого на сервере Forgejo** используйте `https://<FORGEJO_HOST>>`

FORGEJO_HOST - актуальный домен

**Через WEB UI:**
1. Залогиньтесь в Forgejo
2. Перейдите: **Настройки** → **Приложения** → **Сгенерировать новый токен**
3. Укажите имя токена
4. Выберите права:
	repo (обязательно)
	admin:org (для работы с организациями)
	write:org (для управления доступом)
5. Сохраните токен в файл

**Через API:**
Используйте учетные данные **администратора** или **пользователя с правами** создавать токены:
```bash
curl -X POST \
	-H "Content-Type: application/json" \
	-u <ADMIN_USERNAME>:<ADMIN_PASSWORD> \
	http://<FORGEJO_HOST>/api/v1/users/<BOT_USERNAME>/tokens \
	-d '{"name":"<TOKEN_NAME>", "scopes": ["repo", "write:org"]}'
```

Параметры:

ADMIN_USERNAME - логин администратора/пользователя с правами

ADMIN_PASSWORD - пароль администратора

BOT_USERNAME - логин бота, для которого создается токен

TOKEN_NAME - уникальное имя токена

scopes - права доступа (рекомендуемые: repo, write:org)


## **Настройка организаций**

Создание организации через WEB UI:
1. **Профиль** → **Ваши организации** → **Создать организацию**
2. Заполните:
   - Название
   - Описание (опционально)
3. Нажмите **Создать организацию**

Создание организации через API:

```bash
curl -X POST -H "Authorization: token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"username":"testorg", "description":"Test organization"}' \
  http://<FORGEJO_HOST>/api/v1/orgs
```
TOKEN - используйте токен администратора, созданный в разделе "Создание токенов"

## Использование скрипта

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

### Уровни доступа:
Read `-p` просмотр, клонирование
Write (по умолчанию) + запись, создание PR
Admin `-a`+ управление настройками

# Скрипт для создания репозиториев Forgejo из CSV файла
**Формат CSV файла**
Файл должен иметь расширение .csv и содержать данные в следующем формате (разделитель - точка с запятой):
```bash
<организация>/<название репозитория>;<приватный?(bool)>;<создать README?(bool)>;<логины тем, кому дать доступ на чтение(через запятую)>;<логины тем, кому дать доступ на запись(через запятую)>;<логины тем, кому дать админский доступ(через запятую)>
```
**Пример содержимого CSV:**
```bash
myorg/myrepo1;true;true;user1,user2;user3;user4
myorg/myrepo2;false;false;user5;;user6
myorg/myrepo3;true;true;;user7,user8;
```

## **Использование**
```bash
python3 create_github_repos_from_csv.py -t <файл_с_токеном> -f <csv_файл>
```

**Параметры**
`-t`, `--token` - путь к файлу с токеном доступа (обязательно)

`-f`, `--file` - путь к CSV файлу с данными (обязательно)

`--template` - использовать шаблонный репозиторий (опционально)

`--branch_protection` - включить защиту веток (опционально)

## **Примеры использования**
```bash
# Базовое создание репозиториев
python3 create_github_repos_from_csv.py -t token.txt -f repos.csv

# Создание с использованием шаблона
python3 create_github_repos_from_csv.py -t token.txt -f repos.csv --template owner/template-repo

# Создание с защитой веток
python3 create_github_repos_from_csv.py -t token.txt -f repos.csv --branch_protection
```
**Выходные данные**

Список добавленных пользователей
Ссылки на страницы приглашений для каждого репозитория
