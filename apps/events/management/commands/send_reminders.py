from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from threading import Thread
from apps.events.models import Event


def send_reminder_email(participant, event):
    subject = f"Ertaga yoki bugun bo‘lib o‘tadigan tadbir: {event.title}"
    message = (
        f"Salom {participant.first_name},\n\n"
        f"Siz {event.date} sanasida bo‘lib o‘tadigan '{event.title}' tadbirida ishtirokchisiz.\n\n"
        f"Vaqt: {event.start_time} - {event.end_time}\n"
        f"Manzil: {event.location}\n\n"
        f"Iltimos, o‘z vaqtida yetib boring!"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email="jamshidbekshodibekov2004@gmail.com",
            recipient_list=[participant.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {participant.email} - {e}")


class Command(BaseCommand):
    help = "Bugungi va ertangi tadbirlar uchun ishtirokchilarga email eslatma yuboradi"

    def get_upcoming_events(self):
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        for event in Event.objects.filter(date__in=[today, tomorrow]).iterator():
            yield event

    def handle(self, *args, **kwargs):
        threads = []

        for event in self.get_upcoming_events():
            for participant in event.participants.all():
                thread = Thread(target=send_reminder_email, args=(participant, event))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        self.stdout.write(self.style.SUCCESS("Emails sent successfully"))
