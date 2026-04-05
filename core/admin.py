from django.contrib import admin
from .models import Community, PointOfDelivery, Book

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'address')
    search_fields = ('name', 'address')
    list_filter = ('type',)

@admin.register(PointOfDelivery)
class PointOfDeliveryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'community', 'is_active')
    list_filter = ('type', 'community', 'is_active')
    search_fields = ('name', 'address')
    # Добавим возможность быстрого редактирования статуса
    list_editable = ('is_active',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'author', 
        'owner', 
        'status', 
        'community', 
        'point_of_delivery', 
        'created_at'
    )
    list_filter = (
        'status', 
        'type', 
        'condition', 
        'community', 
        'point_of_delivery__is_active'
    )
    search_fields = (
        'title', 
        'author', 
        'isbn', 
        'owner__username'
    )
    readonly_fields = ('created_at', 'updated_at')
    # Показывать владельца как ссылку на пользователя
    raw_id_fields = ('owner',)  # удобно, если много пользователей
    # Или можно использовать autocomplete_fields, но тогда нужен search в UserAdmin
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('owner', 'community', 'point_of_delivery')