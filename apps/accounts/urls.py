from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, ActivateAccountAPIView, LogoutView
from django.urls import path

urlpatterns = [
    path("api/register/", RegisterAPIView.as_view(), name="api_register"),
    path(
        "api/activate/<uidb64>/<token>/",
        ActivateAccountAPIView.as_view(),
        name="api_activate",
    ),
]

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
