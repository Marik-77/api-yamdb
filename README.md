# Проект Yamdb

---

API для сервиса с отзывами на фильмы и книги. API позволяет добавлять категории, жанры и произведения. Для каждого произведения можно написать отзыв (ревью), и к каждому отзыву можно оставлять комментарии. Реализована система ролей (пользователь, модератор, админ). Админ может работать с наполнением БД (добавлять, изменять, просматривать и удалять), модератор имеет доступ к редактированию отзывов и комментариев пользователей.

---

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/Django%20REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

---

## Функционал

- Добавление новых произведений, жанров, категорий
- Публикация отзывов
- Комментарии
- Авторизация с помощью JWT токена и почты

---

## Примеры запросов

### Авторизация (запрос кода на почту)

**Метод и URL:**
```http
POST http://127.0.0.1:8000/api/v1/auth/signup/
```

**Тело запроса:**
```json
{
    "email": "user@example.com",
    "username": "string"
}
```

### Авторизация (получение токена)

**Метод и URL:**
```http
POST http://127.0.0.1:8000/api/v1/auth/token/
```

**Тело запроса:**
```json
{
    "username": "string",
    "confirmation_code": "string"
}
```

### Получение произведений

**Метод и URL:**
```http
GET http://127.0.0.1:8000/api/v1/titles/
```

### Оставить отзыв

**Метод и URL:**
```http
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

**Тело запроса:**
```json
{
    "text": "string",
    "score": 1
}
```

### Оставить комментарий

**Метод и URL:**
```http
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

**Тело запроса:**
```json
{
    "text": "string"
}
```

---

## Как запустить проект

### Клонировать репозиторий

```bash
git clone https://github.com/Woody1502/api-yamdb.git
cd api-yamdb
```

### Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### Установить зависимости

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Выполнить миграции

```bash
cd api-yamdb
python manage.py makemigrations
python manage.py migrate
```

### Запустить проект

```bash
python3 manage.py runserver
```

---

## Авторы

Алексей Смолко (Программист)

Игорь Шкода (Наставник)