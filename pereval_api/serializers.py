from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import User, Coords, Level, Pereval, Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']

class ImageSerializer(serializers.ModelSerializer):
    data = Base64ImageField()
    
    class Meta:
        model = Image
        fields = ['data', 'title']

class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Запрещаем изменение пользователя
    coords = CoordsSerializer()
    level = LevelSerializer()
    attached_images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 
            'add_time', 'user', 'coords', 'level', 'attached_images', 'status'
        ]
        read_only_fields = ['status', 'user']

    def update(self, instance, validated_data):
        coords_data = validated_data.pop('coords', None)
        if coords_data:
            Coords.objects.filter(id=instance.coords.id).update(**coords_data)

        level_data = validated_data.pop('level', None)
        if level_data:
            Level.objects.filter(id=instance.level.id).update(**level_data)

        images_data = validated_data.pop('attached_images', None)
        if images_data:
            instance.attached_images.all().delete()
            for img_data in images_data:
                Image.objects.create(pereval=instance, **img_data)

        return super().update(instance, validated_data)