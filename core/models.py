from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Сущность Community из ПР-03
class Community(models.Model):
    TYPE_CHOICES = [
        ('school', 'Школа'),
        ('family', 'Семья/Район'),
        ('company', 'Компания'),
    ]
    name = models.CharField(max_length=255, verbose_name="Название сообщества")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип")
    address = models.CharField(max_length=500, blank=True, verbose_name="Адрес")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"

# Сущность PointOfDelivery из ПР-03
class PointOfDelivery(models.Model):
    TYPE_CHOICES = [
        ('library', 'Библиотека'),
        ('office', 'Офис'),
        ('cafe', 'Кафе'),
        ('school', 'Школа'),
    ]
    name = models.CharField(max_length=255, verbose_name="Название точки")
    address = models.CharField(max_length=500, verbose_name="Адрес")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип точки")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='points', verbose_name="Сообщество")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    class Meta:
        verbose_name = "Точка выдачи"
        verbose_name_plural = "Точки выдачи"

# Сущность Book из ПР-03
class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('reserved', 'Забронирована'),
        ('transferred', 'Передана'),
    ]
    
    TYPE_CHOICES = [
        ('textbook', 'Учебник'),
        ('fiction', 'Художественная'),
        ('professional', 'Профессиональная'),
    ]

    CONDITION_CHOICES = [
        ('excellent', 'Отличное'),
        ('good', 'Хорошее'),
        ('used', 'Поношенное'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.CharField(max_length=255, verbose_name="Автор")
    isbn = models.CharField(max_length=13, blank=True, null=True, verbose_name="ISBN")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип книги")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Состояние")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', verbose_name="Владелец")
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name="Сообщество")
    point_of_delivery = models.ForeignKey(PointOfDelivery, on_delete=models.SET_NULL, null=True, blank=True, related_name='books', verbose_name="Точка выдачи")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    # Поле для фото (опционально, для MVP можно без него, но лучше добавить)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="Обложка")

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse('profile') # После добавления редиректим в профиль

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"