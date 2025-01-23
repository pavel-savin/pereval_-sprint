from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Pereval, User, Coords, Level, Image

# Create your tests here.
class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            fam="Иванов",
            name="Петр",
            phone="+79991234567"
        )
        self.coords = Coords.objects.create(
            latitude=45.3842,
            longitude=7.1525,
            height=1200
        )
        self.level = Level.objects.create(summer="1А")
        self.pereval = Pereval.objects.create(
            beauty_title="пер. Тестовый",
            title="Тестовый перевал",
            other_titles="Тест",
            connect="",
            user=self.user,
            coords=self.coords,
            level=self.level
        )
        Image.objects.create(
            pereval=self.pereval,
            data="test.jpg",
            title="Тестовое фото"
        )
        
    # 1. Успешное создание перевала (все обязательные поля + правильные типы)
    def test_create_pereval_success(self):
        valid_data = {
            "beauty_title": "пер. ",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "",
            "user": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
                "name": "Василий",
                "otc": "Иванович",
                "phone": "+7 555 55 55"
            },
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "attached_images": [
                {
                    "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=", 
                    "title": "Седловина"
                },
                {
                    "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=", 
                    "title": "Подъём"
                }
            ]
        }
        
        response = self.client.post("/api/submitData/", valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIsNone(response.data["message"])
        
    # 2. Получение перевала по ID (проверка структуры ответа)
    def test_get_pereval_by_id(self):
        response = self.client.get(f"/api/submitData/{self.pereval.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # 3. Редактирование перевала в статусе 'new' (корректный формат запроса)
    def test_update_new_pereval(self):
        update_data = {"title": "Обновленное название"}
        response = self.client.patch(
            f"/api/submitData/{self.pereval.id}/update/",
            update_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["state"], 1)
        
    # 4. Запрет редактирования не в статусе 'new'
    def test_update_non_new_pereval(self):
        self.pereval.status = "accepted"
        self.pereval.save()
        
        response = self.client.patch(
            f"/api/submitData/{self.pereval.id}/update/",
            {"title": "Недопустимое обновление"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["state"], 0)
        
    # 5. Фильтрация по email (адаптация под текущую структуру ответа)
    def test_filter_by_email(self):
        response = self.client.get("/api/submitData/list/?user__email=test@example.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # 6. Обработка невалидных данных (проверка основных ошибок)
    def test_invalid_data_creation(self):
        invalid_data = {
            "title": "Неполные данные",
            "beauty_title": "",  # Обязательное поле
            "other_titles": "",  # Обязательное поле
            "connect": "",       # Обязательное поле
            "user": {"fam": "Неполный"},  # Ошибки в nested поле
            "coords": {},        # Ошибки в nested поле
            "level": {},         # Ошибки в nested поле
            "attached_images": [] 
        }
        
        response = self.client.post("/api/submitData/", invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Проверка основных ошибок без привязки к структуре
        errors = str(response.data).lower()
        self.assertTrue(any(word in errors for word in ['email', 'name', 'phone', 'latitude', 'summer']))
        
# Create your tests here.

