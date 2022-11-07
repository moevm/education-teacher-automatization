# education-teacher-automatization
Скрипты для автоматизации образовательных задач, в частности связанных с онлайн-курсами и репозиториями студентов

## [grant_access_to_github_repo.py](https://github.com/OSLL/education-teacher-automatization/blob/main/grant_access_to_github_repo.py)
Добавляет людей в коллабораторы репозитория. Есть возможность добавить как на чтение, так и на запись  
Примеры использования

Добавление пользователя suiciderabbit в репозиторий github.com/moevm/cs_lectures с правами только на чтение:  
`./grant_access_to_github_repo.py -g=moevm/cs_lectures:suiciderabbit -p True -t ghp_0XXXXXXXXXXXXXXXXX`  
Добавление пользователей suiciderabbit и pro100kot в репозиторий github.com/moevm/cs_lectures с правами на запись:  
`./grant_access_to_github_repo.py -g=moevm/cs_lectures:suiciderabbit,pro100kot -t ghp_0XXXXXXXXXXXXXXXXX`  
После ключа `-t` следует указать токен.
### Как получить токен
[Инструкция](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

[Прямая ссылка на настройки](https://github.com/settings/tokens)

## Часть скриптов перенесена из старого репозитория:
https://github.com/OSLL/stepik-automation
