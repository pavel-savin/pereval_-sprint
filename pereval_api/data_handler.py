from django.db import transaction, IntegrityError
from .models import User, Coords, Level, Pereval, Image

class DataHandler:
    @staticmethod
    @transaction.atomic
    def create_pereval(data):
        """Создает запись о перевале и связанные объекты в БД"""
        try:
            # Извлечение вложенных данных
            user_data = data.pop('user')
            coords_data = data.pop('coords')
            level_data = data.pop('level')
            images_data = data.pop('attached_images')

            # Создание пользователя (или обновление, если email существует)
            user, _ = User.objects.update_or_create(
                email=user_data['email'],
                defaults=user_data
            )

            # Создание координат
            coords = Coords.objects.create(**coords_data)

            # Создание уровня сложности
            level = Level.objects.create(**level_data)

            # Создание перевала (статус автоматически 'new' через модель)
            pereval = Pereval.objects.create(
                **data,
                user=user,
                coords=coords,
                level=level
            )

            # Создание изображений
            for img_data in images_data:
                Image.objects.create(pereval=pereval, **img_data)

            return {'status': 200, 'id': pereval.id, 'message': None}

        except IntegrityError as e:
            return {'status': 500, 'id': None, 'message': f'Ошибка целостности данных: {str(e)}'}
        
        except KeyError as e:
            return {'status': 400, 'id': None, 'message': f'Отсутствует обязательное поле: {str(e)}'}
        
        except Exception as e:
            return {'status': 500, 'id': None, 'message': f'Ошибка сервера: {str(e)}'}