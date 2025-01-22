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
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    attached_images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 
            'add_time', 'user', 'coords', 'level', 'attached_images', 'status'
        ]
        read_only_fields = ['status']

    def create(self, validated_data):
        images_data = validated_data.pop('attached_images')
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')

        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        pereval = Pereval.objects.create(
            **validated_data,
            user=user,
            coords=coords,
            level=level
        )

        for image_data in images_data:
            Image.objects.create(pereval=pereval, **image_data)

        return pereval