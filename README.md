# yamdb_final

[![Yamdb workflow](https://github.com/Praskovya39/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Praskovya39/yamdb_final/actions/workflows/yamdb_workflow.yml)

### Yamdb - это сервис, направленный на оценку любых произведений. Проект разработан с применением CI/CD - автоматический запуск тестов, обновление образов на Docker Hub,автоматический деплой на боевой сервер и отправка уведомления об успешном завершении в Телеграм.
```
С помощью данной плотформы люди могут обмениваться отзывами о произведениях, комментировать отзывы других участников.
```

### Технологи проекта:
```
Django 3.2
Django REST framework
Python 3.7.9
Docker
Nginx
GitHub Actions
```

### Ссылка на документацию:
```
http://51.250.73.9/redoc/
```
### Как запустить проект:
Клонировать репозиторий:
```
git clone https://github.com/Nastasya-M/yamdb_final
```

Для работы workflow необходимо добавить переменные окружения в Secrets GitHub:
```
DOCKER_USERNAME=<имя пользователя DockerHub>
DOCKER_PASSWORD=<пароль DockerHub>

USER=<username для подключения к удаленному серверу>
HOST=<ip-адрес сервера>
PASSPHRASE=<пароль для сервера (если установлен)>
SSH_KEY=<SSH-ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<id вашего Телеграм-аккаунта>
TELEGRAM_TOKEN=<Телеграм-токен вашего бота>
```
Переменные PostgreSQL, ключ проекта Django и их значения по-умолчанию можно взять из .env файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
Вход на удаленный сервер:
```
ssh <username>@<host>
```

Установка Docker:
```
sudo apt install docker.io
```

Установка Docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Скопируйте файлы docker-compose.yaml и nginx/default.conf из корневой директории локального проекта на сервер:
```
scp docker-compose.yaml <username>@<host>:/home/<username>/
scp -r nginx/ <username>@<host>:/home/<username>/
```
После успешного деплоя зайдите на боевой сервер и выполните команды:
```
sudo docker-compose exec web python manage.py migrate # примените миграции
sudo docker-compose exec web python manage.py collectstatic #подгрузите статику
sudo docker-compose exec web python manage.py createsuperuser # создайте суперпользователя
sudo docker-compose exec web python manage.py loaddata fixtures.json # заполните данными базу
```