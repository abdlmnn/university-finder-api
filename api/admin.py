from django.contrib import admin
from .models import *

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'lat', 'lng', 'created_at')
    search_fields = ('name', 'country')

@admin.register(FavoriteUniversity)
class FavoriteUniversityAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'added_at')
    search_fields = ('user__username', 'university__name')
