from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    otc = models.CharField(max_length=150, blank=True, default='')
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.fam} {self.name}'

class Coords(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    height = models.IntegerField()

    def __str__(self):
        return f'Lat: {self.latitude}, Lon: {self.longitude}, H: {self.height}'

class Level(models.Model):
    winter = models.CharField(max_length=2, blank=True, default='')
    summer = models.CharField(max_length=2, blank=True, default='')
    autumn = models.CharField(max_length=2, blank=True, default='')
    spring = models.CharField(max_length=2, blank=True, default='')

    def __str__(self):
        return f'Уровень: зима({self.winter}), лето({self.summer})'

class Pereval(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('pending', 'На модерации'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True, default='')
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.title

class Image(models.Model):
    pereval = models.ForeignKey(
        Pereval, 
        on_delete=models.CASCADE, 
        related_name='attached_images'  # Уникальное имя для обратной связи
    )
    data = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
# Create your models here.
