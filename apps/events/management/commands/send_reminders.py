from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from threading import Thread
from apps.events.models import Event, EventParticipant


def send_reminder_email(participant, event):
    subject = f"Ertaga yoki bugun bo‘lib o‘tadigan tadbir: {event.title}"
    message = (
        f"Salom {participant.first_name},\n\n"
        f"Siz {event.date} sanasida bo‘lib o‘tadigan '{event.title}' tadbirida ishtirokchisiz.\n\n"
        f"Vaqt: {event.start_time} - {event.end_time}\n"
        f"Manzil: {event.location}\n\n"
        f"Iltimos, o‘z vaqtida yetib boring!"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email='jamshidbekshodibekov2004@gmail.com',
        recipient_list=[participant.email],
        fail_silently=False
    )


class Command(BaseCommand):
    help = "Bugungi va ertangi tadbirlar uchun ishtirokchilarga email eslatma yuboradi"

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        events = Event.objects.filter(date__in=[today, tomorrow])

        if not events.exists():
            self.stdout.write(self.style.WARNING("Bugun yoki ertaga tadbir yo‘q."))
            return

        self.stdout.write(self.style.SUCCESS(f"{events.count()} ta tadbir topildi."))

        for event in events:
            participants = event.participants.filter(eventparticipant__is_active=True)

            for participant in participants:
                thread = Thread(target=send_reminder_email, args=(participant, event))
                thread.start()

            self.stdout.write(self.style.SUCCESS(
                f"Tadbir: {event.title} uchun {participants.count()} ta email yuborildi."
            ))
