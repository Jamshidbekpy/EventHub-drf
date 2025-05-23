from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from .serializers import EventListCreateSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Event, EventParticipant
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import status

User = get_user_model()

# Create your views here.


class EventListCreateAPIView(ListCreateAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventListCreateSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_organizer_pending:
            return Response(
                {"error": "You are not authorized to create an event."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventListCreateSerializer

    lookup_field = "slug"

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        participants_count = instance.participants.count()
        if instance.owner == user:
            if participants_count == 0:
                return super().destroy(request, *args, **kwargs)
            else:
                return Response(
                    {"error": "You cannot delete an event with participants."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "You do not have permission to delete this event."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.owner == user:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"error": "You do not have permission to update this event."},
                status=status.HTTP_403_FORBIDDEN,
            )


class RegisterEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        participant = request.user
        event = get_object_or_404(Event, slug=slug)

        if event.participants.filter(pk=participant.pk).exists():
            return Response(
                {"error": "You have already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.status == "Full":
            return Response(
                {"error": "The event is full."}, status=status.HTTP_400_BAD_REQUEST
            )

        EventParticipant.objects.create(user=participant, event=event)

        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(participant.pk))
        token = default_token_generator.make_token(participant)
        activation_link = (
            f"http://{current_site.domain}/events/api/events/activate/{uid}/{token}/"
        )

        message = f"Salom {participant.first_name}, tadbirdan o'tganingizni faollashtirish uchun ushbu havolani bosing: {activation_link}"

        send_mail(
            subject="Tadbir uchun faollashtiring",
            message=message,
            from_email=event.owner.email,
            recipient_list=[participant.email],
        )

        return Response(
            {"message": "Emailga tadbirga aktivatsiya havolasi yuborildi."},
            status=status.HTTP_201_CREATED,
        )


class ActivationRegisterAPIView(APIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            participant = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError, TypeError):
            return Response(
                {"error": "Noto‘g‘ri aktivatsiya havolasi"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(participant, token):
            obj = EventParticipant.objects.get(user=participant)
            obj.is_active = True
            obj.save()

            return Response(
                {
                    "message": "Tadbirga ro'yxatdan o'tish muvaffaqiyatli faollashtirildi"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Havola yaroqsiz yoki eskirgan"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        participant = request.user
        event = get_object_or_404(Event, slug=slug)

        if not event.participants.filter(pk=participant.pk).exists():
            return Response(
                {"error": "Siz bu tadbirda ro‘yxatdan o‘tmagansiz."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(participant.pk))
        token = default_token_generator.make_token(participant)
        logout_link = f"http://{current_site.domain}/events/api/events/confirm-logout/{uid}/{token}/?slug={event.slug}"

        message = f"Salom {participant.first_name}, agar siz ushbu tadbirdan chiqmoqchi bo‘lsangiz, quyidagi havolani bosing: {logout_link}"

        send_mail(
            subject="Tadbirdan chiqish",
            message=message,
            from_email=event.owner.email,
            recipient_list=[participant.email],
        )

        return Response(
            {"message": "Chiqish havolasi emailga yuborildi."},
            status=status.HTTP_200_OK,
        )


class ConfirmLogoutEventAPIView(APIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        slug = request.query_params.get("slug")
        if not slug:
            return Response(
                {"error": "Tadbir slug topilmadi"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            participant = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError, TypeError):
            return Response(
                {"error": "Noto‘g‘ri havola"}, status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(participant, token):
            event = get_object_or_404(Event, slug=slug)
            try:
                participant_link = EventParticipant.objects.get(
                    user=participant, event=event
                )
                participant_link.delete()
            except EventParticipant.DoesNotExist:
                return Response(
                    {"error": "Siz bu tadbirda ro‘yxatdan o‘tmagansiz"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"message": "Siz tadbirdan muvaffaqiyatli chiqdingiz."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Havola yaroqsiz yoki eskirgan"},
                status=status.HTTP_400_BAD_REQUEST,
            )
