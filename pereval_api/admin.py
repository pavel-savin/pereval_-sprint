from django.contrib import admin
from django.utils.html import format_html
from .models import User, Coords, Level, Pereval, Image

# Кастомизация встроенной формы для изображений
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Количество дополнительных полей для загрузки изображений
    readonly_fields = ('image_preview',)  # Поле для миниатюры
    fields = ('image_preview', 'data', 'title')  # Поля в форме
    fk_name = 'pereval'  # Явное указание связи
    
    def image_preview(self, obj):
        if obj.data:  # Проверяем, есть ли изображение
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.data.url)
        return "No Image"

    image_preview.short_description = "Preview"
@admin.register(Pereval)
class PerevalAdmin(admin.ModelAdmin):
    list_display = ('title', 'beauty_title', 'status', 'add_time')
    list_filter = ('status', 'add_time')
    search_fields = ('title', 'beauty_title')
    inlines = [ImageInline]

# Кастомизация админки для User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fam', 'name', 'phone')
    search_fields = ('email', 'fam')

@admin.register(Coords)
class CoordsAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'height')

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('winter', 'summer', 'autumn', 'spring')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'pereval')
# Register your models here.
