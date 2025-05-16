from .views import (
    RegisterAPIView,
    ActivateAccountAPIView,
    LogoutView,
    ConfirmOrganizerAPIView,
    ActivationOrganizer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path("api/register/", RegisterAPIView.as_view(), name="api_register"),
    path(
        "api/activate/<uidb64>/<token>/",
        ActivateAccountAPIView.as_view(),
        name="api_activate",
    ),
    path(
        "api/confirm-organizer/",
        ConfirmOrganizerAPIView.as_view(),
        name="api_confirm_organizer",
    ),
    path(
        "api/activate-organizer/<uidb64>/<token>/",
        ActivationOrganizer.as_view(),
        name="api_activate_organizer",
    ),
]

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
]

