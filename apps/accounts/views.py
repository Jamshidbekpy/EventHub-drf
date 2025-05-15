from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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


# from rest_framework_simplejwt.authentication import JWTAuthentication
