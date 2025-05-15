from django.contrib import admin
from .models import Event, EventParticipant

# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "date",
        "start_time",
        "end_time",
        "location",
        "max_participants",
        "status",
    )
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-date",)
    list_per_page = 10
    date_hierarchy = "date"


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "registered_at")
    search_fields = ("user__username", "event__title")
    list_filter = ("event",)
    ordering = ("-registered_at",)
    list_per_page = 10
