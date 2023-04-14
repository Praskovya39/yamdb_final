# Групповой проект по теме API
## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 

## Запуск проекта
- Клонировать репозиторий и перейти в него в командной строке.
- Установить и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

```bash
python -m pip install --upgrade pip
```

- Затем нужно установить все зависимости из файла requirements.txt

```bash
pip install -r requirements.txt
```

- Выполняем миграции:

```bash
python manage.py migrate
```

- Запускаем проект:

```bash
python manage.py runserver
```

## Примеры запросов к API:
GET api/v1/title/ - получить список всех произведений.

- Для создания публикации используем:

```r
POST запрос к эндпоинту /api/v1/title/
```

в body указываем:

```json
{
"name": "name",
"year": "year",
"description": не обязательно,
"genre": "genre",
"category": "category"
}