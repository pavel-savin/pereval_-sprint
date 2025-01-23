
# 🏔️ Pereval API

**REST API для учёта и модерации горных перевалов**  
Серверная часть системы, позволяющая туристам добавлять данные о перевалах, а модераторам — проверять их.

---

## 📌 Задача проекта

Разработать API для мобильного приложения, которое:
1. Позволяет пользователям добавлять информацию о перевалах (координаты, фото, уровень сложности).
2. Обеспечивает модерацию данных через изменение статуса записей.
3. Запрещает редактирование данных после прохождения модерации.

---

## 🚀 Возможности API

### Основные методы:
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `POST` | `/submitData/` | Добавление нового перевала |
| `GET` | `/submitData/<id>/` | Получение данных по ID |
| `PATCH` | `/submitData/<id>/update/` | Редактирование (только статус `new`) |
| `GET` | `/submitData/list/?user__email=<email>` | Фильтрация по email пользователя |

### Ключевые особенности:
✅ Работа с изображениями в Base64  
✅ Валидация координат и уровней сложности  
✅ Автоматический статус `new` для новых записей  
✅ Защита от изменения персональных данных  
✅ Поддержка Docker + PostgreSQL

---

## 🛠 Технологии

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-red?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?logo=docker&logoColor=white)

---

## 🚀 Быстрый старт

### 1. Установка
```bash
git clone https://github.com/pavel-savin/pereval_-sprint
cd pereval
cp .env.example .env  # Заполните настройки БД
```

## 🚀 Примеры API

### 1. POST /submitData/  
**Добавление перевала**  
**Запрос:**  
```json
{
  "beauty_title": "пер. Грозный",
  "title": "Кавказский перевал",
  "user": {
    "email": "alpinist@mail.ru",
    "fam": "Петров",
    "name": "Иван",
    "phone": "+7 999 123-45-67"
  },
  "coords": {
    "latitude": 43.256790,
    "longitude": 42.456123,
    "height": 3200
  },
  "level": {
    "summer": "2Б"
  },
  "attached_images": [
    {
      "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
      "title": "Седловина"
    }
  ]
}
```

**Ответ:**  
```json
{
  "status": 200,
  "message": null,
  "id": 105
}
```

---

### 2. GET /submitData/105/  
**Получение данных по ID**  
**Ответ:**  
```json
{
  "id": 105,
  "beauty_title": "пер. Грозный",
  "title": "Кавказский перевал",
  "status": "new",
  "user": {
    "email": "alpinist@mail.ru",
    "fam": "Петров",
    "name": "Иван",
    "phone": "+7 999 123-45-67"
  },
  "coords": {
    "latitude": 43.256790,
    "longitude": 42.456123,
    "height": 3200
  },
  "level": {
    "summer": "2Б"
  },
  "attached_images": [
    {
      "data": "/media/images/105_view.jpg",
      "title": "Седловина"
    }
  ]
}
```

---

### 3. PATCH /submitData/105/update/  
**Редактирование перевала**  
**Запрос:**  
```json
{
  "title": "Обновлённый Кавказский перевал",
  "level": {
    "summer": "3А"
  }
}
```

**Успешный ответ:**  
```json
{
  "state": 1,
  "message": null
}
```

**Ошибка:**  
```json
{
  "state": 0,
  "message": "Редактирование запрещено: запись не в статусе 'new'"
}
```

---

### 4. GET /submitData/list/?user__email=alpinist@mail.ru  
**Фильтрация по email**  
**Ответ:**  
```json
[
  {
    "id": 105,
    "title": "Обновлённый Кавказский перевал",
    "status": "pending",
    "user": {"email": "alpinist@mail.ru"},
    "coords": {"latitude": 43.256790}
  }
]
```
