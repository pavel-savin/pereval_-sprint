from django.contrib import admin
from django.utils.html import format_html
from .models import User, Coords, Level, Pereval, Image

# Кастомизация встроенной формы для изображений
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Количество дополнительных полей для загрузки изображений
    readonly_fields = ('image_preview',)  # Поле для миниатюры
    fields = ('image_preview', 'data', 'title')  # Поля в форме

    def image_preview(self, obj):
        if obj.data:  # Проверяем, есть ли изображение
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.data.url)
        return "No Image"

    image_preview.short_description = "Preview"

class PerevalAdmin(admin.ModelAdmin):
    list_display = ('title', 'beauty_title', 'user', 'add_time')  # Поля в списке объектов
    list_filter = ('user', 'add_time')  # Фильтры справа
    search_fields = ('title', 'beauty_title')  # Поиск по полям
    inlines = [ImageInline]  # Встроенная форма для изображений

# Кастомизация админки для User
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fam', 'name', 'phone')  # Отображаемые поля
    search_fields = ('email', 'fam')  # Поиск по email и фамилии

# Регистрация всех моделей
admin.site.register(User, UserAdmin)
admin.site.register(Coords)
admin.site.register(Level)
admin.site.register(Pereval, PerevalAdmin)
admin.site.register(Image)
# Register your models here.
