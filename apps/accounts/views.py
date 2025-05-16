from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import status

from .serializers import RegisterSerializer

User = get_user_model()


class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = (
                f"http://{current_site.domain}/accounts/api/activate/{uid}/{token}/"
            )

            message = f"Salom {user.first_name}, akkauntingizni faollashtirish uchun ushbu havolani bosing: {activation_link}"

            send_mail(
                subject="Akkauntingizni faollashtiring",
                message=message,
                from_email="jamshidbekshodibekov2004@gmail.com",
                recipient_list=[user.email],
            )

            return Response(
                {"message": "Emailga aktivatsiya havolasi yuborildi."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountAPIView(APIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError, TypeError):
            return Response(
                {"error": "Noto‘g‘ri aktivatsiya havolasi"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(
                {"message": "Akkaunt muvaffaqiyatli faollashtirildi"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Havola yaroqsiz yoki eskirgan"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ConfirmOrganizerAPIView(APIView):
    def post(self, request):
        user = request.user
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = (
            f"http://{current_site.domain}/accounts/api/activate/{uid}/{token}/"
        )

        message = f"{user.first_name} {user.last_name} sizga tashkilotchilikka ariza tashladi! Uni activlashtirish uchun {activation_link} ni bosing!"

        send_mail(
            subject=f"Activation status",
            message=message,
            from_email=user.email,
            recipient_list=["jamshidbekshodibekov2004@gmail.com"],
        )

        return Response(
            {"message": "Superuser emailiga aktivatsiya havolasi yuborildi."},
            status=status.HTTP_201_CREATED,
        )


class ActivationOrganizer(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError, TypeError):
            return Response(
                {"error": "Noto‘g‘ri aktivatsiya havolasi"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(user, token):
            user.is_organizer_pending = True
            user.save()

            return Response(
                {"message": "Foydalanuvchi tashkilotchi sifatida tasdiqlandi"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Havola yaroqsiz yoki eskirgan"},
                status=status.HTTP_400_BAD_REQUEST,
            )
