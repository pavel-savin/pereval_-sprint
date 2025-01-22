from django.db import IntegrityError
from .models import User, Coords, Level, Pereval, Image

class DataHandler:
    @staticmethod
    def create_pereval(data):
        try:
            user_data = data.pop('user')
            email = user_data['email']
            
            # Обновляем или создаем пользователя
            user, created = User.objects.update_or_create(
                email=email,
                defaults=user_data
            )
            
            coords = Coords.objects.create(**data.pop('coords'))
            level = Level.objects.create(**data.pop('level'))
            images_data = data.pop('images')
            
            pereval = Pereval.objects.create(
                **data,
                user=user,
                coords=coords,
                level=level
            )
            
            for image_data in images_data:
                Image.objects.create(pereval=pereval, **image_data)
            
            return pereval.id, None
        except IntegrityError as e:
            return None, f"Ошибка целостности данных: {str(e)}"
        except Exception as e:
            return None, str(e)