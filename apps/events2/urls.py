from django.urls import path
from .views import EventsList, EventDetail

app_name = "events2"

urlpatterns = [
    path("events/", EventsList.as_view(), name="events_list"),
    path("events/<slug:slug>/", EventDetail.as_view(), name="event_detail"),
]