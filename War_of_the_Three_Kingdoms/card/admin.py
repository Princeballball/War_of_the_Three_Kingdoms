from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'faction', 'health', 'image_path')
    list_filter = ('faction',)
    search_fields = ('name', 'image_path')
