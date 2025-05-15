from django.urls import path
from .views import EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('api/events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('/api/events/<str:slug>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-retrieve-update-destroy'),

]