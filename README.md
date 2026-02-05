# YaMDb (api_yamdb)

Краткое описание
- YaMDb — бэкенд-сервис для сбора отзывов и рейтингов на произведения (фильмы, книги, музыка).
- Пользователи оставляют отзывы и оценки (1–10), комментируют отзывы. Есть роли: user, moderator, admin.

Особенности
- Регистрация с подтверждением по email (confirmation_code) и выдача JWT-токенов.
- CRUD для пользователей (админ), категорий, жанров, произведений (admin), отзывов и комментариев.
- Автоматический расчёт рейтинга произведения по отзывам.
- Пагинация, фильтрация и права доступа согласно спецификации.

Требования
- Python 3.8+
- Django 4+/5+
- djangorestframework
- djangorestframework-simplejwt
- django-filter
(используйте виртуальное окружение)

Быстрый старт (локально)
1. Клонировать репозиторий и перейти в папку проекта:
   git clone <repo> && cd api_yamdb

2. Создать и активировать виртуальное окружение, установить зависимости:
   python -m venv venv
   source venv/bin/activate   # или venv\Scripts\activate на Windows
   pip install -r requirements.txt

3. Выполнить миграции и создать суперпользователя:
   python manage.py migrate
   python manage.py createsuperuser

4. (Опционально) Подготовка тестовых пользователей:
   В проекте есть скрипт postman_collection/set_up_data.sh для быстрого создания тестовых аккаунтов.

5. Заполнить базу тестовыми данными из csv (если есть):
   Файлы лежат в `static/data/`. Можно написать management command или импортировать через Django shell.

6. Запуск сервера:
   python manage.py runserver

Документация API
- Редок: http://127.0.0.1:8000/redoc/
- Базовый путь API: /api/v1/
  Примеры эндпоинтов:
  - /api/v1/auth/signup/ — регистрация (email + username)
  - /api/v1/auth/token/ — получение JWT (username + confirmation_code)
  - /api/v1/users/ — CRUD пользователей (только для admin)
  - /api/v1/categories/, /api/v1/genres/, /api/v1/titles/
  - /api/v1/titles/{title_id}/reviews/
  - /api/v1/titles/{title_id}/reviews/{review_id}/comments/

Тестирование
- Запуск тестов:
  pytest

Примечания
- Email backend по умолчанию использует консоль (вывод confirmation_code в stdout).
- Пользователь с username `me` запрещён.
- Суперпользователь всегда считается администратором.

Лицензия
- Проект предоставлен для учебных целей.

