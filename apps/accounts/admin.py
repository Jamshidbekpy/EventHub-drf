from django.contrib import admin
from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id","email", "is_organizer_pending")
    search_fields = ("email", "is_organizer_pending")
    list_filter = ("is_organizer_pending",)
