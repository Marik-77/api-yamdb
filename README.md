# YamDB API

## 📝 Описание проекта

YamDB — это REST API для сервиса отзывов на фильмы, книги и музыку. Приложение поддерживает управление категориями, жанрами и произведениями, позволяет пользователям оставлять отзывы и комментарии. Реализована система ролей (user, moderator, admin) с соответствующими правами доступа.

## 👨‍💻 Автор

**Петров Марк**
- Email: [marikp20@gmail.com]

## 🛠️ Стек технологий

- **Python 3.9+**
- **Django 3.2**
- **Django REST Framework**
- **djangorestframework-simplejwt**
- **django-filter**

## 🚀 Локальное развертывание

### 1. Клонирование репозитория

```bash
git clone https://github.com/Marik-77/api-yamdb.git
cd api-yamdb
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/MacOS
# или
venv\Scripts\activate  # для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Переменные окружения

Создайте файл `.env` в корневой директории проекта:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Подготовка базы данных

```bash
python manage.py migrate
```

### 6. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000/`

## 📚 Примеры использования API

### Регистрация пользователя

```bash
POST /api/v1/auth/signup/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com"
}
```

### Получение JWT токена

```bash
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "john_doe",
  "confirmation_code": "your-code"
}
```

### Получение списка произведений

```bash
GET /api/v1/titles/
Authorization: Bearer <your-token>
```

### Создание отзыва

```bash
POST /api/v1/titles/{title_id}/reviews/
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "text": "Отличное произведение!",
  "score": 9
}
```
