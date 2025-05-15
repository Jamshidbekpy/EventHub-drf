from django.urls import path
from .views import (
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
    RegisterEventAPIView,
    ActivationRegisterAPIView,
    LogoutEventAPIView,
    ConfirmLogoutEventAPIView,
)


urlpatterns = [
    path("api/events/", EventListCreateAPIView.as_view(), name="event-list-create"),
    path(
        "/api/events/<str:slug>/",
        EventRetrieveUpdateDestroyAPIView.as_view(),
        name="event-retrieve-update-destroy",
    ),
    path(
        "api/events/<str:slug>/register/",
        RegisterEventAPIView.as_view(),
        name="api_register_event",
    ),
    path(
        "api/events/activate/<uidb64>/<token>/",
        ActivationRegisterAPIView.as_view(),
        name="api_activate_event",
    ),
    path(
        "api/events/<str:slug>/cancel/",
        LogoutEventAPIView.as_view(),
        name="api_logout_event",
    ),
    path(
        "api/events/confirm-logout/<uidb64>/<token>/",
        ConfirmLogoutEventAPIView.as_view(),
        name="api_confirm_logout_event",
    ),
]
