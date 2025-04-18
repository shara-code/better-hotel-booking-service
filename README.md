# Better Hotel Booking Service

Сервис бронирования отелей, разработанный с использованием FastAPI


## Установка

### Метод 1: Локальная установка с uv (рекомендуется)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/better-hotel-booking-service.git
   cd better-hotel-booking-service
   ```

2. Установите uv согласно [официальной документации](https://astral.sh/uv):
   ```bash
   # Например, через pipx
   pipx install uv
   ```

3. Создайте виртуальное окружение и установите зависимости:
   ```bash
   uv venv
   source .venv/bin/activate  # Для Linux/macOS
   # или
   .venv\Scripts\activate  # Для Windows
   
   uv sync
   ```

4. Создайте файл .env в корне проекта (см. раздел Конфигурация)

### Метод 2: Традиционная установка с pip

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/better-hotel-booking-service.git
   cd better-hotel-booking-service
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/macOS
   # или
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -e .
   ```

4. Создайте файл .env в корне проекта (см. раздел Конфигурация)

### Метод 3: Использование Docker

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/better-hotel-booking-service.git
   cd better-hotel-booking-service
   ```

2. Создайте файл .env в корне проекта (см. раздел Конфигурация)

3. Запустите контейнеры с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Конфигурация

Создайте файл `.env` в корне проекта со следующими переменными:

```
MODE=DEV  # Режим работы (DEV, TEST, PROD)

# Основная база данных
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=hotel_booking
DSN=postgresql+asyncpg://postgres:postgres@localhost:5432/hotel_booking

# Тестовая база данных
TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=postgres
TEST_DB_PASS=postgres
TEST_DB_NAME=hotel_booking_test

# Настройки JWT
SECRET_KEY=your_secret_key
ALGORITHM=HS256

# Настройки SMTP для отправки email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASS=your_email_password

# Настройки Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Настройки Celery (при локальном запуске)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Запуск приложения

### Локальный запуск

#### Основное приложение (режим разработки):
```bash
uvicorn app.main:app --reload
```

#### Основное приложение (продакшн режим):
```bash
gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 app.main:app
```

#### Celery worker:
```bash
celery -A app.tasks.celery worker --loglevel=info
```

#### Flower (мониторинг Celery):
```bash
celery -A app.tasks.celery flower --port=5555
```

### Запуск через Docker Compose

Запуск всех сервисов:
```bash
docker-compose up -d
```

Запуск отдельных сервисов:
```bash
docker-compose up -d app  # Только FastAPI приложение
docker-compose up -d db redis  # Только базы данных
docker-compose up -d celery flower  # Только Celery и Flower
```

Для остановки:
```bash
docker-compose down
```

## API документация

После запуска приложения, API документация доступна по следующим адресам:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Мониторинг Celery

После запуска Flower, панель мониторинга Celery доступна по адресу:

- Flower UI: http://localhost:5555

## Тестирование

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск конкретного теста
pytest app/tests/test_file.py

# Запуск с подробным выводом
pytest -v
```

В проекте используется автоматический режим asyncio для тестов, настроенный в файле pytest.ini.

### Запуск тестов с покрытием:

```bash
pytest --cov=app tests/
```

## Миграции базы данных

Для управления миграциями используется Alembic:

```bash
# Создание новой миграции
alembic revision --autogenerate -m "описание миграции"

# Применение всех миграций
alembic upgrade head

# Применение конкретного количества миграций
alembic upgrade +1

# Откат миграций
alembic downgrade -1

# Просмотр истории миграций
alembic history
```

Миграции расположены в директории `app/migrations`.

## Мониторинг

### Логи контейнеров (при использовании Docker)

```bash
# Просмотр логов всех контейнеров
docker-compose logs

# Просмотр логов конкретного сервиса
docker-compose logs app
docker-compose logs db
docker-compose logs redis
docker-compose logs celery
docker-compose logs flower
```

## Структура проекта

```
better-hotel-booking-service/
├── alembic/              # Миграции базы данных
├── app/                  # Основной код приложения
│   ├── admin/            # Административная панель
│   ├── bookings/         # Логика бронирований
│   ├── dao/              # Объекты доступа к данным
│   ├── hotels/           # Логика отелей
│   ├── images/           # Обработка изображений
│   ├── migrations/       # Миграции базы данных
│   ├── pages/            # Веб-страницы
│   ├── sentry/           # Интеграция с Sentry
│   ├── static/           # Статические файлы
│   ├── tasks/            # Celery задачи
│   ├── templates/        # Шаблоны
│   ├── tests/            # Тесты
│   ├── users/            # Логика пользователей
│   ├── config.py         # Конфигурация приложения
│   ├── database.py       # Работа с базой данных
│   ├── exceptions.py     # Обработка исключений
│   └── main.py           # Точка входа в приложение
├── tests/                # Дополнительные тесты
├── .env                  # Переменные окружения
├── .gitignore            # Файлы, игнорируемые Git
├── docker-compose.yaml   # Конфигурация Docker Compose
├── Dockerfile            # Инструкции сборки Docker образа
├── pyproject.toml        # Зависимости и метаданные проекта
├── uv.lock               # Файл блокировки зависимостей для uv
└── README.md             # Этот файл
```

## Особенности проекта

- **FastAPI** - современный высокопроизводительный веб-фреймворк для создания API
- **SQLAlchemy** - ORM для работы с базой данных PostgreSQL
- **Pydantic** - валидация данных и сериализация
- **Redis** - кэширование и брокер сообщений для Celery
- **Celery** - распределенная очередь задач для асинхронной обработки
- **Flower** - веб-интерфейс для мониторинга задач Celery
- **Alembic** - инструмент для миграций базы данных
- **Docker и Docker Compose** - контейнеризация и оркестрация

## Поддержка

При возникновении проблем создайте issue в репозитории проекта или обратитесь к разработчикам.

## Разработка

### Установка pre-commit хуков

Проект использует pre-commit для автоматического форматирования и проверки кода. Для установки хуков выполните:

```bash
# Установка pre-commit
uv add pre-commit

```

### Стиль кода

Проект использует следующие инструменты для поддержания стиля кода:
- **Ruff** - для линтинга и форматирования кода
- **pre-commit** - для автоматизации проверок перед коммитом

Вы можете запустить проверки вручную:

```bash
# Проверка кода с помощью Ruff
ruff check .

# Форматирование кода
ruff format .
```
