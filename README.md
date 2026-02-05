# Yamdb — кратко

API для сервиса отзывов на фильмы и книги. Поддерживает категории, жанры, произведения, отзывы и комментарии. Роли: user, moderator, admin. Авторизация через email + JWT.

Основное:
- CRUD для категорий, жанров и произведений
- Отзывы и комментарии
- Роли и права доступа
- Авторизация: /api/v1/auth/signup/ и /api/v1/auth/token/

Быстрый запуск:
1. git clone https://github.com/Woody1502/api-yamdb.git
2. python3 -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver

Примеры: POST /api/v1/auth/signup/, POST /api/v1/auth/token/, GET /api/v1/titles/
