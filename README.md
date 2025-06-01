# fastapi_crud

REST API на FastAPI для работы с вопросами и ответами (например, для викторин или обучающих платформ).

В учебных целях, посмотреть стек.

## Стек
- Postgres
- SQLAlchemy 2.0.41 + Alembic
- Pydantic 
- FastAPI 0.115
- Python 3.9+

## Быстрый старт

### Установка

```console
git clone https://github.com/megaturik/fastapi_crud
cd fastapi_crud
python3 -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```
### Настройка .env
```
POSTGRES_USER = user
POSTGRES_PASSWORD = password
POSTGRES_DB = test_db
POSTGRES_HOST = localhost
```

## Заполнение базы тестовыми данными:
Запускаеv Postgres через docker-compose, реквизиты доступа подтягиваются из общего .env:

```console
docker compose up -d 
```
Создаем базу данных скриптом init_db.py:

```console
python3 init_db.py
```

Или через alembic в проекте:

```console
alembic upgrade head
```


В test-data/questions.csv есть некоторе количество подготовленных вопросов.

Можно добавить их в базу:

```console
python3 fill_db_from_csv.py
```

## Запуск приложения

```console
fastapi dev app/main.py
```

Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Документация

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

##  Эндпоинты

### `GET /api/v1/questions/`

Получить список всех вопросов.

### `POST /api/v1/questions/`

Создать новый вопрос.

#### Пример запроса

```json
{
  "text": "Столица Франции?",
  "difficult_id": 1,
  "answers": [
    {"text": "Париж", "is_correct": true},
    {"text": "Челябинск", "is_correct": false},
    {"text": "Чиангмай", "is_correct": false},
    {"text": "Новый Уренгой", "is_correct": false}
  ]
}
```

### `GET /api/v1/questions/{question_id}`

Получить вопрос по ID с его ответами.

##  Структура проекта

```
.
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── ...
├── tests/
├── openapi.json
├── requirements.txt
└── README.md
```
